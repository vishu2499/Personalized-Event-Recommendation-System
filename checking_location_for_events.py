# this python script is used to add similar events to already existing events. 
# this program populates the database. duringbrowsing, the user should be recommended events based on the events the user is viewing

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE","event_recommender.settings")

import django

django.setup()

print("[+] Script Started..")

import pandas as pd
import geopandas as gpd
import geopy
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
# import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster


my_lat = 19.2225459
my_lon = 72.9713379

my_cor = (my_lat,my_lon)


from events.models import Events_model

locator = Nominatim(user_agent="myGeocoder")

for event in Events_model.objects.all():
    print("[+] Processing: %s:\t%s" % (event.id,event.e_name))
    print("\t location: '%s'" % (event.e_location))

    try:
        location = locator.geocode(event.e_location)
        print("\t Latitude: %s\tLongitude:%s" % (location.latitude, location.longitude))
        dest_cor = (location.latitude,location.longitude)
        print("\t Distance in kilometers: %s" % (geodesic(my_cor, dest_cor).km))
    except:
        print("\t [+]: location not available:")
        pass
    finally:
        print("\n")
