from django.conf.urls.defaults import *
from topout.views import *
from django.conf import settings

from django.contrib.auth import views as auth_views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$',
        home_view,
        name='home'),
    url(r'^social/',
        include('socialregistration.urls')),
    url(r'^accounts/',
        include('registration.urls')),
    url(r'^admin/',
        include(admin.site.urls)),
    url(r'^gyms/(?P<gym_slug>.*)/routes/(?P<route_id>.*)/complete/',
        add_completed_route_view),
    url(r'^gyms/(?P<gym_slug>.*)/',
        gym_view),
    url(r'^site_media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),
    # (r'^search/$', search_view),
)
