from django.db import models


class Label(models.Model):
    key = models.CharField(max_length=32, primary_key=True)
    value = models.CharField(max_length=128, blank=True, default='')
