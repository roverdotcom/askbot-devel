# -*- coding: utf-8 -*-


from django.db import models, migrations
import askbot.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('askbot', '0010_populate_language_code_for_reps_20160108_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localizeduserprofile',
            name='is_claimed',
            field=models.BooleanField(default=False, help_text='True, if user selects this language', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localizeduserprofile',
            name='language_code',
            field=askbot.models.fields.LanguageCodeField(default='en', max_length=16, db_index=True, choices=[('en', 'English'), ('de', 'Deutsch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='localizeduserprofile',
            name='reputation',
            field=models.PositiveIntegerField(default=0, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='primary_language',
            field=models.CharField(default='en', max_length=16, choices=[('en', 'English'), ('de', 'Deutsch')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='reputation',
            field=models.PositiveIntegerField(default=1, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(default='w', max_length=2, db_index=True, choices=[('d', 'administrator'), ('m', 'moderator'), ('a', 'approved'), ('w', 'watched'), ('s', 'suspended'), ('b', 'blocked')]),
            preserve_default=True,
        ),
    ]
