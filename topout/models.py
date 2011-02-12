from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from models_utils import *

##########################################
#                                        #
#          Hierarchy of objects          #
#                                        #
##########################################

class Gym(models.Model):
    gym_name = models.CharField(unique=True, max_length=50)
    gym_slug = models.SlugField()
    gym_address = models.CharField(max_length=50)
    gym_city = models.CharField(max_length=50)
    gym_state = models.CharField(max_length=20)
    gym_zip = models.CharField(max_length=20)
    url = models.URLField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def __unicode__(self):
        return u'%s' % (self.gym_name)

    def get_absolute_url(self):
        return u'/gyms/%s/' % (self.gym_slug)

    def save(self, *args, **kwargs):
        ''' On save, update time'''
        if not self.id:
            self.created = datetime.today()
        self.modified = datetime.today()
        super(Gym, self).save(*args, **kwargs)

    class Admin:
        pass

class Wall(models.Model):
    wall_name = models.CharField(unique=True, max_length=50)
    wall_slug= models.SlugField()
    gym = models.ForeignKey(Gym)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def __unicode__(self):
        return u'%s' % (self.wall_name)

    def save(self, *args, **kwargs):
        ''' On save, update time'''
        if not self.id:
            self.created = datetime.today()
        self.modified = datetime.today()
        super(Wall, self).save(*args, **kwargs)

    class Admin:
        pass

class Route(models.Model):
    primary_color = models.CharField(max_length=7, choices=COLOR_CHOICES)
    secondary_color = models.CharField(max_length=7, choices=COLOR_CHOICES, blank=True)
    difficulty = models.CharField(max_length=5, choices=DIFFICULTY_CHOICES)
    wall = models.ForeignKey(Wall)
    gym = models.ForeignKey(Gym)
    route_setter = models.CharField(max_length=20, blank=True)
    is_avail_status = models.BooleanField(default=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)
    closed = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        if not self.secondary_color:
            return u'%s' % self.get_primary_color_display()
        else:
            return u'%s and %s' % (self.get_primary_color_display(),
                                   self.get_secondary_color_display())

    def save(self, *args, **kwargs):
        ''' On save, update time '''
        if not self.id:
            self.created = datetime.today()
        self.modified = datetime.today()
        if not (self.closed and self.is_avail_status):
            self.closed = datetime.today()
        super(Route, self).save(*args, **kwargs)

    class Admin:
        pass

class Session(models.Model):
    user = models.ForeignKey(User)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def __unicode__(self):
        return u'%s, %s - %s' % (self.user, self.start_time, self.end_time)

    def save(self, *args, **kwargs):
        '''On save, update time'''
        if not self.id:
            self.created = datetime.today()
        self.modified = datetime.today()
        super(Session, self).save(*args, **kwargs)

    class Meta:
        get_latest_by = 'created'

    class Admin:
        pass

class Completed_Route(models.Model):
    climber = models.ForeignKey(User)
    route = models.ForeignKey(Route)
    session = models.ForeignKey(Session)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    def __unicode__(self):
        return u'%s - %s' % (self.climber, self.created)

    def save(self, *args, **kwargs):
        ''' On save, update time'''
        if not self.id:
            self.created = datetime.today()
        self.modified = datetime.today()
        super(Completed_Route, self).save(*args, **kwargs)

    class Admin:
        pass
