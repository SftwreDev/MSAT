from django.db import models

from quiz.models import Year_Level

class Handouts(models.Model):

    name = models.CharField(max_length=100)
    category = models.CharField(max_length = 200)
    year_level = models.ForeignKey(Year_Level, on_delete=models.CASCADE)
    documents = models.FileField(upload_to='handouts')
    description = models.CharField(max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Videos(models.Model):
    title = models.CharField(max_length=100)
    category = models.CharField(max_length = 200)
    year_level = models.ForeignKey(Year_Level, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    video = models.FileField(upload_to="videos")
    uploaded_at = models.DateTimeField(auto_now_add=True)
