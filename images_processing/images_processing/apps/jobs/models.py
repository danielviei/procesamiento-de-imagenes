import datetime
import json

from django.db import models

class Jobs(models.Model):
    id = models.AutoField(primary_key=True)

class Steps(models.Model):
    job_id = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    step = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    start_time = models.DateTimeField(default=datetime.datetime.now())
    end_time = models.DateTimeField(default=datetime.datetime.now())
