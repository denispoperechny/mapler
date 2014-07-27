from map.models import Point, Attachment, FileUploadSession, UserLog
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import os
import os.path
import time

def test(request):
	return HttpResponse("Tested")

def upload(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	f = request.FILES.get('attachment')
	pointId = request.POST['pointId']
	point = Point.objects.get(pk=int(pointId))

	newAttachment = Attachment()
	newAttachment.owner=request.user
	newAttachment.point=point
	newAttachment.fileName=f.name
	newAttachment.directory='.'
	newAttachment.save()

	newUplSession = FileUploadSession()
	newUplSession.attachment = newAttachment
	newUplSession.uploadIdentifier = request.POST['uploadIdentifier']
	newUplSession.save()

	path = _getFilesLocation() + _getFileName(newAttachment)
	# if not os.path.exists(os.path.dirname(directory)):
	# 	os.mkdir(directory, 0o777)
	destination = open(path, 'wb+')
	for chunk in f.chunks():
		destination.write(chunk)
	destination.close()

	newUplSession.uploadFinished = True
	newUplSession.uploadedPercentage = 100
	newUplSession.save()

	logRecord = UserLog()
	logRecord.ip = str(get_client_ip(request))
	logRecord.user = request.user
	logRecord.comment="File uploaded: " + f.name
	logRecord.save()

	return HttpResponseRedirect(request.POST['redirectTarget'])

def delete(request, attchId):
	attch = Attachment.objects.get(pk=int(attchId))

	path = _getFilesLocation() + _getFileName(attch)
	if os.path.isfile(path):
		os.remove(path)

	attch.delete()
	return HttpResponse("Success")

def isUploadCompleted(request, uploadIdentifier):
	# # Pretty hacky method
	# # upload sessions to be implemented
	# response=''
	# attachment = Attachment.objects.filter(fileName=fileName).latest('id')
	# response = attachment.directory
	# return HttpResponse(respons)
	session = FileUploadSession.objects.get(uploadIdentifier=uploadIdentifier)
	response=''
	if session.uploadFinished:
		response = 'true'
	else:
		response = 'false'

	return HttpResponse(response)


def _getFilesLocation():
	return settings.MEDIA_ROOT

def _getFileName(attachment):
	return str(attachment.id) + "_" + attachment.fileName

def getUserName(request):
	userName = None
	if request.user.is_authenticated():
		userName = request.user.username
	return userName

def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip