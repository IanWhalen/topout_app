from models import *
from django.http import Http404
from datetime import datetime, timedelta
from django.utils import simplejson
import urllib

#####################################################
#                                                   #
#            Primary Context Generators             #
#                                                   #
#####################################################

def get_context_for_mobile_user_home(request):
    last_route = get_last_route_for_user(request.user)
    c = {'user': request.user,
         'last_route': last_route}
    return c

def get_context_for_anon_home():
    route_list = Completed_Route.objects.order_by('created')[0:5]
    return route_list

def get_context_for_user_home(request):
    last_route = get_last_route_for_user(request.user)
    prev_session = get_completes_in_prev_session(request.user)
    c = {'user': request.user,
         'last_route': last_route,
         'prev_session': prev_session}
    return c

def get_context_for_wall_page(request, wall_slug):
    wall = get_wall_from_slug(wall_slug)
    route_list = get_list_for_wall(request.user, wall)

    c = {'user': request.user,
         'route_list': route_list,
         'wall': wall}
    return c

def get_context_for_gym_page(request, gym_slug):
    gym = get_gym_from_slug(gym_slug)
    gym_map = get_map_for_gym(gym)
    wall_list, route_list, climb_count = get_lists_for_gym(request.user, gym)

    c = {'gym': gym,
         'user': request.user,
         'gym_map': gym_map,
         'route_list': route_list,
         'wall_list': wall_list,
         'climb_count': climb_count}
    return c

def get_context_for_gym_list_page(request):
    gym_list = get_gym_list()

    c = {'gym_list': gym_list}
    return c


#####################################################
#                                                   #
#            Mobile Phone Detection                 #
#                                                   #
#####################################################

mobiles_uas = [
    'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
    'blaz','brew','cell','cldc','cmd-','dang','doco','hipt','inno',
    'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
    'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
    'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
    'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
    'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
    'toshi','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
    'wapr','webc','winw','winw','xda','xda-'
    ]

mobile_ua_hints = [ 'SymbianOS', 'Opera Mini', 'iPhone' ]

def mobileBrowser(request):
    """
    Mobile device detection.
    """

    mobile_browser = False
    ua = request.META['HTTP_USER_AGENT'].lower()

    for i in mobiles_uas:
        if i in ua:
            mobile_browser = True
        else:
            for hint in mobile_ua_hints:
                if request.META['HTTP_USER_AGENT'].find(hint) > 0:
                    mobile_browser = True

    return mobile_browser


#####################################################
#                                                   #
#       Utils Called By Context Generators          #
#                                                   #
#####################################################

def get_completes_in_prev_session(user):
    try:
        prev_session = Session.objects.filter(user=user).latest()
        completes = Completed_Route.objects.filter(session=prev_session)
    except:
        completes = None
    return completes

def get_wall_from_slug(wall_slug):
    try:
        wall = Wall.objects.get(wall_slug=wall_slug)
    except:
        raise Http404
    return wall

def get_wall_slug_from_route_id(route_id):
    wall_slug = Wall.objects.get(route=route_id).wall_slug
    return wall_slug

def get_gym_from_slug(gym_slug):
    try:
        gym = Gym.objects.get(gym_slug=gym_slug)
    except:
        raise Http404
    return gym

def add_completed_route(request):
    """
    Check age of previous user session.
    If older than 3 hours, create a new session and save both.
    Otherwise, update old session endtime and save both.
    """
    user = request.user
    route = Route.objects.get(id=request.REQUEST['route_id'])
    now = datetime.now()

    if not Session.objects.filter(user=user):
        new_session_obj = Session(user=user,
                                  start_time=now,
                                  end_time=now + timedelta(minutes=5))
        new_session_obj.save()
        comp_route_obj = Completed_Route(climber=user,
                                         route=route,
                                         session=new_session_obj)
    else:
        diff = timedelta(hours=3)
        prior_session_obj = Session.objects.filter(user=user).latest()
        prior_end_time = prior_session_obj.end_time

        if now - diff < prior_end_time:
            prior_session_obj.end_time = now + timedelta(minutes=5)
            prior_session_obj.save()
            comp_route_obj = Completed_Route(climber=user,
                                             route=route,
                                             session=prior_session_obj)
        else:
            new_session_obj = Session(user=user,
                                      start_time=now,
                                      end_time=now + timedelta(minutes=5))
            new_session_obj.save()
            comp_route_obj = Completed_Route(climber=user,
                                             route=route,
                                             session=new_session_obj)

    comp_route_obj.save()
    return

def get_gym_list():
    gym_list = Gym.objects.all()
    return gym_list

def get_lists_for_gym(user, gym):
    wall_list = Wall.objects.filter(gym=gym.id)
    route_list = Route.objects.filter(gym=gym.id,
                                      is_avail_status=True).order_by('wall', 'difficulty')

    route_list, climb_count = append_last_climbed(user, route_list)
    return wall_list, route_list, climb_count

def get_list_for_wall(user, wall):
    route_list = Route.objects.filter(wall=wall.id,
                                      is_avail_status=True).order_by('difficulty')

    route_list, climb_count = append_last_climbed(user, route_list)
    return route_list

def append_last_climbed(user, route_list):
    climb_count = 0
    for route in route_list:
        try:
            route.latest_completed_route = route.completed_route_set.filter(climber=user).latest('created').created
            climb_count += 1
        except:
            pass

    return route_list, climb_count

def get_last_route_for_user(user):
    try:
        com = Completed_Route.objects.filter(climber=user).order_by('-modified')[0]
        last_route = Route.objects.get(id=com.route.id)
    except:
        last_route = None

    return last_route

def get_map_for_gym(gym):
    # Static fields
    base = 'http://maps.google.com/maps/api/staticmap?'
    size = '290x170'
    markers = 'markers'
    sensor = 'false'

    # Dynamic fields
    address = gym.gym_address
    city = gym.gym_city
    state = gym.gym_state
    zip_code = gym.gym_zip
    location = ' '.join([address, city, state, zip_code])

    # Concatenate list
    params = urllib.urlencode({'size': size,
                               'markers': location,
                               'sensor': sensor})
    str_list = [base, params]

    return ''.join(str_list)
