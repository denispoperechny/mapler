from django.db import models
from django.contrib.auth.models import User

class Point(models.Model):
    owner = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)
