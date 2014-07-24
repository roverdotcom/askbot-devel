from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class AskbotUserManager(models.Manager):
    """Custom model manager for AskbotUser.
    Preprocesses ORM queries and adds 'user__' in order to query related the
    related auth User, where appropriate.

    Note that chaining of queryset methods is not supported:

    # YES
    AskbotUser.objects.all()

    # NO
    AskbotUser.objects.filter(username="something").filter(email="something)

    To achieve chaining, a custom QuerySet class will have to be defined for
    the AskbotUser.
    """
    def get_query_set(self):
        """
        """

        # Get these fields from the auth_user table.
        auth_user_selects = {
            'username': 'auth_user.username',
            'first_name': 'auth_user.first_name',
            'last_name': 'auth_user.last_name',
            'email': 'auth_user.email',
            'password': 'auth_user.password',
            'groups': 'auth_user.groups',
            'user_permissions': 'auth_user.user_permissions',
            'is_staff': 'auth_user.is_staff',
            'is_active': 'auth_user.is_active',
            'is_superuser': 'auth_user.is_superuser',
            'last_login': 'auth_user.last_login',
            'date_joined': 'auth_user.date_joined',
        }

        results = super(AskbotUserManager, self).get_query_set()
        results.extra(
            select=auth_user_selects,
            where=["(AskbotUser.user_id = )"]
        )


class AskbotUser(models.Model):
    """Custom user model which encapsulates askbot functionality.
    Replaces monkey-patched auth User model.
    """
    user = models.OneToOneField(User, related_name='askbot_user')

    objects = AskbotUserManager()

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
