# -*- coding: utf-8 -*-
"""
:synopsis: connector to standard Django admin interface

To make more models accessible in the Django admin interface, add more classes subclassing ``django.contrib.admin.Model``

Names of the classes must be like `SomeModelAdmin`, where `SomeModel` must
exactly match name of the model used in the project
"""
from django.contrib import admin
from django.core.urlresolvers import reverse_lazy
from askbot import models

class AnonymousQuestionAdmin(admin.ModelAdmin):
    """AnonymousQuestion admin class"""

class TagAdmin(admin.ModelAdmin):
    """Tag admin class"""

class VoteAdmin(admin.ModelAdmin):
    """  admin class"""

class FavoriteQuestionAdmin(admin.ModelAdmin):
    """  admin class"""

class PostRevisionAdmin(admin.ModelAdmin):
    """  admin class"""

class AwardAdmin(admin.ModelAdmin):
    """  admin class"""

class ReputeAdmin(admin.ModelAdmin):
    """  admin class"""

class ActivityAdmin(admin.ModelAdmin):
    """  admin class"""


class AskbotUserAdmin(admin.ModelAdmin):
    """AskbotUser admin class."""
    exclude = (
        'user',

        # This will try to populate a multiple selection widget with every
        # AskbotUser in the system. Something similar would be useful to
        # have on the admin page, though.
        'following',

        'bronze',
        'silver',
        'gold',
        'is_fake',
        'email_key',
    )

    readonly_fields = (
        'user_link',
        'person_link',
    )

    def user_link(self, obj):
        """Fake admin field displaying a link to this profile's 'User' object.
        """
        return '<a href="{}">View User in admin.</a>'.format(
            reverse_lazy('admin:auth_user_change', args=[obj.user.id])
        )

    def person_link(self, obj):
        """Fake admin field displaying a link to this profile's 'Person'
        object.
        """
        return '<a href="{}">View Person in admin.</a>'.format(
            reverse_lazy('admin:people_person_change', args=[obj.person.id])
        )

    user_link.allow_tags = True
    person_link.allow_tags = True

# We don't register any ModelAdmin's for askbot as they don't
# provide useful functionality
