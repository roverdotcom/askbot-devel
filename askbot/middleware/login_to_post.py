"""Middleware used to re-enable 'login/sign up to post' functionality
without having to tie it the login view or create a non-safe/non-idempotent
GET view.

This middleware should be active via URLMiddleware on the login view only.
It checks for the presence of a created AnonymousQuestion or AnonymousAnswer
in the session, and, if it finds one, redirects to it.
"""

from askbot.models import Post
from django.shortcuts import redirect


class LoginToPostMiddleware(object):
    """Redirect to a newly-posted question or answer, if posted anonymously."""
    def process_response(request, response):
        if request.method == 'POST':
            try:
                anon_post = \
                    Post.objects.get(id=request.session.get('anon_post', None))
                del request.session['anon_post']
                request.session.modified = True

            except KeyError, Post.DoesNotExist:
                pass

            else:
                return redirect(anon_post)

        return response
