from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.sites.models import Site , RequestSite
from django.contrib.auth.views import login as django_login
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.html import escape 
from django import forms

import datetime, random, sys, os

from django.conf import settings

from gmapi import maps
from bikematchapp.forms import MapForm
from profiles.models import Profile


# import the logging library
import logging

logger = logging.getLogger(__name__)

def init_logging():
    stdoutHandler = logging.StreamHandler(sys.stdout)
    if len(logger.handlers) < 1:
        logger.addHandler(stdoutHandler)

init_logging()

@login_required
def index(request):
    error_message = ""
    try: 
        profile = request.user.get_profile()
    except:
        return redirect('/profiles/create')
        
    return render_to_response('bikematchapp/mapview.html', {
        'error_message': error_message,
    }, context_instance=RequestContext(request))

def mapview(request, template_name='bikematchapp/mapview.html'):
    gmap = maps.Map(opts={
        'center': maps.LatLng(34.122605,-118.309708), #USC is 34.0205N, 118.2856W 
        'mapTypeId': maps.MapTypeId.ROADMAP,
        #'size': maps.Size(800,600),
        'zoom': 11,
        'mapTypeControlOptions': {
             'style': maps.MapTypeControlStyle.DROPDOWN_MENU
        },
    })
    
    for profile in Profile.objects.all():
        if profile.location:
            
            if profile.profile_pic_small.url:
                image = os.path.join(profile.profile_pic_small_border.url) 
            else:
                image = os.path.join(settings.STATIC_URL, "images", "bike_blue.png")
                       
            marker = maps.Marker(opts={
                                     'map': gmap,
                                     'position': maps.LatLng(profile.location.latitude, profile.location.longitude),
                                     'icon' : image,
                                     'profile_username': profile.user.username
        
                                     })
            
            maps.event.addListener(marker, 'mouseover', 'myobj.markerOver')
            maps.event.addListener(marker, 'mouseout', 'myobj.markerOut')
            maps.event.addListener(marker, 'click', 'myobj.onClick')
            
            contentString = '<div class="row"><div class="span2"><img src="%s"/></div><div class="span2"><p><strong>%s</strong></p><p>%s</p></div></div>' % (escape(profile.profile_pic_med.url),escape(profile.name),escape(profile.about[:60] + ".."))
    
            info = maps.InfoWindow({
                                    'content': contentString,
                                    })
            info.open(gmap, marker)
    
    return render_to_response(
    template_name, {
        'form': MapForm(initial={'map': gmap})
    }, context_instance=RequestContext(request))
    

def root_index(request):
    return redirect('/') 

def resources(request):
    error_message = ""
   
    return render_to_response('bikematchapp/resources.html', {
        'error_message': error_message,
    }, context_instance=RequestContext(request))

