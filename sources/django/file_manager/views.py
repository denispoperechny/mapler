from map.models import Point, Attachment
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import os
import os.path
import time

def test(request):
	return HttpResponse("Tested")

def upload(request):
	f = request.FILES.get('attachment')
	pointId = request.POST['pointId']
	point = Point.objects.get(pk=int(pointId))

	newAttachment = Attachment()
	newAttachment.owner=request.user
	newAttachment.point=point
	newAttachment.fileName=f.name
	newAttachment.directory='.'
	newAttachment.save()

	path = _getFilesLocation() + _getFileName(newAttachment)
	# if not os.path.exists(os.path.dirname(directory)):
	# 	os.mkdir(directory, 0o777)
	destination = open(path, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()
	return HttpResponseRedirect(request.POST['redirectTarget'])

def delete(request, attchId):
	attch = Attachment.objects.get(pk=int(attchId))

	path = _getFilesLocation() + _getFileName(attch)
	if os.path.isfile(path):
		os.remove(path)

	attch.delete()
	return HttpResponse("Success")

def _getFilesLocation():
	return settings.MEDIA_ROOT

def _getFileName(attachment):
	return str(attachment.id) + "_" + attachment.fileName
