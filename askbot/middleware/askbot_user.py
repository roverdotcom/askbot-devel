"""Middleware that modifies the 'user' attribute of HttpRequest objects
coming into Askbot urls.

The 'user' is a SimpleLazyObject, which takes as the argument to its
__init__ a function that it can use to reliably find the User instance it
should look up. By default, this is auth.get_user. This middleware replaces
that SimpleLazyObject with one that instead uses get_askbot_user, defined
here.

This middleware is also responsible for backfilling AskbotUsers for existing
Rover users.
"""

from django.contrib.auth import get_user
from django.contrib.auth.models import User
from django.utils.functional import SimpleLazyObject
from askbot.models import AskbotUser


def get_askbot_user(request):
    """Call auth.get_user, and, if its return value is a User object,
    translate it into an AskbotUser object.
    """
    # Replace cached auth Users with AskbotUsers.
    if not hasattr(request, '_cached_user') or \
            isinstance(request._cached_user, User):
        user = get_user(request)
        if isinstance(user, User):
            user, created = AskbotUser.objects.get_or_create(user=user)
        request._cached_user = user
    return request._cached_user


class AskbotUserMiddleware(object):
    """Replace 'user' SimpleLazyObject of incoming requests with one that
    finds AskbotUsers instead of Users.

    Load after Django's AuthenticationMiddleware.
    """
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: get_askbot_user(request))
