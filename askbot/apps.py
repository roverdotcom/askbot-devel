from django.apps import AppConfig


class AskbotAppConfig(AppConfig):
    name = 'askbot'
    verbose_name = 'Super-awesome Q&A community app'

    def ready(self):
        # Load/register all the askbot settings
        from askbot.conf.settings_load import *
