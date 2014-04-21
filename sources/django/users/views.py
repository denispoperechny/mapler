# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context, loader

from django.shortcuts import render
from forms.LoginUserForm import LoginUserForm
from forms.CreateUserForm import CreateUserForm


def login(request):
    if request.method == 'POST': # If the form has been submitted...
        form = LoginUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return index(request) # Redirect after POST
    else:
        form = LoginUserForm() # An unbound form

    return render(request, 'users/login.html', {
        'form': form,
    })

def create(request):
    if request.method == 'POST': # If the form has been submitted...
        form = CreateUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # Process the data in form.cleaned_data
            # ...
            return index(request) # Redirect after POST
    else:
        form = CreateUserForm() # An unbound form

    return render(request, 'users/create.html', {
        'form': form,
    })

def profile(request):
    t = loader.get_template('users/profile.html')
    c = Context({
    #    'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

# def loginSubmit(request):
#     return index(request)

# def createSubmit(request):
#     return index(request)

def index(request):
    return HttpResponseRedirect("/")