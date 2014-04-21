# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context, loader

from django.shortcuts import render
from forms.LoginUserForm import LoginUserForm
from forms.CreateUserForm import CreateUserForm


def login(request):
    errorMessage = ''
    if request.method == 'POST': # If the form has been submitted...
        form = LoginUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            errorMessage = tryLogin(form.cleaned_data['login'], form.cleaned_data['password'])
            if errorMessage == '':
                return index(request) # Redirect after POST
    else:
        form = LoginUserForm() # An unbound form

    return render(request, 'users/login.html', {
        'userForm': form,
        'userError': errorMessage,
    })

def create(request):
    errorMessage = ''
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            errorMessage = tryCreate(form.cleaned_data['login'], form.cleaned_data['password'], form.cleaned_data['mail'])
            if errorMessage == '':
                return index(request)
    else:
        form = CreateUserForm()

    return render(request, 'users/create.html', {
        'userForm': form,
        'userError': errorMessage,
    })

def profile(request):
    t = loader.get_template('users/profile.html')
    c = Context({
    #    'latest_poll_list': latest_poll_list,
    })
    return HttpResponse(t.render(c))

def index(request):
    return HttpResponseRedirect("/")

def tryLogin(login, passwd):
    return "Not implemented. Login: "+login

def tryCreate(login, passwd, mail=''):
    return "Not implemented. Login: "+login