from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils import simplejson
from django.shortcuts import redirect
from askbot.models import User
from askbot.models import Post


class FollowUser(View):
    """Allow AskbotUsers to follow other AskbotUsers."""
    def post(self, request, object_id=None, **kwargs):
        try:
            user = User.objects.get(id=object_id)
            if request.user.follow_user(user):
                response_content = {'status': 'success'}
            else:
                response_content = {'status': 'noop'}

        # Forgive me! This is what Askbot expects!
        except Exception, e:
            response_content = {
                'status': 'error',
                'error_message': unicode(e),
            }

        return HttpResponse(
            simplejson.dumps(response_content),
            content_type='application/json'
        )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FollowUser, self).dispatch(*args, **kwargs)


class UnfollowUser(View):
    """Allow AskbotUsers to unfollow followed AskbotUsers."""
    def post(self, request, object_id=None, **kwargs):
        try:
            user = User.objects.get(id=object_id)
            request.user.unfollow_user(user)
            response_content = {'status': 'success'}

        except Exception, e:
            response_content = {
                'status': 'error',
                'error_message': unicode(e),
            }

        return HttpResponse(
            simplejson.dumps(response_content),
            content_type='application/json'
        )

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(UnfollowUser, self).dispatch(*args, **kwargs)


class MostRecentQuestion(View):
    """Redirects to the most recent question posted by the given user.

    Fails through to the list view, and can be directed to fail through
    to the list view via a GET parameter if a question wasn't just posted
    anonymously.
    """

    def get(self, request, id=None, **kwargs):
        if request.GET.get('anon_only', False):
            try:
                question = Post.objects.get(
                    id=request.session.get('anon_question', None),
                    author__id=id,
                )
            except Post.DoesNotExist:
                return redirect('askbot-index')
            else:
                return redirect(question)

        else:
            questions = Post.objects.filter(
                author__id=id,
                post_type='question'
            ).order_by('-added_at')

            if questions:
                return redirect(questions[0])
            else:
                return redirect('askbot-index')


class MostRecentAnswer(View):
    """Redirects to the most recent answer posted by the given user.

    Fails through to the list view, and can be directed to fail through
    to the list view via a GET parameter if an answer wasn't just posted
    anonymously.
    """

    def get(self, request, id=None, **kwargs):
        if request.GET.get('anon_only', False):
            try:
                answer = Post.objects.get(
                    id=request.session.get('anon_answer', None),
                    author__id=id,
                )
            except Post.DoesNotExist:
                return redirect('askbot-index')
            else:
                return redirect(answer)

        else:
            answers = Post.objects.filter(
                author__id=id,
                post_type='answer'
            ).order_by('-added_at')

            if answers:
                return redirect(answers[0])
            else:
                return redirect('askbot-index')
