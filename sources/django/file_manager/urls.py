from django.conf.urls import patterns, url
from file_manager import views

urlpatterns = patterns('',
    (r'^upload/', views.upload),
    (r'^delete/(\d+)/$', views.delete),
)