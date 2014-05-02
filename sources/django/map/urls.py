from django.conf.urls import patterns, url
from map import views

urlpatterns = patterns('',
    url(r'^$', views.index),
    url(r'^overview/', views.overview),
    url(r'^manage-points/', views.managePoints),
    url(r'^submit-point/', views.submitPoint),
    url(r'^delete-point/(\d+)/$', views.deletePoint),
)