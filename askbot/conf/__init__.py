from askbot import const
import askbot

from askbot.conf.settings_wrapper import settings

from django.conf import settings as django_settings


def should_show_sort_by_relevance():
    """True if configuration support sorting
    questions by search relevance
    """
    return ('postgresql_psycopg2' in askbot.get_database_engine_name())


def get_tag_display_filter_strategy_choices():
    from askbot.conf import settings as askbot_settings
    if askbot_settings.SUBSCRIBED_TAG_SELECTOR_ENABLED:
        return const.TAG_DISPLAY_FILTER_STRATEGY_CHOICES
    else:
        return const.TAG_DISPLAY_FILTER_STRATEGY_MINIMAL_CHOICES


def get_tag_email_filter_strategy_choices():
    """returns the set of choices appropriate for the configuration"""
    from askbot.conf import settings as askbot_settings
    if askbot_settings.SUBSCRIBED_TAG_SELECTOR_ENABLED:
        return const.TAG_EMAIL_FILTER_ADVANCED_STRATEGY_CHOICES
    else:
        return const.TAG_EMAIL_FILTER_SIMPLE_STRATEGY_CHOICES
