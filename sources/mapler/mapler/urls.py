from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mapler.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^map/', include('map.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^data/', include('data_access.urls')),
    url(r'^file/', include('file_manager.urls')),

    # Default app
    url(r'^$', include('map.urls'))

)