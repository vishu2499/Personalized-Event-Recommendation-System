from django.contrib import admin
from .models import UserProfile,UserSearch

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserSearch)