from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse

from .models import Event_User_log
from django.contrib.auth.models import User
from events.models import Events_model

from datetime import datetime


# Create your views here.
class CollectBrowsingData(View):

    def get(self, request):

        print(self.request)
        response = JsonResponse({"my_name":"Vikram bhavsar"})
        return response

    def post(self,request):
        print("-------------- CUSTOM CODE -----------------")
        userid = int(request.POST["user"])
        eventid = int(request.POST["eventid"])
        evidenceType = int(request.POST["evidenceType"])
        print("%s\t%s\t%s" % (type(userid),type(eventid),type(evidenceType)))

        log_user = User.objects.get(pk=userid)
        log_event = Events_model.objects.get(pk=eventid)
        log_event.e_regis_count += 1
        log_event.save()

        try:
            # will be executed if data is already present in the database
            event_log = Event_User_log.objects.get(user=log_user,event=log_event)
            print("[CC]\t Event and user intteraction exists")

            event_log.timedetails = datetime.now()

            if evidenceType == 1:
                print("[CC]\t User clicked on view registration")
                event_log.viewRegistration = event_log.viewRegistration + 1
            elif evidenceType == 2:
                print("[CC]\t User clicked on view location")
                event_log.viewLocation = event_log.viewLocation + 1
            elif evidenceType == 3:
                print("[CC]\t User clicked on view date")
                event_log.viewDate = event_log.viewDate + 1
            elif evidenceType == 4:
                print("[CC]\t User clicked on view details")
                event_log.viewDetails = event_log.viewDetails + 1

            event_log.save()

        except Event_User_log.DoesNotExist:
            print("[CC]\t Event and user intteraction doesnt exist")
            # will be executed when the user has interracted with the event for the first time.
            event_log = Event_User_log(user=log_user,event=log_event)

            event_log.timedetails = datetime.now()

            if evidenceType == 1:
                print("[CC]\t User clicked on view registration")
                event_log.viewRegistration = event_log.viewRegistration + 1
            elif evidenceType == 2:
                print("[CC]\t User clicked on view location")
                event_log.viewLocation = event_log.viewLocation + 1
            elif evidenceType == 3:
                print("[CC]\t User clicked on view date")
                event_log.viewDate = event_log.viewDate + 1
            elif evidenceType == 4:
                print("[CC]\t User clicked on view details")
                event_log.viewDetails = event_log.viewDetails + 1
            
            event_log.save()
        
            
        response = JsonResponse({"status":'done'})
        return response

        
