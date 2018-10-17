from django.conf import settings
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from pinax.apps.account.openid_consumer import PinaxConsumer
from profiles.views import ProfileCreateView, ProfileUpdateView
from profiles.forms import EditProfileForm, CreateProfileForm

from bikematchapp.views import mapview, resources



handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "homepage.html",
    }, name="home"),
    url(r"^admin/invite_user/$", "pinax.apps.signup_codes.views.admin_invite_user", name="admin_invite_user"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^about/", include("about.urls")),
    url(r"^account/", include("pinax.apps.account.urls")),
    url(r"^openid/", include(PinaxConsumer().urls)),
    url(r"^profiles/edit/$", ProfileUpdateView.as_view(),dict(form_class=EditProfileForm, template_name="profiles/profile_edit.html"), name="profile_edit"),
    url(r"^profiles/editnoescape/$", ProfileUpdateView.as_view(),dict(form_class=EditProfileForm, template_name="profiles/profile_edit_noescape.html"), name="profile_edit_noescape"),
    url(r"^profiles/create/$", ProfileCreateView.as_view(), dict(form_class=CreateProfileForm), name="profile_create"),
    url(r"^profiles/", include("profiles.urls")),
    url(r"^notices/", include("notification.urls")),
    url(r"^announcements/", include("announcements.urls")),
    (r'^messages/', include('django_messages.urls')),
    url(r"^wall/", include("wall.urls")),
    url(r"^mapview/$", "bikematchapp.views.mapview", name="mapview"),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
)
    
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^site_media/media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
)
