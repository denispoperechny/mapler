# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader


def index(request):
    t = loader.get_template('map/index.html')
    c = Context({
    #    'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))
