from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.models import UserManager
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db.models.query import QuerySet
from django.db.models import Q
from model_utils.managers import PassThroughManager


class AskbotUserQuerySet(QuerySet):
    """Custom queryset that automatically adds related object names to
    queries, where appropriate.

    So, a request on AskbotUser for:
    AskbotUser.objects.filter(username='something')

    Will automatically be translated to:
    AskbotUser.objects.filter(user__username='something')

    And a request on Post for:
    Post.objects.filter(author__username='something')

    Will be translated to:
    Post.objects.filter(author__user__username='something')
    """

    # List of attributes on User objects that need 'user__' prefixed to
    # their ORM query keyword arguments.
    user_attributes = tuple(
        attr for attr in AuthUser._meta.get_all_field_names() if attr != 'id'
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
        def _preprocess_Q_and_kwargs(*args, **kwargs):
            """Return results of method 'name' with processed arguments
            *args and **kwargs, where **kwargs and 'children' of Q objects
            in *args have had 'user__' inserted, where appropriate.
            """
            for q_obj in args:
                self._traverse_Q(q_obj)

            return getattr(super(AskbotUserQuerySet, self), name)(
                *args,
                **{
                    self._prefix_user_fields(query): kwargs[query]
                    for query in kwargs.keys()
                }
            )

        return _preprocess_Q_and_kwargs

    def _decorate_args_preprocessor(self, name):
        """Decorate an instance of _preprocess_args with the method name
        it should call, then return the resulting callable.
        """
        def _preprocess_args(*args, **kwargs):
            """Return results of method 'name' with processed arguments
            *args, where *args have had 'user__' inserted, where appropriate.
            """
            return getattr(super(AskbotUserQuerySet, self), name)(
                *map(self._prefix_user_fields, args),
                **kwargs
            )

        return _preprocess_args

    def _decorate_field_preprocessor(self, name):
        """Decorate an instance of _preprocess_field with the method name
        it should call, then return the resulting callable.
        """
        def _preprocess_field(field, *args, **kwargs):
            """Return results of method 'name' with processed argument
            field and remaining arguments, where field has had 'user__'
            inserted, if appropriate.
            """
            return getattr(super(AskbotUserQuerySet, self), name)(
                self._prefix_user_fields(field),
                *args,
                **kwargs
            )

        return _preprocess_field

    def _traverse_Q(self, q_obj):
        """Recursively traverse a Q object (whose 'children' may contain
        other Q objects with differing connectors) and prefix 'user__' to
        field names, where appropriate.
        """
        for i in range(len(q_obj.children)):
            if isinstance(q_obj.children[i], Q):
                self._traverse_Q(q_obj.children[i])
            else:
                query, param = q_obj.children[i]
                if query.split('__')[0] in self.user_attributes:
                    q_obj.children[i] = ('user__%s' % query, param)

    def _prefix_user_fields(self, query):
        """Find single field lookups on AskbotUser or related field lookups
        that query through a related AskbotUser.
        """
        if query[0] == '-':
            descending = '-'
            query = query[1:]
        else:
            descending = ''

        fields = query.split('__')

        current_model = self.model

        for i, field in enumerate(fields):
            if current_model is AskbotUser and field in self.user_attributes:
                fields[i] = 'user__%s' % field
                current_model = current_model._meta.get_field('user').rel.to

            try:
                current_model = current_model._meta.get_field(field).rel.to
            except AttributeError:
                pass

        return ''.join([descending, '__'.join(fields)])


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
        which ends up being an AskbotUser. contrib.auth.get_user_model is
        subsituted here, instead.
        """
        now = timezone.now()
        email = UserManager.normalize_email(email)

        user_model = get_user_model()

        new_user = user_model(
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
    user = models.OneToOneField(AuthUser, related_name='askbot_user')

    objects = AskbotUserPassThroughManager.for_queryset_class(
        AskbotUserQuerySet
    )()

    class Meta(object):
        app_label = 'askbot'

    def __getattr__(self, name):
        """If the AskbotUser does not have some attribute, look for it on the
        AskbotUser's AuthUser object.

        For now, __getattr__ is querying only public attributes on its User -
        querying all attributes causes a max recursion depth exception.
        If this proves problematic, __getattr__ may need to keep a list of
        attributes that it's allowed to query on the User.
        """
        try:
            if name[0] != '_':
                return getattr(self.user, name)

        except AttributeError:
            raise AttributeError(
                "Neither '%s' object nor '%s' object have public attribute"
                " '%s'" % (
                    self.__class__.__name__,
                    self.user.__class__.__name__,
                    name
                )
            )

        raise AttributeError(
            "'%s' object has no attribute '%s'" % (
                self.__class__.__name__,
                name
            )
        )

    def __setattr__(self, name, value):
        """If the attribute being set exists on the AskbotUser's AuthUser
        object, set it there, not here.

        Only allow setting of model fields on the underlying AuthUser.
        """
        # try-except to catch attempts to access self.user before it has been
        # assigned (during AskbotUser instantiation).
        try:
            if name != u'id' and \
                    name in get_user_model()._meta.get_all_field_names():
                setattr(self.user, name, value)
            else:
                super(AskbotUser, self).__setattr__(name, value)

        except AuthUser.DoesNotExist:
            super(AskbotUser, self).__setattr__(name, value)

    def __unicode__(self):
        try:
            return u'AskbotUser related to %s' % self.user.__unicode__()

        except AuthUser.DoesNotExist:
            return u'AskbotUser with no related User'

    def save(self, *args, **kwargs):
        """Save self.user prior to saving self."""
        # It would make sense to validate these with full_clean, so that we
        # don't end up with one saved when the other is invalid - but
        # AskbotUser cannot be full_cleaned, because many of its fields are
        # populated by pre_save and post_save handlers. Vexing.
        self.user.save()
        super(AskbotUser, self).save(*args, **kwargs)


class AskbotUserRelatedModel(models.Model):
    """Abstract base class for models that have relations to AskbotUser."""
    # TO DO: When we reach the point where AskbotUser is getting toggled on and
    # off by a setting, this class will need to determine whether or not to
    # attach a PassThroughManager to itself (because it won't be necessary when
    # AskbotUser is not being used).

    objects = PassThroughManager.for_queryset_class(AskbotUserQuerySet)()

    class Meta(object):
        abstract = True


@receiver(post_save, sender=AuthUser)
def create_corresponding_askbot_user(sender, instance, created, **kwargs):
    """Create a new AskbotUser whenever an AuthUser is saved."""
    if created:
        new_askbot_user = AskbotUser()
        new_askbot_user.user = instance

        # Avoid another set of user save signals being emitted.
        super(AskbotUser, new_askbot_user).save()
