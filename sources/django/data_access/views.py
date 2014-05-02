from django.http import HttpResponse, HttpResponseRedirect
from map.models import Point
from django.contrib.auth.models import User
import json

def point(request, pointId):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	point = Point.objects.get(pk=int(pointId))
	data = json.dumps(getPointInfo(point))
	return HttpResponse(data, content_type="application/json")

def pointsByUser(request, userLogin):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	userId = User.objects.get(username=userLogin)
	points = Point.objects.filter(owner=userId)
	resultSet = []
	for point in points:
		resultSet.append(getPointInfo(point))

	data = json.dumps(resultSet)
	return HttpResponse(data, content_type="application/json")

def points(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	points = Point.objects.all()
	resultSet = []
	for point in points:
		resultSet.append(getPointInfo(point))

	data = json.dumps(resultSet)
	return HttpResponse(data, content_type="application/json")

def getPointInfo(point):
	pointInfo = {
	'id': point.id,
	'owner': point.owner.username,
	'creationDate': "{:%d.%m.%Y %H:%M:%S}".format(point.creation_date),
	'latitude': str(point.latitude),
	'longitude': str(point.longitude),
	'description': point.description
	}

	return pointInfo

def getUserName(request):
	userName = None
	if request.user.is_authenticated():
		userName = request.user.username
	return userName