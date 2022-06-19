from datetime import datetime
from django.db import models

class Logs(models.Model):
    date = models.DateTimeField(default=datetime.now)
    error_code = models.CharField(max_length=10)
    description = models.TextField()
