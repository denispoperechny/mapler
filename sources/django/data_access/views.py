from django.http import HttpResponse, HttpResponseRedirect
from map.models import Point, GroupJoinRequest, GroupExtension
from django.contrib.auth.models import User, Group
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

	user = User.objects.get(username=userLogin)
	data = modelToJson(Point.objects.filter(owner=user), getPointInfo)
	return HttpResponse(data, content_type="application/json")

def points(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	data = modelToJson(Point.objects.all(), getPointInfo)
	return HttpResponse(data, content_type="application/json")

def groupsOwnedByUser(request, userLogin):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	# Do anyone can see this?
	groups = []
	user = User.objects.get(username=userLogin)
	groupExts = GroupExtension.objects.filter(owner=user)
	for grExt in groupExts:
		groups.append(grExt.group)

	data = modelToJson(groups, getGroupInfo)
	return HttpResponse(data, content_type="application/json")

def groupsByUser(request, userLogin):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	# Do anyone can see this?
	groups = User.objects.get(username=userLogin).groups.all()
	data = modelToJson(groups, getGroupInfo)
	return HttpResponse(data, content_type="application/json")

def groupMembers(request, groupName):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	# Do anyone can see this?
	users = Group.objects.get(name=groupName).user_set.all()
	data = modelToJson(users, getUserInfo)
	return HttpResponse(data, content_type="application/json")

def groupSearch(request, groupName):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	# Do anyone can see this?
	# Refactor
	groupsResult = []
	groups = Group.objects.all()
	if groupName == "_all":
		groupsResult = groups
	else:
		for group in groups:
			if groupName.lower() in group.name.lower():
				groupsResult.append(group)

	data = modelToJson(groupsResult, getGroupInfo)
	return HttpResponse(data, content_type="application/json")

def groupRequests(request, groupName):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	# Do anyone can see this?
	group = Group.objects.get(name=groupName)
	requests = GroupJoinRequest.objects.filter(group=group)
	data = modelToJson(requests, getRequestInfo)
	return HttpResponse(data, content_type="application/json")

def modelToJson(modelSet, formatter):
	resultSet = []
	for model in modelSet:
		resultSet.append(formatter(model))

	return json.dumps(resultSet)

def getRequestInfo(request):
	requestInfo = {
	'group': request.group.name,
	'initiator': request.initiator.username,
	'comment': request.comment,
	'creationDate': formatDate(request.creation_date),
	}

	return requestInfo

def getGroupInfo(group):
	groupExt = GroupExtension.objects.get(group=group)

	groupInfo = {
	'name': group.name,
	'owner': groupExt.owner.username,
	'description': groupExt.description,
	'creationDate': formatDate(groupExt.creation_date),
	'userCount': len(group.user_set.all()),
	}

	return groupInfo

def getUserInfo(user):
	userInfo = {
	# 'id': point.id,
	'login': user.username,
	}

	return userInfo

def getPointInfo(point):
	pointInfo = {
	'id': point.id,
	'owner': point.owner.username,
	'group': point.owningGroup.name,
	'creationDate': formatDate(point.creation_date),
	'latitude': str(point.latitude),
	'longitude': str(point.longitude),
	'description': point.description
	}

	return pointInfo

def formatDate(date):
	return "{:%d.%m.%Y %H:%M:%S}".format(date)

def getUserName(request):
	userName = None
	if request.user.is_authenticated():
		userName = request.user.username
	return userName