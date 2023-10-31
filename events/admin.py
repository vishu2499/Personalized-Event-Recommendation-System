from django.contrib import admin
from .models import Event_keywords_model,Events_model,Event_category_model

# Register your models here.
admin.site.register(Event_keywords_model)
admin.site.register(Events_model)
admin.site.register(Event_category_model)
