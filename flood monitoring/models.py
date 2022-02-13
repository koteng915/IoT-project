from django.db import models
from django_pg_current_timestamp import CurrentTimestamp
import datetime
import pytz
import requests

# Create your models here.

class Dms(models.Model):
    time = models.TimeField()
    distance = models.FloatField()


    def __float__(self):
        return self.distance

    def __str__(self):
        return self.time

    """float for representing the MyModelName object (in Admin site etc.)."""

