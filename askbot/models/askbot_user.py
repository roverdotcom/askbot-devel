from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# class AskbotUserManager(models.Manager):
#     """Custom model manager for AskbotUser.
#     Performs left outer join with auth User to get User fields.
#     """
#     def get_query_set(self):
#         """Perform a left outer join to get auth_user attributes.

#         This method comes courtesy of Colin Copeland:
#         http://www.caktusgroup.com/blog/2009/09/28/custom-joins-with-djangos-queryjoin/
#         Note that this method relies on Django methods that are deprecated as
#         of Django 1.6: upgrading from Django 1.5.8 will break this method, and
#         make an outer join pretty much impossible without resorting to raw SQL,
#         which will require a substantial overhaul.

#         An outer join is employed here to keep AskbotUser as pluggable as
#         possible. Ideally, we want to return a queryset that contains the auth
#         user attributes, so that we don't have to modify all existing Askbot
#         ORM calls to query related models. We want the existing Askbot code,
#         which looks like this:

#         User.objects.filter(username='JoeSchmoe')

#         To not have to be manually changed to this:

#         User.objects.filter(user__username='JoeSchmoe')

#         Monkey-patching is evil.
#         """

#         # Get these fields from the auth_user table.
#         auth_user_selects = {
#             'username': 'auth_user.username',
#             'first_name': 'auth_user.first_name',
#             'last_name': 'auth_user.last_name',
#             'email': 'auth_user.email',
#             'password': 'auth_user.password',
#             'groups': 'auth_user.groups',
#             'user_permissions': 'auth_user.user_permissions',
#             'is_staff': 'auth_user.is_staff',
#             'is_active': 'auth_user.is_active',
#             'is_superuser': 'auth_user.is_superuser',
#             'last_login': 'auth_user.last_login',
#             'date_joined': 'auth_user.date_joined',
#         }

#         results = super(AskbotUserManager, self).get_query_set()
#         results.extra(
#             select=auth_user_selects,
#             where=["(AskbotUser.user_id = )"]
#         )


class AskbotUser(models.Model):
    """Custom user model which encapsulates askbot functionality.
    Replaces monkey-patched auth User model.
    """
    user = models.OneToOneField(User, related_name='askbot_user')

    # objects = AskbotUserManager()

    class Meta(object):
        app_label = 'askbot'

    def __init__(self, user, *args, **kwargs):
        """Create a new AskbotUser tied to an existing User."""
        self.user = user
        super(AskbotUser, self).__init__(*args, **kwargs)

    def __getattr__(self, name):
        """If the AskbotUser does not have some attribute, look for it on the
        AskbotUser's User object.
        """
        return getattr(self.user, name)

    def save(self, *args, **kwargs):
        """Save self.user prior to saving self."""
        self.user.save()
        super(AskbotUser, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_corresponding_askbot_user(sender, instance, created, **kwargs):
    """Create a new AskbotUser whenever a User is saved."""
    if created:
        new_user = AskbotUser(instance)
        new_user.save()
