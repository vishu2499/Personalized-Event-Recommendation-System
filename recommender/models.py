from django.db import models

from events.models import Event_category_model,Events_model, Event_keywords_model
from django.contrib.auth.models import User
from django.utils import timezone

from datetime import date

# Create your models here.
class SimilarEvents(models.Model):
    event = models.OneToOneField(Events_model,on_delete=models.CASCADE,primary_key=True)
    similar_events = models.CharField(max_length=200)

    # def __str__(self):
    #     return event


class HistoryRecommendedEvents(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    rec_events = models.CharField(max_length=300)
    latest_update = models.DateField(default=date.today())

    

    # def __str__(self):
    #     return user



    
