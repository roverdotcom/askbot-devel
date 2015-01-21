from askbot.utils import decorators
from askbot import const
from askbot import models
from askbot import mail
from django.utils import timezone
from django.utils.translation import string_concat
from django.utils.translation import ungettext
from django.utils.translation import ugettext as _
from django.template.loader import get_template
from django.conf import settings as django_settings
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_text
from django.template import RequestContext
from django.views.decorators import csrf
from django.utils.encoding import force_text
from django.core import exceptions
try:
    import json
except ImportError:
    from django.utils import simplejson as json

#some utility functions
def get_object(memo):
    content_object = memo.activity.content_object
    if isinstance(content_object, models.PostRevision):
        return content_object.post
    else:
        return content_object


def get_editors(memo_set, exclude=None):
        editors = set()
        for memo in memo_set:
            post = get_object(memo)
            editors.add(post.author)

        if exclude in editors:
            editors.remove(exclude)#make sure not to block yourself
        return editors

def concat_messages(message1, message2):
    if message1:
        message = string_concat(message1, ', ')
        return string_concat(message, message2)
    else:
        return message2


@csrf.csrf_exempt
@decorators.post_only
@decorators.ajax_only
def moderate_post_edits(request):
    if request.user.is_anonymous():
        raise exceptions.PermissionDenied()
    if not request.user.is_administrator_or_moderator():
        raise exceptions.PermissionDenied()

    post_data = json.loads(request.raw_post_data)
    #{'action': 'decline-with-reason', 'items': ['posts'], 'reason': 1, 'edit_ids': [827]}

    memo_set = models.ActivityAuditStatus.objects.filter(
                                        id__in=post_data['edit_ids']
                                    ).select_related('activity')
    result = {'message': ''}

    if post_data['action'] == 'decline-with-reason':
        num_posts = 0
        for memo in memo_set:
            post = get_object(memo)
            request.user.delete_post(post)
            reject_reason = models.PostFlagReason.objects.get(id=post_data['reason'])
            template = get_template('email/rejected_post.html')
            data = {
                    'post': post.html,
                    'reject_reason': reject_reason.details.html
                   }
            body_text = template.render(RequestContext(request, data))
            mail.send_mail(
                subject_line = _('your post was not accepted'),
                body_text = unicode(body_text),
                recipient_list = [post.author.email,]
            )
            num_posts += 1

        if num_posts:
            posts_message = ungettext('%d post deleted', '%d posts deleted', num_posts) % num_posts
            result['message'] = concat_messages(result['message'], posts_message)

    if post_data['action'] == 'approve':
        num_posts = 0
        if 'posts' in post_data['items']:
            for memo in memo_set:
                if memo.activity.activity_type == const.TYPE_ACTIVITY_MARK_OFFENSIVE:
                    #unflag the post
                    content_object = memo.activity.content_object
                    request.user.flag_post(content_object, cancel_all=True, force=True)
                    num_posts += 1
                else:
                    revision = memo.activity.content_object
                    if isinstance(revision, models.PostRevision):
                        request.user.approve_post_revision(revision)
                        num_posts += 1


        if 'users' in post_data['items']:
            editors = get_editors(memo_set)
            for editor in editors:
                editor.set_status('a')

            num_editors = len(editors)
            if num_editors:
                users_message = ungettext('%d user approved', '%d users approved', num_editors) % num_editors
                result['message'] = concat_messages(result['message'], users_message)
            
            #approve revisions by the authors
            revisions = models.PostRevision.objects.filter(author__in=editors)
            now = timezone.now()
            revisions.update(approved=True, approved_at=now, approved_by=request.user)
            ct = ContentType.objects.get_for_model(models.PostRevision)
            mod_activity_types = (
                const.TYPE_ACTIVITY_MARK_OFFENSIVE,
                const.TYPE_ACTIVITY_MODERATED_NEW_POST,
                const.TYPE_ACTIVITY_MODERATED_POST_EDIT
            )
            items = models.Activity.objects.filter(
                                        content_type=ct,
                                        object_id__in=revisions.values_list('id', flat=True),
                                        activity_type__in=mod_activity_types
                                    )
            num_posts = items.count()
            items.delete()

        if num_posts > 0:
            posts_message = ungettext('%d post approved', '%d posts approved', num_posts) % num_posts
            result['message'] = concat_messages(result['message'], posts_message)

    if 'users' in post_data['items'] and post_data['action'] == 'block':
        editors = get_editors(memo_set, exclude=request.user)
        num_posts = 0
        for editor in editors:
            editor.set_status('b')
            num_posts += request.user.delete_all_content_authored_by_user(editor)

        if num_posts:
            posts_message = ungettext('%d post deleted', '%d posts deleted', num_posts) % num_posts
            result['message'] = concat_messages(result['message'], posts_message)

        num_editors = len(editors)
        if num_editors:
            users_message = ungettext('%d user blocked', '%d users blocked', num_editors) % num_editors
            result['message'] = concat_messages(result['message'], users_message)

    moderate_ips = getattr(django_settings, 'ASKBOT_IP_MODERATION_ENABLED', False)
    if moderate_ips and 'ips' in post_data and post_data['action'] == 'block':
        for memo in memo_set:
            obj = memo.activity.content_object
            if isinstance(obj, models.PostRevision):
                ips.add(obj.ip_addr)

        #to make sure to not block the admin and 
        #in case REMOTE_ADDR is a proxy server - not
        #block access to the site
        ips.remove(request.META['REMOTE_ADDR'])

        from stopforumspam.models import Cache
        already_blocked = Cache.objects.filter(ip__in=ips)
        already_blocked.update(permanent=True)
        already_blocked_ips = already_blocked.values_list('ip', flat=True)
        ips = ips - set(already_blocked_ips)
        for ip in ips:
            cache = Cache(ip=ip, permanent=True)
            cache.save()

        num_ips = len(ips)
        if num_ips:
            ips_message = ungettext('%d ip blocked', '%d ips blocked', num_ips) % num_ips
            result['message'] = concat_messages(result['message'], ips_message)

    memo_set.delete()
    request.user.update_response_counts()
    if result['message']:
        result['message'] = force_text(result['message'])
    return result
