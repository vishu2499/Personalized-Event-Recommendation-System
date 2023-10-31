# this file contains standalone method that requires help to other classes.

import re,math


def getStopWords():
    custom_stop_words = set()
    file_to_read = open('static/google_long_list_stop_words.txt','r')
    lines = file_to_read.readlines()
    file_to_read.close()

    for line in lines:
        custom_stop_words.add(line[:-1])

    return custom_stop_words


class HistoryRecommendation():

    def get_record_split(self,sentence):
        rege = re.compile(r'[a-z0-9]{2,}')

        # returns list of words by removing any special characters from the string.
        return rege.findall(sentence)

    def main_driver(self,records,latest_access_time,stop_words):

        word_count = {}

        for record in records:


            if record[0] is not None and record[2] is not None:

                current_record = record[0].lower()

                # getting the words
                words = self.get_record_split(current_record)

                # preprocessing on single words.
                for word in words:
                    if word not in stop_words and not word.isnumeric() and word not in ['facebook','google','youtube','instagram','twitter','gmail','drive','amigos','ers','ppt','slides','event','registration','form']:
                        
                        if word not in word_count.keys():
                            word_count[word] = [1,[record[2]],record[2]]
                        else:
                            li = word_count[word]
                            li[0] = li[0] + 1
                            li[1].append(record[2])
                            li[2] = li[2] + record[2]
                            word_count[word] = li
        
        # keyword_set is a set containing all the keywords (used for weighted cosine similarity)
        
        keywords,keyword_set,max_spread,min_spread = self.getSpread(word_count,latest_access_time)
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        
        return sorted_keywords,keywords,keyword_set,max_spread,min_spread
        
    def getSpread(self,word_counts,latest_access_time):

        # dictionary structure is:
        # {'word': [frequency, [t1,t2,t2,t3] , total]}
        keywords = {}
        
        max_spread = 0
        min_spread = float("inf")
        
        # set used for calculating weighted cosine similarity
        keyword_set = set()
        
        for word in word_counts.keys():

            mean = word_counts[word][2]/word_counts[word][0]
            spread = 0
            li = word_counts[word][1]

            # submission
            for time_stamp in li:
                if (latest_access_time-mean) > 0:
                    spread += ((time_stamp - mean) ** 2)/math.log(latest_access_time-mean)
                
            if spread > 0:
            
                if spread > max_spread:
                    max_spread = spread

                if spread < min_spread:
                    min_spread = spread

                keywords[word] = spread
                
                # adding the word to main keyword set
                keyword_set.add(word)

        return keywords, keyword_set, max_spread, min_spread


