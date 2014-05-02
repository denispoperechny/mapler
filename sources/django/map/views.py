# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader
from forms.AddPointForm import AddPointForm
from models import Point
from django.template import RequestContext
from django.template.loader import render_to_string
from django.core import serializers

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
	})
	return HttpResponse(t.render(c))

def submitPoint(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	form = AddPointForm(request.POST)
	if form.is_valid():
		maplerId = form.cleaned_data['maplerId']
		if maplerId == -1: # new point
			newPoint = Point(owner=request.user)
			updatePointAccordingToForm(form, newPoint)
			newPoint.save()
		else:
			point = Point.objects.get(pk=maplerId)
			if point.owner.username == userName:
				updatePointAccordingToForm(form, point)
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

def index(request):
	userName = getUserName(request)
	if userName != None:
		return HttpResponseRedirect("/map/overview")

	t = loader.get_template('map/index.html')
	c = Context({
		# 'userName': userName,
	})
	return HttpResponse(t.render(c))

def updatePointAccordingToForm(form, point):
	point.description = form.cleaned_data['description']
	point.latitude = form.cleaned_data['latitude']
	point.longitude = form.cleaned_data['longitude']


def getAddPointForm(request):
	addForm = AddPointForm(initial={'maplerId': -1})
	# editForm = LoginUserForm()
	#t = loader.get_template('map/point-edit.html')
	c = Context({ 
		# 'object_list': SomeModel.objects.all(),
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
