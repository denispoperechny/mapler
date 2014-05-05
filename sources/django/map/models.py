from django.db import models
from django.contrib.auth.models import User, Group

class Point(models.Model):
    owner = models.ForeignKey(User)
    owningGroup = models.ForeignKey(Group)
    creation_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=12, decimal_places=8)
    longitude = models.DecimalField(max_digits=12, decimal_places=8)

class GroupExtension(models.Model):
	owner = models.OneToOneField(User)
	description = models.CharField(max_length=200)
	creation_date = models.DateTimeField(auto_now_add=True)

class GroupJoinRequest(models.Model):
    initiator = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    creation_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    active = models.BooleanField()
