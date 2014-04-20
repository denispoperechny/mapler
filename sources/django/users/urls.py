from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^login/', views.login),
    url(r'^create/', views.create),
    url(r'^profile/', views.profile),

    # Submitting a forms
    url(r'^login-submit/', views.loginSubmit),
    url(r'^create-submit/', views.createSubmit)
)