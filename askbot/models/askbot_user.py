from django.contrib.auth.models import User
# Import UserManager so we can access the normalize_email classmethod.
from django.contrib.auth.models import UserManager
from django.utils import timezone
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
            return self._decorate_Q_and_kwargs_preprocessor(name)
        elif name in queryset_args_methods:
            return self._decorate_args_preprocessor(name)
        elif name in queryset_field_methods:
            return self._decorate_field_preprocessor(name)
        else:
            return super(AskbotUserQuerySet, self).__getattribute__(name)

    def _decorate_Q_and_kwargs_preprocessor(self, name):
        """Decorate an instance of _preprocess_Q_and_kwargs with the method
        name it should call, then return the resulting callable.
        """
        def _preprocess_kwargs(*args, **kwargs):
            """Return results of method 'name' with processed arguments
            *args and **kwargs, where **kwargs and 'children' of Q objects
            in *args have been prefixed with 'user__', where appropriate.
            """
            for q in args:
                for i in range(len(q.children)):
                    query, param = q.children[i]
                    if query.split('__')[0] in self.user_attributes:
                        q.children[i] = ('user__%s' % query, param)

            # Keep a list of keys to modify, as we can't modify the dict
            # while looping over it.
            to_modify = []
            for key in kwargs.keys():
                if key.split('__')[0] in self.user_attributes:
                    to_modify.append(key)

            for key in to_modify:
                kwargs['user__%s' % key] = kwargs[key]
                del kwargs[key]

            # Use the superclass method here to avoid another call to
            # __getattribute__ - infinite recursion.
            return getattr(
                super(AskbotUserQuerySet, self),
                name
            )(*args, **kwargs)

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
            # Build a new args tuple. Occasionally this gets passed in as
            # a tuple, so it can't reliably be modified in place.
            new_args = ()
            for arg in args:
                if arg.split('__')[0] in self.user_attributes:
                    new_args += 'user__%s' % (arg,)
                elif arg[0] == '-' and \
                        arg[1:].split('__')[0] in self.user_attributes:
                    new_args += ('-user__%s' % arg[1:],)
                else:
                    new_args += (arg,)

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
            if field.split('__')[0] in self.user_attributes:
                field = 'user__%s' % field

            # Use the superclass method here to avoid another call to
            # __getattribute__ - infinite recursion.
            return getattr(super(AskbotUserQuerySet, self), name)(*args)

        return _preprocess_field


class AskbotUserPassThroughManager(PassThroughManager):
    """Create a custom PassThroughManager with create_user and
    create_superuser.
    """
    def create_user(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        """Create a new User and return the AskbotUser created in post_save.

        Note on implementation: inheriting from UserManager and calling

        super(AskbotUserPassThroughManager, self).create_user

        won't work here because UserManager.create_user creates a self.model,
        which ends up being an AskbotUser. As a side effect, this method will
        break if a custom AUTH_USER_MODEL is defined, because it will always
        create a standard contrib.auth User. This method is basically a copy-
        pasted version of UserManager.create_user with self.model replaced.
        """
        now = timezone.now()

        email = UserManager.normalize_email(email)

        new_user = User(
            username=username,
            email=email,
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        new_user.set_password(password)

        new_user.save()

        # new_user's post_save signal creates an AskbotUser.
        return new_user.askbot_user

    def create_superuser(
        self,
        username,
        email=None,
        password=None,
        **extra_fields
    ):
        """Create a new AskbotUser as a superuser.

        See documentation for AskbotUserPassThroughManager.create_user for
        implementation notes.
        """
        new_askbot_user = self.create_user(
            username,
            email,
            password,
            **extra_fields
        )

        new_askbot_user.is_superuser = True
        new_askbot_user.is_staff = True
        new_askbot_user.save()

        return new_askbot_user


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
