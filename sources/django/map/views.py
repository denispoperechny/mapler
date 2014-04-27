# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, loader

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
	})
	return HttpResponse(t.render(c))

def managePoints(request):
	userName = getUserName(request)
	if userName == None:
		return HttpResponseRedirect("/")

	t = loader.get_template('map/manage-points.html')
	c = Context({
		'userName': userName,
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
