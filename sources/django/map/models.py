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
	group = models.OneToOneField(Group)
	owner = models.ForeignKey(User)
	description = models.CharField(max_length=200)
	creation_date = models.DateTimeField(auto_now_add=True)

class GroupJoinRequest(models.Model):
    initiator = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    creation_date = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=200)
    active = models.BooleanField()

class Attachment(models.Model):
    owner = models.ForeignKey(User)
    point = models.ForeignKey(Point)
    creation_date = models.DateTimeField(auto_now_add=True)
    fileName = models.CharField(max_length=256)
    directory = models.CharField(max_length=256)

class FileUploadSession(models.Model):
    attachment = models.ForeignKey(Attachment)
    uploadIdentifier = models.CharField(max_length=256)
    uploadFinished = models.BooleanField(default=False)
    uploadedPercentage = models.IntegerField(default=0)

