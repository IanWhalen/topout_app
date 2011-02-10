from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import *

from views_utils import *


#####################################################
#                                                   #
#            Desktop & Mobile Views                 #
#                                                   #
#####################################################

def home_view(request):
    if not request.user.is_authenticated():
        if mobileBrowser(request):
            c = {}
            c.update(csrf(request))
            return render_to_response('m/m_anon_home.html', \
                                      context_instance=RequestContext(request))
        else:
            home_activity_list = get_context_for_anon_home()
            c = {'home_activity_list': home_activity_list}
            c.update(csrf(request))
            return render_to_response('anon_home.html', c)
    else:
        if mobileBrowser(request):
            c = get_context_for_mobile_user_home(request)
            return render_to_response('m/m_user_home.html', c)
        else:
            c = get_context_for_user_home(request)
            return render_to_response('user_home.html', c)

def gym_view(request, gym_slug):
    c = get_context_for_gym_page(request, gym_slug)

    if mobileBrowser(request):
        return render_to_response('m/m_gym.html', c, context_instance=RequestContext(request))
    else:
        return render_to_response('gym.html', c, context_instance=RequestContext(request))

def wall_view(request, gym_slug, wall_slug):
    if mobileBrowser(request):
        c = get_context_for_wall_page(request, gym_slug, wall_slug)
        return render_to_response('m/m_wall.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('gym_view', args=[gym_slug]))

def add_completed_route_view(request, gym_slug, route_id):
    if request.method == 'POST' and request.user.is_authenticated():
        try:
            r = Route.objects.get(id=route_id)
            g = Gym.objects.get(gym_slug=gym_slug)
        except:
            raise Http404
        add_completed_route(request.user, r)
        return HttpResponseRedirect('/gyms/brooklyn-boulders/')
    else:
        latest_route_list = Route.objects.order_by('created')[0:10]
        return render_to_response('anon_home.html', {'latest_route_list':
                                                     latest_route_list})
