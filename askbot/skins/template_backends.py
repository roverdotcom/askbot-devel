from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.template.backends.base import BaseEngine
from askbot.skins.loaders import Loader, get_skin, JinjaAppDirectoryLoader
from askbot.utils.loading import load_module
from django.utils.module_loading import import_string

# class made to respect the compressor calls
class FakeCompressEngine(object):
    def __init__(self):
        self.loaders = []

    # this signature is needed
    def get_template_loaders(self, template_loaders):
        return []


class AskbotSkinTemplates(BaseEngine):

    def __init__(self, params):
        junk = params.pop('OPTIONS') #we don't use this parameter
        super(AskbotSkinTemplates, self).__init__(params)
        self.loader = Loader(self)
        self.engine = FakeCompressEngine()

    def get_template(self, name):
        return Template(self.loader.load_template(name)[0])

    def from_string(self, template_code):
        skin = get_skin()
        return Template(skin.from_string(template_code))

CONTEXT_PROCESSORS = list()

class Template(object):

    def __init__(self, template):
        self.template = template

    @classmethod
    def load_context_processors(cls, paths):
        processors = list()
        for path in paths:
            processors.append(load_module(path))
        return processors

    @classmethod
    def get_engine_config(cls):
        t_settings = django_settings.TEMPLATES
        for config in t_settings:
            backend = 'askbot.skins.template_backends.AskbotSkinTemplates'
            if config['BACKEND'] == backend:
                return config
        raise ImproperlyConfigured('template backend %s is required', backend)


    @classmethod
    def get_extra_context_processor_paths(cls):
        conf = cls.get_engine_config()
        if 'OPTIONS' in conf and 'context_processors' in conf['OPTIONS']:
            return conf['OPTIONS']['context_processors']
        return tuple()

    @classmethod
    def get_context_processors(cls):
        global CONTEXT_PROCESSORS
        if len(CONTEXT_PROCESSORS) == 0:
            context_processor_paths = (
                'askbot.context.application_settings',
                'askbot.user_messages.context_processors.user_messages',#must be before auth
                'django.contrib.auth.context_processors.auth', #this is required for the admin app
                'django.core.context_processors.csrf', #necessary for csrf protection
                'askbot.deps.group_messaging.context.group_messaging_context',
            )
            extra_paths = cls.get_extra_context_processor_paths()
            for path in extra_paths:
                if path not in context_processor_paths:
                    context_processor_paths += (path,)

            CONTEXT_PROCESSORS = cls.load_context_processors(context_processor_paths)

        return CONTEXT_PROCESSORS

    @classmethod
    def update_context(cls, context, request):
        for processor in cls.get_context_processors():
            context.update(processor(request))
        return context

    def render(self, context=None, request=None):
        if context is None:
            context = {}

        if request is not None:
            context['request'] = request
            context = self.update_context(context, request)

        return self.template.render(context)
