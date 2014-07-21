from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


class AskbotUser(models.Model):
    """Custom user model which encapsulates askbot functionality.
    Replaces monkey-patched auth User model.
    """
    user = models.OneToOneField(User)

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
