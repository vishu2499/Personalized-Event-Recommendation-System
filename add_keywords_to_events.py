# This python script is used to populate keywords based on the event database
# in real however, the keywords would be calculated on fly as new events are added to the database.
# all events would be taken up inside an array and TF*IDF score would then be calculated.

# Dependencies
# sklearn
# pandas

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","event_recommender.settings")

import django

django.setup()

print("[+] Script Started..")

from events.models import Events_model,Event_keywords_model

# importing packages required for tf*idf score.
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class KeywordsExtraction:

    def get_record_split(self,sentence):
        rege = re.compile(r'[a-z0-9]{2,}')

        # returns list of words by removing any special characters from the string.
        return rege.findall(sentence)

    def getProcessedEventData(self,stop_words):
        # gets event details after pre-processing by removing stop words and combining event
        # title and event Description together.
        unprocessed_events_list = []

        for event in Events_model.objects.all():
            temp = str(event.e_name) + " " +  str(event.e_description)
            unprocessed_events_list.append(temp)


        processed_events_list = []
        for event in unprocessed_events_list:
            words = self.get_record_split(event.lower())

            current_event = ""

            for word in words:
                if word not in stop_words and not word.isnumeric():
                    current_event += word + " "
            
            processed_events_list.append(current_event)

        return processed_events_list

    def tf_idf_get_keywords_list(self,event_data_list):
        # a list of keywords for a particular event that will added to the main data frame as a setence
        # and will be used during cosine similarity between events and interest extracted.
        keywords_list = []
        scores_list = []
    
        
        # calculating the keywords
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(event_data_list)

        feature_names = vectorizer.get_feature_names()

        # dense = vectors.todense()
        # print(vectors[0].todense().tolist())
        
        # constructing a list of keywords for each specific event
        for event_count in range(len(event_data_list)):
            
            score = {'tf_idf': vectors[event_count].todense().tolist()[0]}

            df = pd.DataFrame(score,index=feature_names)
            df = df.sort_values('tf_idf',ascending=False)
            
            # keywords and scores would be appaned to data_frame 
            current_event_keywords = ""
            current_event_tf_idf_scores = ""
            
            for index, row in df.iterrows():
                if row["tf_idf"] > 0:
                    current_event_keywords += index + " "
                    current_event_tf_idf_scores += str(row["tf_idf"]) + " "

                    
            keywords_list.append(current_event_keywords)
            scores_list.append(current_event_tf_idf_scores)



        #     print(df.head(50))
        return keywords_list,scores_list

    def updateKeywordsAndScoreToDatabase(self,stop_words):
        # this method is responsible to update the keywords and their respected scores into the database

        # ----- Structure of Event Keywords Model
        #       e_keyword = models.CharField(max_length=50)
        #       e_score = models.FloatField()
        #       e_event = models.ForeignKey(Events_model, on_delete=models.CASCADE)
        keywords_list, scores_list = self.tf_idf_get_keywords_list(self.getProcessedEventData(stop_words))

        event_count = 0


        for event in Events_model.objects.all():

            print("[+] Adding keywords for event #%s" % event.id)

            event_keywords = keywords_list[event_count].split(' ')
            keyw_scores = scores_list[event_count].split(' ')
        
            for event_keyw_count in range(len(keyw_scores)):
                single_keyw = event_keywords[event_keyw_count]
                single_score = keyw_scores[event_keyw_count] 

                if single_keyw != '' and single_score != '':
                    event_keyword = Event_keywords_model(e_keyword=single_keyw,e_score=single_score,e_event=event)
                    event_keyword.save()

            # incrementing list counter.
            event_count += 1
  
# Getting stop words for extraction
from HelperPack import help
stop_words = help.getStopWords()

extractioner = KeywordsExtraction()

extractioner.updateKeywordsAndScoreToDatabase(stop_words)
