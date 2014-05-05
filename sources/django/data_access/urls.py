from django.conf.urls import patterns, url
#from data_access import views

urlpatterns = patterns('',
	# points
    (r'^point/(\d+)/$', 'data_access.views.point'),
    (r'^points/$', 'data_access.views.points'),
    (r'^points-by-user/(\S+)/$', 'data_access.views.pointsByUser'),
    # groups
    (r'^groups-owned-by-user/(\S+)/$', 'data_access.views.groupsOwnedByUser'),
    (r'^groups-by-user/(\S+)/$', 'data_access.views.groupsByUser'),
    (r'^group-members/(\S+)/$', 'data_access.views.groupMembers'),
    (r'^group-requests/(\S+)/$', 'data_access.views.groupRequests'),
    #
    (r'^group-search/(\S+)/$', 'data_access.views.groupSearch'),
)