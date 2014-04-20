from django.conf.urls import patterns, url
from users import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.login, name='login'),
    url(r'^create/', views.create, name='create'),
    url(r'^profile/', views.profile, name='profile')
    #,url(r'^test/', views.test, name='test')
)