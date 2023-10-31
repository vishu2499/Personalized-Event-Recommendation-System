from django.shortcuts import render
from .models import Events_model, Event_keywords_model,Event_category_model
from django.contrib.auth.models import User
from django.db.models import Q


from recommender.models import SimilarEvents
from collector.models import Event_User_log
from user_app.models import UserSearch

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from datetime import datetime

# adding location imports
import pandas as pd
import geopandas as gpd
import geopy
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
# import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster



def get_courousel_list_for_objects(data_obj):
    proper_count = 0

    count = 0
    courousel_list = []
    courousel_list_active = []
    obj_list = []

    for obj in data_obj:
        if proper_count >= 4:
            obj_list.append(obj)
            count += 1

            if count == 4:
                print(obj_list)
                count = 0
                courousel_list.append(obj_list)
                obj_list = []
        else:
            courousel_list_active.append(obj)
            proper_count += 1


    #adding remaining events to the list
    if count != 0:
        courousel_list.append(obj_list)
        
    return courousel_list_active,courousel_list

def getHomePage(request):

    trendingEvents = Events_model.objects.order_by("-e_regis_count")
    categories = Event_category_model.objects.all()
    context = {'categories':Event_category_model.objects.all()}

    # getting events coural ready
    trending_active_eves,trending_eves = get_courousel_list_for_objects(trendingEvents)
    context["trending_active_eves"] = trending_active_eves
    context["trending_eves"] = trending_eves


    return render(request,"events/main_page.html",context)

# Create your views here.
def index(request):

    trending_events = Events_model.objects.get().order_by("-e_regis_count")

    


    data_obj = Event_category_model.objects.all()

    count = 0

    courousel_list = []
    obj_list = []

    for obj in data_obj:
        obj_list.append(obj)
        count += 1

        if count == 3:
            # print(obj_list)
            count = 0
            courousel_list.append(obj_list)
            obj_list = []
        
    # print(courousel_list)

    return render(request,"events/temp.html",{"data_obj":courousel_list})

