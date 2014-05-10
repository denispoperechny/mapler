# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from forms.AddPointForm import AddPointForm
from forms.AddGroupForm import AddGroupForm
from models import Point, GroupExtension
from django.template import RequestContext
from django.template.loader import render_to_string
from django.contrib.auth.models import User, Group
import json

def getUserName(request):
	userName = None
	if request.user.is_authenticated():
		userName = request.user.username
	return userName

def overview(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	t = loader.get_template('map/overwiev.html')
	c = Context({
		'userName': userName,
		'previewPointHtmlData' : getPointPreviewHtml(),
		'viewName': 'Overwiev',
	})
	return HttpResponse(t.render(c))

def managePoints(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")
	
	t = loader.get_template('map/manage-points.html')
	c = Context({
		'userName': userName,
		'addingPointHtmlData' : getAddPointForm(request),
		'editingPointHtmlData': getEditPointForm(request),
		'viewName': 'Manage Points',
	})
	return HttpResponse(t.render(c))

# def submitPoint(request):
# 	userName = getUserName(request)
# 	if userName == None:
# 		return HttpResponseRedirect("/")

# 	form = AddPointForm(request.POST)
# 	if form.is_valid():
# 		maplerId = form.cleaned_data['maplerId']
# 		if maplerId == -1: # new point
# 			newPoint = Point(owner=request.user)
# 			updatePointAccordingToForm(form, newPoint)
# 			newPoint.save()
# 		else:
# 			point = Point.objects.get(pk=maplerId)
# 			if point.owner.username == userName:
# 				updatePointAccordingToForm(form, point)
# 				point.save()	

# 	return HttpResponseRedirect("/map/manage-points/")
def submitPoint(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	maplerId = int(request.POST['maplerId'])
	if maplerId == -1: # new point
		newPoint = Point(owner=request.user)
		updatePointAccordingToForm(request.POST, newPoint)
		newPoint.save()
	else:
		point = Point.objects.get(pk=maplerId)
		if point.owner.username == userName:
			updatePointAccordingToForm(request.POST, point)
			point.save()

	return HttpResponseRedirect("/map/manage-points/")

def deletePoint(request, pointId):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	point = Point.objects.get(pk=int(pointId))
	if (point.owner.username==userName) :
		point.delete()

	return HttpResponseRedirect("/map/manage-points/")

def manageGroups(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")
	
	t = loader.get_template('map/manage-groups.html')
	c = Context({
		'userName': userName,
		'createGroupFormData': getAddGroupForm(request),
		'viewName': 'Manage Groups',
	})
	return HttpResponse(t.render(c))

def index(request):
	userName = getUserName(request)
	if userName != None:
		return HttpResponseRedirect("/map/overview")

	t = loader.get_template('map/index.html')
	c = Context({
		# 'userName': userName,
	})
	return HttpResponse(t.render(c))

# def updatePointAccordingToForm(form, point):
# 	point.description = form.cleaned_data['description']
# 	point.latitude = form.cleaned_data['latitude']
# 	point.longitude = form.cleaned_data['longitude']
# 	# temporary fix
# 	point.owningGroup = Group.objects.all()[0]
def updatePointAccordingToForm(form, point):
	group = Group.objects.get(name=form['group'])

	point.description = form['description']
	point.latitude = form['latitude']
	point.longitude = form['longitude']
	# temporary fix
	point.owningGroup = group

def getAddPointForm(request):
	addForm = AddPointForm(initial={'maplerId': -1})
	c = Context({ 
		'mode': 'add',
		'form': addForm,
		})
	rendered = render_to_string('map/point-edit.html', c, context_instance=RequestContext(request))
	return rendered

def getEditPointForm(request):
	editForm = AddPointForm(initial={'maplerId': -1})
	c = Context({ 
		'mode': 'edit',
		'form': editForm,
		})
	rendered = render_to_string('map/point-edit.html', c, context_instance=RequestContext(request))
	return rendered

def getPointPreviewHtml():
	c = Context({ 
		#'mode': 'edit',
		})
	rendered = render_to_string('map/point-view.html', c)
	return rendered

def getAddGroupForm(request):
	addForm = AddGroupForm(initial={'maplerId': -1})
	c = Context({ 
		# 'mode': 'add',
		'form': addForm,
		})
	rendered = render_to_string('map/group-edit.html', c, context_instance=RequestContext(request))
	return rendered

def createGroupFormSubmit(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	if request.method != 'POST':
		return HttpResponse(json.dumps({'success': False, 'errorMessage': 'Please use POST method to submit a form'}), content_type="application/json")

	# form = AddGroupForm(request.POST)
	# valid = form.is_valid()
	# groupName = form.cleaned_data['name']
	groupName = request.POST['name']
	description = request.POST['description']

	if groupName == '':
		return HttpResponse(json.dumps({'success': False, 'errorMessage': 'Group name could not be empty'}), content_type="application/json")		

	uniqueName = True
	for (i, existedGroup) in enumerate(Group.objects.all()):
		if existedGroup.name.lower() == groupName.lower():
			uniqueName = False

	if not uniqueName:
		return HttpResponse(json.dumps({'success': False, 'errorMessage': 'Group with specified name already exists'}), content_type="application/json")

	newGroup = Group(name=groupName)
	newGroup.save()
	newGroup.user_set.add(request.user)
	newGroup.save()
	groupNameExt = GroupExtension(group=newGroup, description=description, owner=request.user)
	groupNameExt.save()
	
	return HttpResponse(json.dumps({'success': True}), content_type="application/json")

def deleteGroup(request, groupName):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	group = Group.objects.get(name=groupName)
	groupExt = GroupExtension.objects.get(group=group)
	points = Point.objects.filter(owningGroup=group)
	for (i, point) in enumerate(points):
		point.delete()
	groupExt.delete()
	group.delete()

	return HttpResponseRedirect("/map/manage-groups/")

def addUserToGroup(request, userName, groupName):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	group = Group.objects.get(name=groupName)
	user = User.objects.get(username=userName)
	group.user_set.add(user)
	group.save()

	return HttpResponseRedirect("/map/manage-groups/")

def removeUserFromGroup(request, userName, groupName):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	group = Group.objects.get(name=groupName)
	user = User.objects.get(username=userName)
	group.user_set.remove(user)
	group.save()

	return HttpResponseRedirect("/map/manage-groups/")


