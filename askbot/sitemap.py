from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from askbot.models import Post

class OverviewSitemap(Sitemap):
    changefreq = 'weekly'

    def items(self):
        return [
            ('askbot.views.readers.index', 0.6),
            ('askbot.views.readers.tags', 0.5),
            ('askbot.views.users.show_users', 0.5),
        ]

    def priority(self, item):
        return item[1]

    def location(self, item):
        return reverse(item[0])

class QuestionsSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.5

    def items(self):
        questions = Post.objects.get_questions()
        questions = questions.exclude(deleted=True)
        questions = questions.exclude(approved=False)
        return questions.select_related('thread__title',
                                        'thread__last_activity_at')

    def lastmod(self, obj):
        return obj.thread.last_activity_at

    def location(self, obj):
        return obj.get_absolute_url()
