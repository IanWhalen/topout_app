from django.contrib import admin
from django.contrib.auth.models import User
from topout.models import Route, Completed_Route, Wall, Gym

class RouteAdmin(admin.ModelAdmin):
    list_display = ('primary_color', 'secondary_color',
                    'difficulty', 'wall', 'gym', 'route_setter',
                    'is_avail_status', 'created')
    list_filter = ('wall', 'is_avail_status', 'gym', 'difficulty')
    ordering = ('-created',)

class Completed_RouteAdmin(admin.ModelAdmin):
    pass

class WallAdmin(admin.ModelAdmin):
    list_display = ('wall_name', 'gym', 'created')
    prepopulated_field = {'wall_slug': ('wall_name',)}

class GymAdmin(admin.ModelAdmin):
    list_display = ('gym_name', 'url', 'created')
    prepopulated_fields = {'gym_slug': ('gym_name',)}

admin.site.register(Route, RouteAdmin)
admin.site.register(Completed_Route, Completed_RouteAdmin)
admin.site.register(Wall, WallAdmin)
admin.site.register(Gym, GymAdmin)
