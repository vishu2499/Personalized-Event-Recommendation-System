from django.shortcuts import render
from django.contrib.auth.models import User

from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from recommender.models import HistoryRecommendedEvents

from events.models import Events_model,Event_keywords_model,Event_category_model
from datetime import date
from django.views.decorators.csrf import csrf_exempt

import json

from HelperPack import help

def getCosineBetHistoryAndEvents(sorted_keywords,keywords_dictionary,user_keywords_set,max_spread,min_spread):

    recommendationForUser = {}

    for event in Events_model.objects.all():

        keywords = []
        score = []
        
        for keywo in  event.event_keywords.all():
            keywords.append(keywo.e_keyword)
            score.append(keywo.e_score)

        
        event_keywords = {}
        event_keywords_set = set()

        # calculating top 50% of the keywords
        end = int(len(keywords) * 50 /100)
        for i in range(end):
            event_keywords[keywords[i]] = float(score[i])
            event_keywords_set.add(keywords[i])

        # calculating top 20% of the keywords
        end = int((len(user_keywords_set) * 10 )/ 100)
        temp_user_keyword_set = set()
        for i in range(min(50,len(sorted_keywords))):
            temp_user_keyword_set.add(sorted_keywords[i][0])

        # print("-----------USERS KEYWORD SET---------")
        # print(temp_user_keyword_set)
        # unionizing the two set
        keyword_set = set()
        keyword_set = event_keywords_set.intersection(temp_user_keyword_set)
        # print("%s\t%s" % (index,keyword_set)

        # now finally calculating the cosine similarity
        # the moment we have all been waiting for. 
        eucli_user = 0
        eucli_event = 0
        cosine = 0
        
        #temporarily tracking the words that match
        words_list = []
        # print("\nEvent Word List %s" % event_keywords_set)
        # print("Word List for event %s %s is %s\n" % (event.pk,event.e_name,keyword_set))
        for keyw in keyword_set:
    #         print("(%s) %s  and %s" % (keyw,event_keywords[keyw],sorted_keywords[keyw]))
            
            normalized_user_score = (keywords_dictionary[keyw] - min_spread)/(max_spread-min_spread)        
            cosine += event_keywords[keyw] * (normalized_user_score)
    #         print("Cosine for %s is %s" % (keyw,normalized_user_score))
            eucli_user += normalized_user_score ** 2
            eucli_event += event_keywords[keyw] ** 2
            words_list.append(keyw)

        eucli_user = eucli_user ** 0.5
        eucli_event = eucli_event ** 0.5
        
        # calculating final similarity
        similarity = 0
        if eucli_user != 0 and eucli_event != 0:
            similarity = cosine / (eucli_user * eucli_event)        

        # cosine value for that event is added to the dictionary    
        if similarity > 0:
            recommendationForUser[event.pk] = similarity

    # sorting the events in decreasing order
    sorted_tuples = sorted(recommendationForUser.items(), key=lambda item: item[1],reverse=True)

    return sorted_tuples
    # incase to display the items, uncomment the below code
    # for item in sorted_tuples:
        # print(item)

def putRecInDatabase(sorted_recs,user_id):
    
    # print("%s and its type %s" % (user_id,type(user_id)))
    cu_user = User.objects.get(id=user_id)

    if HistoryRecommendedEvents.objects.filter(user=cu_user).exists():
        # print("Data Already exists. Deleting")
        to_delete = HistoryRecommendedEvents.objects.get(user=cu_user)
        to_delete.delete()
    else:
        # print("Does not exists")
        pass

    recs = ""
    print("here is individual events sorted.")
    for eve in sorted_recs:
        recs += str(eve[0]) + " "

    # print("<%s>" % recs[:-1])

    # putting records into the database
    reco = HistoryRecommendedEvents(user=cu_user,rec_events=recs)
    reco.save()

    print(reco.user)
    print(reco.rec_events)
    print(reco.latest_update)

# Create your views here.
# following method is used to put data into the database
@csrf_exempt
def index(request):
    if request.method == 'GET':
        pass
        
    elif request.method == 'POST':
        print("POST REQUEST RECEIVED FOR STORING DATA")
        
        # print("this is from inside of the recommender function")
        jsonHistory = json.loads(request.body)

        records = []

        latestAccessTime = 1

        user_id = ""

        for element in jsonHistory:
            if 'user_id' in element.keys():
                user_id = element["user_id"]
                # print("User_ID that was receieved was %s" % element["user_id"])
            elif 'title' in element.keys():
                record = [element["title"],element["url"],element["time"]]
                records.append(record)

                if element["time"] > latestAccessTime:
                    latestAccessTime = element["time"]


        # sending processed history to the helper class which contains
        # code that processes the history data
        stop_words = help.getStopWords()

        history_recommender = help.HistoryRecommendation()

        sorted_keywords,keywords_dictionary, user_keywords_set, max_spread, min_spread = history_recommender.main_driver(records,latestAccessTime,stop_words)

        # calculating cosine similarity now.
        sorted_recs = getCosineBetHistoryAndEvents(sorted_keywords,keywords_dictionary, user_keywords_set, max_spread, min_spread)
        
        putRecInDatabase(sorted_recs,user_id)
        

    return HttpResponse("Received Data from server")

# this method is called again and again to check if new data is available to put into the database.
@csrf_exempt
def history_recommendations(request):

    if request.method == 'POST':
        # print("%s" % request.POST["user"])

        cu_user = User.objects.get(id=request.POST["user"])
        
        try:
            recs = HistoryRecommendedEvents.objects.get(user=cu_user)

            if recs.latest_update == date.today():
                
                eve_to_suggest = []
                events = recs.rec_events.split(' ')

                for eve in events:

                    if eve.isnumeric():

                        cu_event = Events_model.objects.get(id=eve)

                        temp = {}
                        temp["user_id"] = request.POST["user"]
                        temp["id"] = cu_event.pk
                        temp["name"] = cu_event.e_name
                        temp["image_link"] = cu_event.e_image_link
                        temp["description"] = cu_event.e_description
                        temp["guest"] = cu_event.e_guest
                        temp["location"] = cu_event.e_location
                        temp["date"] = cu_event.e_time
                        eve_to_suggest.append(temp)

                return JsonResponse(eve_to_suggest,safe=False)
            else:
                return JsonResponse({"success":"failed miserably"},safe=False,status=503)
        except Exception:
            return JsonResponse({"success":"failed miserably"},safe=False,status=503)



        # data = [{'name': 'Peter', 'email': 'peter@example.org'},
        # {'name': 'Julia', 'email': 'julia@example.org'}]

        # return JsonResponse(data,safe=False,status=503)







