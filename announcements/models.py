from django.db import models

from quiz.models import Year_Level

class Announcements(models.Model):
    title = models.CharField(max_length = 200)
    year_level = models.ForeignKey(Year_Level, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length= 1000)
