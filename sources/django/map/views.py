# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader


def index(request):
	userName = None
	if request.user.is_authenticated():
		userName = request.user.username

	t = loader.get_template('map/index.html')
	c = Context({
		'userName': userName,
	})
	return HttpResponse(t.render(c))
