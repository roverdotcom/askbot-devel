from django.core.management.base import BaseCommand
from django.utils import timezone

from askbot.models import Post
from askbot.models import Tag
from askbot.models import AskbotUser


class Command(BaseCommand):
    excluded_tags = ['sitter', 'support']

    def handle(self, *args, **options):
        questions = Post.objects.filter(
            post_type='question'
        ).exclude(thread__tags__name__in=self.excluded_tags)

        print 'Tagging {} questions with the tag "dogs"'.format(
            questions.count()
        )

        tag = Tag.objects.get(name='dogs')
        tag.status = Tag.STATUS_ACCEPTED
        tag.save()

        user = AskbotUser.objects.get(user__email='matt@rover.com')

        for question in questions:
            question.thread.add_tag(
                tag_name=tag.name,
                user=user,
                timestamp=timezone.now(),
                silent=True
            )

            question.thread.invalidate_cached_data()

            print u'Tagged question #{} "{}"'.format(
                question.pk,
                unicode(question)
            )
