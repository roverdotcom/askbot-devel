# -*- coding: utf-8 -*-
"""
:synopsis: connector to standard Django admin interface

To make more models accessible in the Django admin interface, add more classes subclassing ``django.contrib.admin.Model``

Names of the classes must be like `SomeModelAdmin`, where `SomeModel` must
exactly match name of the model used in the project
"""
from django.contrib import admin
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
        'last_seen',
    )

    def user_display(self):
        """Fake admin field displaying a link to this profile's 'User' object.
        """
        pass

    def person_display(self):
        """Fake admin field displaying a link to this profile's 'Person'
        object.
        """
        pass

    def last_seen_display(self):
        """Fake admin field displaying 'last_seen' date."""
        pass

admin.site.register(models.Post)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Vote, VoteAdmin)
admin.site.register(models.FavoriteQuestion, FavoriteQuestionAdmin)
admin.site.register(models.PostRevision, PostRevisionAdmin)
admin.site.register(models.Award, AwardAdmin)
admin.site.register(models.Repute, ReputeAdmin)
admin.site.register(models.Activity, ActivityAdmin)
admin.site.register(models.BulkTagSubscription)
admin.site.register(models.AskbotUser, AskbotUserAdmin)
