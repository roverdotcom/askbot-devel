from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager


class AskbotUserQuerySet(QuerySet):
    """Custom queryset that automatically adds related object names to
    queries, where appropriate.

    So, a request for:
    AskbotUser.objects.filter(username='something')

    Will automatically be translated to:
    AskbotUser.objects.filter(user__username='something')

    in order to successfully tunnel through the one-to-one relationship
    while treating the one-to-one related model's fields as if they were
    part of this model.
    """

    # List of attributes on User objects that need 'user__' prefixed to
    # their ORM query keyword arguments.
    user_attributes = tuple(
        attr for attr in User._meta.get_all_field_names() if attr != 'id'
    )

    def __getattribute__(self, name):
        """Intercept calls to queryset methods that take field names or field
        lookups as arguments.
        """
        # UNSUPPORTED METHODS:
        # create
        # get_or_create
        # Aggregation functions - although these may or may not actually
        # need explicit support.

        # Lists of methods that need to be intercepted. These are the
        # Django 1.5 methods - some have changed in 1.6 and 1.7.

        # List of methods on QuerySet objects that take a list of field-
        # lookup format keyword arguments.
        queryset_kwargs_methods = (
            'filter',
            'exclude',
            # 'get',  # This method calls filter.
        )
        # Note that 'update' takes **kwargs but does not support related
        # field lookups.

        # List of methods on QuerySet objects that take a list of field
        # names as positional arguments.
        queryset_args_methods = (
            'order_by',
            'distinct',
            'values',
            'values_list',
            'select_related',
            'prefetch_related',
            'defer',
            'only',
        )

        # List of methods on QuerySet objects that take a single field
        # name as their first positional argument.
        queryset_field_methods = (
            'dates',
            'latest',
        )

        if name in queryset_kwargs_methods:
            return self._decorate_kwargs_preprocessor(name)
        elif name in queryset_args_methods:
            return self._decorate_args_preprocessor(name)
        elif name in queryset_field_methods:
            return self._decorate_field_preprocessor(name)
        else:
            return super(AskbotUserQuerySet, self).__getattribute__(name)

    def _decorate_kwargs_preprocessor(self, name):
        """Decorate an instance of _preprocess_kwargs with the method
        name it should call, then return the resulting callable.
        """
        def _preprocess_kwargs(**kwargs):
            """Return results of method 'name' with processed arguments
            **kwargs, where **kwargs have been prefixed with 'user__',
            where appropriate.
            """
            # Keep a list of keys to modify, as we can't modify the dict
            # while looping over it.
            to_modify = []
            for key in kwargs.keys():
                if key in self.user_attributes:
                    to_modify.append(key)

            for key in to_modify:
                kwargs['user__%s' % key] = kwargs[key]
                del kwargs[key]

            # Use the superclass method here to avoid another call to
            # __getattribute__ - infinite recursion.
            return getattr(super(AskbotUserQuerySet, self), name)(**kwargs)

        return _preprocess_kwargs

    def _decorate_args_preprocessor(self, name):
        """Decorate an instance of _preprocess_args with the method name
        it should call, then return the resulting callable.
        """
        def _preprocess_args(*args):
            """Return results of method 'name' with processed arguments
            *args, where *args have been prefixed with 'user__', where
            appropriate.
            """
            for i in range(len(args)):
                if args[i] in self.user_attributes:
                    args[i] = 'user__%s' % args[i]
                elif args[i][0] == '-' and args[i][1:] in self.user_attributes:
                    args[i] = '-user__%s' % args[i][1:]

            # Use the superclass method here to avoid another call to
            # __getattribute__ - infinite recursion.
            return getattr(super(AskbotUserQuerySet, self), name)(*args)

        return _preprocess_args

    def _decorate_field_preprocessor(self, name):
        """Decorate an instance of _preprocess_field with the method name
        it should call, then return the resulting callable.
        """
        def _preprocess_field(field, *args, **kwargs):
            """Return results of method 'name' with processed argument
            field and remaining arguments, where field has been prefixed
            with 'user__', where appropriate.
            """
            if field in self.user_attributes:
                field = 'user__%s' % field

            # Use the superclass method here to avoid another call to
            # __getattribute__ - infinite recursion.
            return getattr(super(AskbotUserQuerySet, self), name)(*args)

        return _preprocess_field


class AskbotUserPassThroughManager(UserManager, PassThroughManager):
    """Create a custom PassThroughManager with UserManager's special
    properties.
    """
    def create_user(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        """Call UserManager's create_user and return the the AskbotUser that
        gets tied to the resulting User object.
        """
        new_user = super(AskbotUserPassThroughManager, self).create_user(
            username,
            email=email,
            password=password,
            **extra_fields
        )

        # new_user's post_save signal creates an AskbotUser.
        return new_user.askbot_user

    def create_superuser(
        self,
        username,
        email=None,
        password=None,
        **extra_fields
    ):
        """Call UserManager's create_superuser and return the the AskbotUser
        that gets tied to the resulting User object.
        """
        new_user = super(AskbotUserPassThroughManager, self).create_superuser(
            username,
            email=email,
            password=password,
            **extra_fields
        )

        # new_user's post_save signal creates an AskbotUser.
        return new_user.askbot_user


class AskbotUser(models.Model):
    """Custom user model which encapsulates askbot functionality.
    Replaces monkey-patched auth User model.
    """
    user = models.OneToOneField(User, related_name='askbot_user')

    objects = AskbotUserPassThroughManager.for_queryset_class(
        AskbotUserQuerySet
    )()

    class Meta(object):
        app_label = 'askbot'

    def __getattr__(self, name):
        """If the AskbotUser does not have some attribute, look for it on the
        AskbotUser's User object.

        For now, __getattr__ is querying only public attributes on its user -
        querying all attributes causes maximum recursion depth to be exceeded,
        as the two __getattr__s bounce back and forth forver. If this proves
        problematic, __getattr__ may need to keep a list of attributes that
        it's allowed to query on the User.
        """
        try:
            return super(AskbotUser, self).__getattr__(name)
        except AttributeError:
            if name[0] != '_' and hasattr(self.user, name):
                return getattr(self.user, name)
            else:
                raise AttributeError(
                    "Neither AskbotUser nor User has public attribute %s" % (
                        name
                    )
                )

    def save(self, *args, **kwargs):
        """Save self.user prior to saving self."""
        self.user.save()
        super(AskbotUser, self).save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_corresponding_askbot_user(sender, instance, created, **kwargs):
    """Create a new AskbotUser whenever a User is saved."""
    if created:
        new_askbot_user = AskbotUser()
        new_askbot_user.user = instance
        new_askbot_user.save()
