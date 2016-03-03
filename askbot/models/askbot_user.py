from django.contrib.auth.models import User as AuthUser
from django.contrib.auth.models import UserManager
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.db.models.query import QuerySet
from django.db.models import Q
from django.utils.functional import cached_property
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
                    self._prefix_user_fields(query): value
                    for query, value in kwargs.items()
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
        other Q objects with differing connectors) and insert 'user__' into
        field names, where appropriate.
        """
        for i, child in enumerate(q_obj.children):
            if isinstance(child, Q):
                self._traverse_Q(child)
            else:
                query, value = child
                q_obj.children[i] = (self._prefix_user_fields(query), value)

    def _prefix_user_fields(self, query):
        """Find single field lookups on AskbotUser or related field lookups
        that query through a related AskbotUser and prefix those fields with
        'user__'.
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
                # For some reason, get_field fails to find some fields that
                # get_field_by_name discovers.
                current_model = \
                    current_model._meta.get_field_by_name(field)[0].rel.to
            except (AttributeError, FieldDoesNotExist):
                # AttributeError will be raised when the field's 'rel'
                # attribute is None - it has no relation, so we're done.
                # FieldDoesNotExist will be raised if we reach an ORM operator
                # like lt or exact, which are not field names. These terms
                # appear at the end of the query, so we're done.
                pass

        return ''.join([descending, '__'.join(fields)])

    @cached_property
    def user_attributes(self):
        """
        Return a tuple of attributes on User objects that need 'user__'
        prefixed to their ORM query keyword arguments.
        """
        return tuple(
            attr for attr in AuthUser._meta.get_all_field_names() if attr != 'id')


class AskbotUserManager(PassThroughManager):
    """Create a custom PassThroughManager with create_user and
    create_superuser methods.
    """
    def get_query_set(self):
        return super(AskbotUserManager, self).get_queryset(). \
            select_related('user')

    def create_user(
            self,
            username,
            email=None,
            password=None,
            **extra_fields
    ):
        """Create a new User-AskbotUser pair. Return the AskbotUser.

        Note on implementation: inheriting from UserManager and calling

        super(AskbotUserManager, self).create_user

        won't work here because UserManager.create_user creates a self.model,
        which ends up being an AskbotUser. contrib.auth.get_user_model is
        subsituted here, instead.
        """
        now = timezone.now()

        new_user = get_user_model()(
            username=username,
            email=UserManager.normalize_email(email),
            is_staff=False,
            is_active=True,
            is_superuser=False,
            last_login=now,
            date_joined=now,
            **extra_fields
        )

        new_user.set_password(password)
        new_user.save()

        new_askbot_user = AskbotUser(user=new_user)

        # AskbotUser.save() performs a save() on User, as well. We had to
        # save new_user separately in order to create its id, so avoid
        # saving it again unecessarily by calling AskbotUser's superclass save.
        super(AskbotUser, new_askbot_user).save()

        return new_askbot_user

    def create_superuser(
        self,
        username,
        email=None,
        password=None,
        **extra_fields
    ):
        """Create a new AskbotUser as a superuser.

        See documentation for AskbotUserManager.create_user for
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
    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followed_by'
    )

    date_joined = models.DateTimeField(default=timezone.now)

    objects = AskbotUserManager.for_queryset_class(AskbotUserQuerySet)()

    class Meta:
        app_label = 'askbot'
        verbose_name = 'Rover Q&A Community Profile'
        verbose_name_plural = 'Rover Q&A Community Profiles'

    def __getattr__(self, name):
        """If the AskbotUser does not have some attribute, look for it on the
        AskbotUser's AuthUser object.

        For now, __getattr__ is querying only public attributes on its AuthUser
        - querying all attributes causes a max recursion depth exception.
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
            if (
                    name not in self._meta.get_all_field_names() and
                    name in get_user_model()._meta.get_all_field_names()):
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
        # don't end up with one saved when the other is invalid, but
        # AskbotUser cannot be full_cleaned, because many of its fields are
        # populated by pre_save handlers. Vexing.
        self.user.save()
        super(AskbotUser, self).save(*args, **kwargs)

    def get_followers(self):
        return self.followed_by.all()

    def get_followed_users(self):
        return self.following.all()

    def is_following(self, user):
        return user in self.following.all()

    def follow_user(self, user):
        """Follow the specified User. Returns True or False to indicate
        whether this is a new relationship (for compliance with Askbot).
        """
        if user in self.following.all():
            return True
        else:
            self.following.add(user)
            return False

    def unfollow_user(self, user):
        self.following.remove(user)

    def get_full_name(self):
        """Return first name and last initial, separated by a space."""
        name = ''
        if self.user.first_name:
            name = self.user.first_name

        if self.user.last_name:
            name = u'{} {}.'.format(name, self.user.last_name[0])

        return name

    def get_default_avatar_url(self, size=48):
        """Return Rover image url."""
        if size <= 200:
            return self.user.person.get_small_image_url()
        elif size <= 450:
            return self.user.person.get_medium_image_url()
        else:
            return self.user.person.get_large_uncropped_image_url()

    def get_leaderboard_position(self):
        """Get this user's position on the leaderboard."""

        if any([
            self.status in ['d', 'm', 'b'],
            self.is_staff,
            self.is_superuser
        ]):
            return 'N/A'

        return AskbotUser.objects.exclude(
            Q(status__in=['d', 'm', 'b']) |
            Q(is_staff=True) |
            Q(is_superuser=True)
        ).filter(
            Q(reputation__gt=self.reputation) |
            Q(reputation=self.reputation, last_seen__lt=self.last_seen)
        ).count() + 1
