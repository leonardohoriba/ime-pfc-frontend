# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Detection(models.Model):
    time = models.CharField(max_length=250)
    state = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    danger = models.FloatField()
    sensor = models.CharField(max_length=50)
    sensortype = models.CharField(max_length=25)

    def __str__(self):
        return self.time