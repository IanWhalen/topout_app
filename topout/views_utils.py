from models import *

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

def get_data_for_mobile_user_home(request):
    user = request.user
    completions = Completed_Route.objects.filter(climber=user.id).order_by('-modified')
    try:
        last_completion = completions[0]
        last_route = Route.objects.get(id=last_completion.route.id)
    except:
        last_route = None

    return last_route

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

def get_data_for_gym_page(request, gym_slug):
    try:
        g = Gym.objects.get(gym_slug=gym_slug)
    except Gym.DoesNotExist:
        raise Http404

    try:
        gym_list, climber_list = create_route_lists(request.user, g)
    except:
        gym_list, climber_list = create_route_lists(0, g)

    c = {'g': g, 'user': request.user, 'gym_list': gym_list, \
         'climber_list': climber_list}
    return c
