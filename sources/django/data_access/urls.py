from django.conf.urls import patterns, url
#from data_access import views

urlpatterns = patterns('',
    (r'^point/(\d+)/$', 'data_access.views.point'),
    (r'^points/$', 'data_access.views.points'),
    (r'^points-by-user/(\S+)/$', 'data_access.views.pointsByUser'),
)