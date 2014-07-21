from django.contrib.auth.models import User
from django.db import models


class AskbotUser(models.Model):
    """Custom user model which encapsulates askbot functionality.
    Replaces monkey-patched auth User model.
    """
    user = models.OneToOneField(User)

    class Meta(object):
        app_label = 'askbot'

    def __init__(self, *args, **kwargs):
        """Create and save underlying User before initializing AskbotUser."""
        # TO DO: resolve need for an existing User id. Delve into Askbot to
        # figure out how it creates its users.
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
