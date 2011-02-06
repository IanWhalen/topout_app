from models import *
from django.http import Http404
from datetime import datetime, timedelta

#####################################################
#                                                   #
#            Primary Context Generators             #
#                                                   #
#####################################################

def get_context_for_mobile_user_home(request):
    last_route = get_last_route_for_user(request)
    c = {'user': request.user,
         'last_route': last_route}
    return c

def get_context_for_anon_home():
    route_list = Completed_Route.objects.order_by('created')[0:5]
    return route_list

def get_context_for_user_home(request):
    last_route = get_last_route_for_user(request.user)
    c = {'user': request.user,
         'last_route': last_route}
    return c

def get_context_for_gym_page(request, gym_slug):
    gym = get_gym_from_slug(gym_slug)

    try:
        combo_list, climb_count = create_route_lists(request.user, gym)
    except:
        combo_list, climb_count = create_route_lists(0, gym)

    c = {'gym': gym,
         'user': request.user,
         'combo_list': combo_list,
         'climb_count': climb_count}
    return c


#####################################################
#                                                   #
#            Mobile Phone Detection                 #
#                                                   #
#####################################################

mobiles_uas = [
    'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
    'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
    'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
    'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
    'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
    'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
    'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
    'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
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

def get_gym_from_slug(gym_slug):
    try:
        gym = Gym.objects.get(gym_slug=gym_slug)
    except Gym.DoesNotExist:
        raise Http404
    return gym

def add_completed_route(user, route):
    """
    Check age of previous user session.
    If older than 3 hours, create a new session and save both.
    Otherwise, update old session endtime and save both.
    """
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

def create_route_lists(user, gym):
    """
    Returns two values: an object list of all routes at gym and
    a count of all total routes climbed by signed-in user.
    """
    gym_list = Route.objects.filter(gym=gym.id,
                                    is_avail_status=True).order_by('difficulty')

    route_list = Route.objects.filter(completed_route__climber=user, gym=gym.id,
                                       is_avail_status=True)

    climb_count = route_list.count()

    combo_list = []
    for r in gym_list:
        try:
            com = Completed_Route.objects.filter(route=r, climber=user).latest('created')
        except Completed_Route.DoesNotExist:
            com = None
        combo_list.append((r, com))

    return combo_list, climb_count

def get_last_route_for_user(user):
    try:
        com = Completed_Route.objects.filter(climber=user).order_by('-modified')[0]
        last_route = Route.objects.get(id=com.route.id)
    except:
        last_route = None

    return last_route
