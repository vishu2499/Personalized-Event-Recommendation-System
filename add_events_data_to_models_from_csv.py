
# This python script is used to add data from the CSV to the database.
# Available data To enter from the CSV:
# Event Name, Event Description, DateTime, Location, Organization, Category, 

# Model datafield Reference:
#     e_name = models.CharField(max_length=200)
#     e_description = models.TextField()
#     e_guest = models.CharField(max_length=100,blank=True)
#     e_location = models.CharField(max_length=100,blank=True)
#     e_time = models.DateTimeField(blank=True)

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","event_recommender.settings")

import django

django.setup()

print("[+] Script Started..")

from events.models import Events_model,Event_keywords_model
import pandas as pd


# Deleting all previous data from database
Events_model.objects.all().delete()
Event_keywords_model.objects.all().delete()

event_df = pd.read_csv('CSV_Data/all_events_new.csv')

for index, row in event_df.iterrows():

    event_obj = Events_model(e_name=row["Event Name"],e_description=row["Event Description"],e_location=row["Venue"])
    event_obj.save()

    print("[+] Adding: %s\t%s.." % (index,row["Event Name"]))
