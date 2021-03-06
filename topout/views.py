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
    if mobileBrowser(request):
        c = get_context_for_m_gym_page(request, gym_slug)
        return render_to_response('m/m_gym.html', c, context_instance=RequestContext(request))
    else:
        c = get_context_for_gym_page(gym_slug)
        return render_to_response('gym.html', c, context_instance=RequestContext(request))

def gym_list_view(request):
    c = get_context_for_gym_list_page(request)

    if mobileBrowser(request):
        return HttpResponseRedirect(reverse('home_view'))
    else:
        return render_to_response('gym_list.html', c, context_instance=RequestContext(request))

def wall_view(request, gym_slug, wall_slug):
    if mobileBrowser(request):
        c = get_context_for_wall_page(request, wall_slug)
        return render_to_response('m/m_wall.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('gym_view', args=[gym_slug]))

def incomplete_routes_view(request, gym_slug):
    if mobileBrowser(request):
        c = get_context_for_incomplete_page(request, gym_slug)
        return render_to_response('m/m_incomplete.html', c, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('gym_view', args=[gym_slug]))

def add_completed_route_view(request):
    if request.method == 'POST' and request.user.is_authenticated():
        add_completed_route(request)
        if request.is_ajax():
            if request.REQUEST['incompletes'] is True:
                gym_slug = get_gym_slug_from_route_id(request.REQUEST['route_id'])
                c = get_context_for_incomplete_page(request, gym_slug)
                return render_to_response('m/js_route_table.html', c, context_instance=RequestContext(request))
            else:
                wall_slug = get_wall_slug_from_route_id(request.REQUEST['route_id'])
                c = get_context_for_wall_page(request, wall_slug)
                return render_to_response('m/js_route_table.html', c, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect(request.REQUEST['next'])
    else:
        return HttpResponseRedirect(reverse('home_view'))
