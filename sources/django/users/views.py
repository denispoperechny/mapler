# Create your views here.

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context, loader

from django.shortcuts import render
from forms.LoginUserForm import LoginUserForm
from forms.CreateUserForm import CreateUserForm

from django.contrib.auth.models import User
# from django.contrib.auth.models import UserManager
from django.contrib.auth import authenticate, login as django_login, logout as django_logout

def login(request):
    errorMessage = ''
    if request.method == 'POST': # If the form has been submitted...
        form = LoginUserForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            errorMessage = tryLogin(form.cleaned_data['login'], form.cleaned_data['password'], request)
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
                errorMessage = tryLogin(form.cleaned_data['login'], form.cleaned_data['password'], request)
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

def logout(request):
    django_logout(request)
    return index(request)

def index(request):
    return HttpResponseRedirect("/")

def tryLogin(login, passwd, request):
    errorMessage = ''
    user = authenticate(username=login, password=passwd)
    if user is not None:
        django_login(request, user)
    else:
        errorMessage = "Your username and password were incorrect"
    
    return errorMessage

def tryCreate(login, passwd, mail=''):
    errorMessage = ''
    
    # Check if user already exists
    userExists = True
    try:
        existedUser = User.objects.get(username__exact=login)
    except User.DoesNotExist:
        userExists = False
    if userExists:
        errorMessage = 'User already exists with specified login: '+login

    # Create user
    if errorMessage == '':
        newUser = User.objects.create_user(login, mail, passwd)
        newUser.save()

    return errorMessage
