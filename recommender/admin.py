from django.contrib import admin
from recommender.models import SimilarEvents,HistoryRecommendedEvents

# Register your models here.
admin.site.register(SimilarEvents)
admin.site.register(HistoryRecommendedEvents)