# Create your views here.

from django.http import HttpResponse
from django.template import Context, loader

def login(request):
    t = loader.get_template('users/login.html')
    c = Context({
    #    'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

def create(request):
    t = loader.get_template('users/create.html')
    c = Context({
    #    'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

def profile(request):
    t = loader.get_template('users/profile.html')
    c = Context({
    #    'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

def index(request):
    return login(request)