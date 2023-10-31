from django.db import models
from events.models import Event_category_model
# Create your models here. 
class Organizer(models.Model):  
    ename = models.CharField(max_length=200)  
    edesc = models.CharField(max_length=1000)  
    eguest = models.CharField(max_length=150)  
    eloc = models.CharField(max_length=150)
    ecat = models.CharField(max_length=200)
    class Meta:  
        db_table = "organizer" 