class EventsListView(ListView):

    model = Events_model
    template_name = 'events/events_list.html'
    # template_name = 'static_html/demo.html'
    context_object_name = "events"

    def get(self, request, *args, **kwargs):

        print(kwargs)
        return super().get(request, *args, **kwargs)

    def get_queryset(self): 
        if 'category_pk' in self.kwargs:
            category_pk = self.kwargs["category_pk"]
            return Events_model.objects.filter(e_category=Event_category_model.objects.get(pk=category_pk)).order_by("-e_regis_count")
            
        else:
            print("\t\t\tNormal GET function")
            
            # checking if user has searched for any events
            if 'search_q' in self.request.GET:
                search_term = self.request.GET["search_q"]
                
                print("Here is the search term: %s" % search_term)

                if self.request.user.is_authenticated:
                    cu_user = User.objects.get(pk=self.request.user.id)
                    new_search = UserSearch(user=cu_user,search_term=search_term,time_details=datetime.now())
                    new_search.save()

                return Events_model.objects.filter(Q(e_name__contains=search_term)| Q(e_description__contains=search_term))
                
            else:
                print("Normal search is taking place.")
                return super().get_queryset()

    def get_context_data(self, **kwargs):

        # does not differentiate between passing the keywords and not passing the keywords
        # i.e website/events/  and  website/events/2
        
    
        context = super().get_context_data(**kwargs)
        context["categories"] = Event_category_model.objects.all()

        print("----CUSTOM CODE----")
        print("%s" % kwargs)
        # not giving trending events if not required:
        if 'category_pk' not in self.kwargs and 'search_q' not in self.request.GET:
            for cat in Event_category_model.objects.all():
                context[str(cat.e_category).replace(" ","_").replace("&","and").replace(",","")] = Events_model.objects.filter(e_category=cat).order_by("-e_regis_count")
            

        # only showing the results if its not a search request
        if 'search_q' not in self.request.GET:

            if self.request.user.is_authenticated:

                # print("user is authenticated")
                # following is a list (getting rec based on event clicks)
                user_clicks_recommends_temp = get_recs_based_on_click_events(self.request.user)
                user_clicks_recommends = []
                if 'user_location' in self.request.GET:

                    # getting user's location
                    user_location_in_list = self.request.GET["user_location"].split('--')
                    user_loc = (user_location_in_list[0],user_location_in_list[1])
                    # tuple of user's location

                    for eve_id in user_clicks_recommends_temp:
                        eve = Events_model.objects.get(pk=eve_id)

                        if eve.e_location != 'online':
                                loc = eve.e_location
                                locator = Nominatim(user_agent="myGeocoder")
                                location = locator.geocode(loc)
                                event_loc = (location.latitude,location.longitude)

                                if geodesic(event_loc, user_loc).km > 50:
                                    print("Distance is: %s" % geodesic(event_loc, user_loc).km)
                                    print("Distance between the event and user is more than 50km")
                                    print("hence not adding the event to recommendation")
                                    continue
                                
                        user_clicks_recommends.append(eve_id)


                else:
                    user_clicks_recommends = user_clicks_recommends_temp

                # print("here are the click events %s" % user_clicks_recommends)


                user_clicks_recommends = Events_model.objects.filter(pk__in=user_clicks_recommends)
                
                
                # getting results based on past search history
                cu_user = User.objects.get(pk=self.request.user.id)
                # following is a queryset 
                user_browse_recommends = UserSearch.objects.filter(user=cu_user).order_by("-time_details")
                user_browse_recommendation_list = []

                # to get only last two searches
                search_count = 0
                for user_search in user_browse_recommends:
                    search_count += 1
                    
                    # taking only last two search count to show.
                    if search_count >= 4:
                        break

                    search_events = Events_model.objects.filter(Q(e_name__contains=user_search.search_term)| Q(e_description__contains=user_search.search_term))

                    # removing already registered event from the search
                    non_registered_event = []
                    for srch_event in search_events:
                        event_id = srch_event.id
                        search_event = Events_model.objects.get(pk=event_id)
                        
                        if Event_User_log.objects.filter(user=cu_user,event=search_event).exists():
                            eve_user_log = Event_User_log.objects.get(user=cu_user,event=search_event)
                            if eve_user_log.viewRegistration > 0:
                                pass
                            else:
                                non_registered_event.append(event_id)
                        else:
                            non_registered_event.append(event_id)

                    # putting back results into the same object.
                    search_events = Events_model.objects.filter(pk__in=non_registered_event)
                    

                    for srch_event in search_events:    

                        print("------------------------------------")
                        print("%s" % self.request.GET)

                        if 'user_location' in self.request.GET:
                            # print("User's Location is: %s" % self.request.GET["user_location"])

                            user_location_in_list = self.request.GET["user_location"].split('--')
                            user_loc = (user_location_in_list[0],user_location_in_list[1])

                            print("%s is the user's location\n%s is the cordinateds\n\n" % (srch_event.e_location,user_loc))
                            if srch_event.e_location != 'online':
                                loc = srch_event.e_location
                                locator = Nominatim(user_agent="myGeocoder")
                                location = locator.geocode(loc)
                                event_loc = (location.latitude,location.longitude)

                                if geodesic(event_loc, user_loc).km > 50:
                                    print("Distance is: %s" % geodesic(event_loc, user_loc).km)
                                    print("Distance between the event and user is more than 50km")
                                    print("hence not adding the event to recommendation")
                                    continue
                                
                        user_browse_recommendation_list.append(srch_event)

                # adding the data recieved to the conttext
                click_recs_carousal_active,click_recs_carousal = get_courousel_list_for_objects(user_clicks_recommends)
                browse_recs_carousal_active,browse_recs_carousal = get_courousel_list_for_objects(user_browse_recommendation_list)

                context["user_click_recommendations_active"] = click_recs_carousal_active
                context["user_click_recommendations"] = click_recs_carousal
                context["user_browse_recommendations_active"] =browse_recs_carousal_active
                context["user_browse_recommendations"] = browse_recs_carousal
                # print("------CUSTOM CODE ----")
                # print("\n%s\n\n%s"% (click_recs_carousal_active,click_recs_carousal))

        # print("Custome code-----")
        # for eve_key in context.keys():
        #     print("\n\n%s\n\n%s\n\n"% (eve_key,context[eve_key]))
        
        return context

class EventDetailView(DetailView):
    model = Events_model

    template_name = 'events/events_details.html'

    context_object_name = "event"

    def get_context_data(self, **kwargs):

        # getting other similar events        
        print("----custom code----")
        cur_even_pk = self.kwargs['pk']

        similar_events_id = SimilarEvents.objects.get(pk=cur_even_pk)
        similar_events_id = similar_events_id.similar_events.split(' ')

        # converting values to integer
        similar_events_id_int = []
        for sim_id in similar_events_id:
            if sim_id.isnumeric():
                similar_events_id_int.append(int(sim_id))
        
        # similar_events = Events_model.objects.filter(pk__in=[similar_events_id_int[1:min(6,len(similar_events_id_int))]])   
        similar_events = Events_model.objects.filter(pk__in=similar_events_id_int[1:min(6,len(similar_events_id_int))])

        context = super().get_context_data(**kwargs)
        context['similar_events'] = similar_events
        # print(context)
        
        return context

# this method takes event id and gets Top five events similar to it 
def getTopFiveSimilarEvents(cur_even_pk):

    # print("[+]\tINSIDE SIMILAR EVENTS")

    similar_events_id = SimilarEvents.objects.get(pk=cur_even_pk)
    similar_events_id = similar_events_id.similar_events.split(' ')

    # converting values to integer
    similar_events_id_int = []
    for sim_id in similar_events_id:
        if sim_id.isnumeric():
            similar_events_id_int.append(int(sim_id))

    return similar_events_id_int[1:min(6,len(similar_events_id_int))]

