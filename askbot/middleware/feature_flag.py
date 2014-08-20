"""Middleware that redirects non-staff requests to Askbot urls to the home
page if Askbot's feature flag is switched off.
"""
from gargoyle import gargoyle
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


class AskbotFeatureFlagMiddleware(object):
    """Redirect Askbot urls to root if the flag is disabled."""
    def process_request(request):
        if not gargoyle.is_active('askrover'):
            return HttpResponseRedirect(reverse('index'))
