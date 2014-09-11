"""
main url configuration file for the askbot site
"""
from django.conf import settings
try:
    from django.conf.urls import handler404
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import handler404
    from django.conf.urls.defaults import include, patterns, url

from askbot.views.error import internal_error as handler500
from django.conf import settings
from django.contrib import admin

from askbot.views import askbot_user

from urlmiddleware.conf import middleware, mpatterns
from askbot.middleware.anon_user import ConnectToSessionMessagesMiddleware
from askbot.middleware.askbot_user import AskbotUserMiddleware
from askbot.middleware.cancel import CancelActionMiddleware
from askbot.middleware.forum_mode import ForumModeMiddleware
from askbot.middleware.spaceless import SpacelessMiddleware
from askbot.middleware.view_log import ViewLogMiddleware
# Middleware classes unused in default Askbot installation.
# from askbot.middleware.locale import LocaleMiddleware
# from askbot.middleware.remote_ip import SetRemoteIPFromXForwardedFor

admin.autodiscover()

if getattr(settings, 'ASKBOT_MULTILINGUAL', False) == True:
    from django.conf.urls.i18n import i18n_patterns
    urlpatterns = i18n_patterns('',
        (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    )
else:
    urlpatterns = patterns('',
        (r'%s' % settings.ASKBOT_URL, include('askbot.urls'))
    )

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    #(r'^cache/', include('keyedcache.urls')), - broken views disable for now
    #(r'^settings/', include('askbot.deps.livesettings.urls')),
    # (r'^followit/', include('followit.urls')),
    url(
        r'^followit/follow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        askbot_user.FollowUser.as_view(),
        name='follow_object'
    ),
    url(
        r'^followit/unfollow/(?P<model_name>\w+)/(?P<object_id>\d+)/$',
        askbot_user.UnfollowUser.as_view(),
        name='unfollow_object'
    ),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^robots.txt$', include('robots.urls')),
    url( # TODO: replace with django.conf.urls.static ?
        r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:],
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT.replace('\\','/')},
    ),
)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
                    url(r'^rosetta/', include('rosetta.urls')),
                )

handler500 = 'askbot.views.error.internal_error'


# Add middleware.
middlewarepatterns = mpatterns(
    '',
    middleware(
        r'%s' % settings.ASKBOT_URL,
        ConnectToSessionMessagesMiddleware
    ),
    middleware(r'%s' % settings.ASKBOT_URL, AskbotUserMiddleware),
    middleware(r'%s' % settings.ASKBOT_URL, CancelActionMiddleware),
    middleware(r'%s' % settings.ASKBOT_URL, ForumModeMiddleware),
    middleware(r'%s' % settings.ASKBOT_URL, SpacelessMiddleware),
    middleware(r'%s' % settings.ASKBOT_URL, ViewLogMiddleware),
    # Middleware classes unused in default Askbot installation.
    # middleware(r'%s' % settings.ASKBOT_URL, LocaleMiddleware),
    # middleware(r'%s' % settings.ASKBOT_URL, SetRemoteIPFromXForwardedFor),
)
