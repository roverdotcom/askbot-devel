"""
This module records the site visits by the authenticated users

Included here is the ViewLogMiddleware
"""
from django.conf import settings
from django.utils import timezone
from askbot.models import signals


class ViewLogMiddleware(object):
    """
    ViewLogMiddleware sends the site_visited signal

    """
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.path.startswith('/' + settings.ASKBOT_URL):
            return

        #send the site_visited signal for the authenticated users
        if request.user.is_authenticated():
            signals.site_visited.send(None, #this signal has no sender
                user = request.user,
                timestamp = timezone.now()
            )
