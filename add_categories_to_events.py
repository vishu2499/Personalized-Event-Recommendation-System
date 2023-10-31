# this script is used to add categories to the events.
# Prerequisites:
# event_model has data already in it.



import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","event_recommender.settings")

import django

django.setup()

print("[+] Script Started..")

from events.models import Events_model,Event_keywords_model,Event_category_model
import pandas as pd

event_df = pd.read_csv('CSV_Data/all_events_new.csv')

for index, row in event_df.iterrows():
    key = index+1
    event = Events_model.objects.get(pk=key)
    event.e_category.clear()

    event_category = row["Category"].lower()

    if 'technology' in event_category:
        categ = Event_category_model.objects.get(pk=5)
        event.e_category.add(categ)
        event.save()

    elif 'dance' in event_category or 'dancing' in event_category:
        categ = Event_category_model.objects.get(pk=11)
        event.e_category.add(categ)
        event.save()

    elif 'food' in event_category:
        categ = Event_category_model.objects.get(pk=3)
        event.e_category.add(categ)
        event.save()

    elif 'wellness' in event_category:
        categ = Event_category_model.objects.get(pk=1)
        event.e_category.add(categ)
        event.save()

    elif 'travel' in event_category or 'tour' in event_category:
        categ = Event_category_model.objects.get(pk=7)
        event.e_category.add(categ)
        event.save()

    elif 'live' in event_category:
        categ = Event_category_model.objects.get(pk=6)
        event.e_category.add(categ)
        event.save()

    elif 'art' in event_category:
        categ = Event_category_model.objects.get(pk=4)
        event.e_category.add(categ)
        event.save()

    elif 'gaming' in event_category:
        categ = Event_category_model.objects.get(pk=9)
        event.e_category.add(categ)
        event.save()

    elif 'auto' in event_category:
        categ = Event_category_model.objects.get(pk=8)
        event.e_category.add(categ)
        event.save()

    elif 'sport' in event_category:
        categ = Event_category_model.objects.get(pk=10)
        event.e_category.add(categ)
        event.save()

    elif 'fashion' in event_category:
        categ = Event_category_model.objects.get(pk=2)
        event.e_category.add(categ)
        event.save()

    print("[+] Updating event %s to %s" % (event.id,event.e_category.all()))
    


