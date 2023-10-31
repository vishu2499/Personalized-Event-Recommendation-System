from django.db import models

class Event_category_model(models.Model):
    e_category = models.CharField(max_length=60)
    image_link = models.CharField(max_length=200,null=True,blank=True)

    def __str__(self):
        return str(self.id) + " " + self.e_category

# Create your models here.
class Events_model(models.Model):
    e_name = models.CharField(max_length=200)
    e_description = models.TextField()
    e_guest = models.CharField(max_length=100,blank=True,null=True)
    e_location = models.CharField(max_length=100,blank=True,null=True)
    e_time = models.DateTimeField(blank=True,null=True)
    e_category = models.ManyToManyField(Event_category_model)
    e_regis_count = models.IntegerField(default=0)
    e_image_link = models.CharField(max_length=100,blank=True,null=True)

    def increaseCount(self):
        self.e_regis_count += 1

    def __str__(self):
        return str(self.id) + " " + self.e_name        


class Event_keywords_model(models.Model):
    e_keyword = models.CharField(max_length=50)
    e_score = models.FloatField()
    e_event = models.ForeignKey(Events_model,related_name='event_keywords', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + "\t" + self.e_keyword + "\t" + str(self.e_score)


