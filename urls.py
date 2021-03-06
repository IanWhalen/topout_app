from django.conf.urls.defaults import *
from topout.views import *
from django.conf import settings

from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        home_view,
        name='home_view'),
    url(r'^social/',
        include('socialregistration.urls')),
    url(r'^accounts/',
        include('registration.urls')),
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^route/complete/',
        add_completed_route_view),
    url(r'^gyms/(?P<gym_slug>.*)/walls/(?P<wall_slug>.*)/$',
        wall_view,
        name='wall_view'),
    url(r'^gyms/(?P<gym_slug>.*)/incomplete/$',
        incomplete_routes_view,
        name='incomplete_routes_view'),
    url(r'^gyms/(?P<gym_slug>.*)/$',
        gym_view,
        name='gym_view'),
    url(r'^gyms/$',
        gym_list_view,
        name='gym_list_view'),
    url(r'^site_media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
)