# this function is called by "get_recs_based_on_click_events"
# and it returns list of integer that is the key used for recommending events
def get_recs_from_regis_and_not_regis(high_regis_event,high_not_regis_event):

    recs_list = []
    if high_regis_event is not None and high_not_regis_event is not None:
        recs_list.append(high_not_regis_event)

        similar_list = getTopFiveSimilarEvents(high_regis_event)
        for eve in similar_list:
            recs_list.append(eve)

        similar_list = getTopFiveSimilarEvents(high_not_regis_event)
        for eve in similar_list:
            recs_list.append(eve)

        # print("Showing similar events for %s" % high_regis_event)
        # print("Final List which is generated for recommendation is %s" % recs_list)
        # print("\n\n")
    elif high_regis_event is not None and high_not_regis_event is None:

        # only putting similar events based on highest score that have been registered
        similar_list = getTopFiveSimilarEvents(high_regis_event)
        for eve in similar_list:
            recs_list.append(eve)

    elif high_regis_event is None and high_not_regis_event is not None:


        # only putting similar events based on highest score that havent been registered
        recs_list.append(high_not_regis_event)
        similar_list = getTopFiveSimilarEvents(high_not_regis_event)
        for eve in similar_list:
            recs_list.append(eve)

    # when both are null below option would be executed.
    else:
        print("\t\tInside Else tag where the  user has not intteracted with any events.")
        pass

    return recs_list

# This method calculates scores of various evidence.
def get_recs_based_on_click_events(user):

    # print("---INSIDE THE GET RECS BASED ON CLICK METHOD--")
    # print(user)

    cu_user = User.objects.get(pk=user.id)

    evidences = Event_User_log.objects.filter(user=cu_user)

    # dictionary which stores the score and event id from below.
    evidences_id = {}


    # calculating score:
    for evidence in evidences:
        score = 0
        # print("[+] Investigation %s" % evidence)
        if evidence.viewRegistration > 0:
            score += 100
            # print("Has Viewed Registration")
        
        # checking view date and location together. (very strong chance the user is intrested)
        if evidence.viewDate > 0 and evidence.viewLocation > 0:
            score += 80
        elif evidence.viewDate > 0 or evidence.viewLocation > 0:
            score += 40
        
        if evidence.viewDetails > 0:
            score += 20

        if score > 0:
            evidences_id[evidence.event.id] = score

        print("Final Score is - %s for %s" % (score,evidence))
    
    # sorting the dictionary based on values.
    sorted_evidence = sorted(evidences_id.items(), key=lambda x: x[1],reverse=True)  

    # print("Following is the sorted tuple %s " % sorted_evidence)
    # print("Type is %s" % type(sorted_evidence))

    # stands for highest scored events which are registered or not registered.
    # this is used to store just the event ids.
    high_not_regis_event = None
    high_regis_event = None

    # this is used to store database object
    high_not_regis_event_obj = None
    high_regis_event_obj = None

    for evide in sorted_evidence:
        cu_event = Events_model.objects.get(pk=evide[0])
        
        cu_log = Event_User_log.objects.get(user=cu_user,event=cu_event)
        if cu_log.viewRegistration == 0:

            if high_not_regis_event is None:
                high_not_regis_event = cu_event.id
                high_not_regis_event_obj = cu_log

            # Updating the variables if there's a recent entry
            elif high_not_regis_event is not None and cu_log.timedetails > high_not_regis_event_obj.timedetails:
                high_not_regis_event = cu_event.id
                high_not_regis_event_obj = cu_log

            # print("%s has not been registered" % cu_log)
        else:

            if high_regis_event is None:
                high_regis_event = cu_event.id
                high_regis_event_obj = cu_log

            # Updating the variables if there's a recent entry
            elif high_regis_event is not None and cu_log.timedetails > high_regis_event_obj.timedetails:
                high_regis_event = cu_event.id
                high_regis_event_obj = cu_log


    print("Choosen (Not Registered): %s" % high_not_regis_event_obj)
    print("Choosen (Registered): %s" % high_regis_event_obj)

    print("Choosen ID (Not Registered): %s" % high_not_regis_event)
    print("Choosen ID (Registered): %s" % high_regis_event)
            # print("%s has been registered" % cu_log)
    # print("%s and %s" % (high_not_regis_event,high_regis_event))

    return get_recs_from_regis_and_not_regis(high_regis_event,high_not_regis_event)

    
    # for reference
    # timedetails = models.DateField(default=datetime.date.today)
    # viewDetails = models.IntegerField(default=0)
    # viewDate = models.IntegerField(default=0)
    # viewLocation = models.IntegerField(default=0)
    # viewRegistration = models.IntegerField(default=0)
    


    