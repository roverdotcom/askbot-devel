from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class AskbotUserManager(models.Manager):
    """Custom model manager for AskbotUser.
    Performs left join with auth User to get User fields.
    """
    def get_query_set(self):
        return self.raw(
            'SELECT * FROM askbot_askbotuser LEFT OUTER JOIN auth_user'
            'ON askbot_user.user_id = auth_user.id;'
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
