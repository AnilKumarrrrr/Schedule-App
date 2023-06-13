from django.db import models
from django.contrib.auth.models import User
import datetime

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    date = models.DateField(default=datetime.date.today)  # Add default value
    start_time = models.TimeField()
    duration = models.IntegerField()

    def __str__(self):
        return self.name