from django.db import models

class Images(models.Model):
    path = models.FilePathField()

