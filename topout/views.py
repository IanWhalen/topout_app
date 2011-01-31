from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from models import *

def home_view(request):
    if not request.user.is_authenticated():
        home_activity_list = get_activity_for_home()

        c = {'home_activity_list': home_activity_list}
        c.update(csrf(request))
        return render_to_response('new_anon_home.html', c)
    else:
        user = request.user
        return render_to_response('user_home.html', {'user': user})

def gym_view(request, gym_slug):
    try:
        g = Gym.objects.get(gym_slug=gym_slug)
    except Gym.DoesNotExist:
        raise Http404

    try:
        gym_list, climber_list = create_route_lists(request.user, g)
    except:
        gym_list, climber_list = create_route_lists(0, g)

    c = {'g': g, 'user': request.user, 'gym_list': gym_list,
         'climber_list': climber_list}
    c.update(csrf(request))
    return render_to_response('gym.html', c)

def add_completed_route_view(request, gym_slug, route_id):
    if request.method == 'POST' and request.user.is_authenticated():
        try:
            r = Route.objects.get(id=route_id)
            g = Gym.objects.get(gym_slug=gym_slug)
        except:
            raise Http404
        add_completed_route(request.user, r)
        return HttpResponseRedirect('/gyms/%s' % gym_slug)
    else:
        latest_route_list = Route.objects.order_by('created')[0:10]
        return render_to_response('anon_home.html', {'latest_route_list':
                                                     latest_route_list})

#####################################################
#                                                   #
#            Helper Functions For Views             #
#                                                   #
#####################################################

def add_completed_route(user, route):
    """Tests if Completed_Route object for this user & route exists.
    If not, creates one."""
    obj, created = Completed_Route.objects.get_or_create(
        climber=user, route=route)
    if created:
        obj.save()
    else:
        pass

def create_route_lists(user, gym):
    """ Returns two object lists: all routes at gym and all routes climbed by
    signed-in user."""
    gym_routes_list = Route.objects.filter(gym=gym.id,
                                    is_avail_status=True).order_by('difficulty')

    routes_climbed_list = Route.objects.filter(completed_route__climber=user,
                                               is_avail_status=True).order_by('difficulty')

    return gym_routes_list, routes_climbed_list

def get_activity_for_home():
    route_list = Completed_Route.objects.order_by('created')[0:10]
    return route_list
