from django.views.generic.base import View
from django.views.generic.list import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.utils import simplejson
from django.db.models import Q
from askbot.models import User


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


class Leaderboard(ListView):
    """Display users ordered by reputation."""
    model = User
    template_name = "leaderboard.html"
    context_object_name = "users"
    paginate_by = 10

    def get_queryset(self):
        """Do not display admins/moderators on the leaderboard."""
        # 'd' means administrator, which implies is_staff and is_superuser -
        # but the reverse relation, is_staff and is_superuser -> 'd', doesn't
        # hold for some reason. 'm' is moderator, which is separate from
        # is_staff and is_superuser.
        # 'b' is a blocked user - these should also not display on the
        # leaderboard.
        return User.objects.exclude(
            Q(status__in=['d', 'm', 'b']) | Q(is_staff=True, is_superuser=True)
        ).order_by('-reputation')
