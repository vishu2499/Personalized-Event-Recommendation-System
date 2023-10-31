# this python script is used to add similar events to already existing events. 
# this program populates the database. duringbrowsing, the user should be recommended events based on the events the user is viewing

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","event_recommender.settings")

import django

django.setup()

print("[+] Script Started..")


# importing requried libraries
import re, sqlite3,os
import pandas as pdr
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time,math


# importing
from events.models import Events_model,Event_category_model,Event_keywords_model
from recommender.models import SimilarEvents

# reading data from the CSV.
event_df = pd.read_csv('CSV_Data/all_events_new.csv')

class SimilarityCalculator():

    def get_record_split(self,sentence):

        rege = re.compile(r'[a-z0-9]{2,}')

        # returns list of words by removing any special characters from the string.
        return rege.findall(sentence)

    def getCosineSimilarity(self,stop_words):

        matrix = self.getTfIdfMatrix(stop_words)
        return cosine_similarity(matrix,matrix)

    def getTfIdfMatrix(self,stop_words):

        event_data_list = self.getProcessedEventData(stop_words)

        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform(event_data_list)
        
        return tfidf_matrix
    
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


# Getting stop words for extraction
from HelperPack import help
stop_words = help.getStopWords()


calc = SimilarityCalculator()

cosine_sim = calc.getCosineSimilarity(stop_words)


##### important thing to note here is that
##### cosine_sim[0] represent an event which has pk = 1

for indx in range(len(cosine_sim)):

    sorted_sim = list(enumerate(cosine_sim[indx]))
    sorted_sim = sorted(sorted_sim, key=lambda x: x[1], reverse=True)

    cur_even_sim = ''
    for evn_sim in sorted_sim:
        if evn_sim[1] > 0:
            cur_even_sim += str(evn_sim[0]+1) + " "
    

    cur_evn = Events_model.objects.get(pk=indx+1)

    sim_evn = SimilarEvents(event=cur_evn,similar_events=cur_even_sim)
    sim_evn.save()

