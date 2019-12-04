# Generated by Django 2.2.7 on 2019-12-04 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askbot', '0014_populate_askbot_roles'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-last_edited_at', '-points']},
        ),
        migrations.AlterField(
            model_name='askwidget',
            name='include_text_field',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='emailfeedsetting',
            name='feed_type',
            field=models.CharField(choices=[('q_all', 'Entire forum'), ('q_ask', 'Questions that I asked'), ('q_ans', 'Questions that I answered'), ('q_noans', 'Unanswered questions'), ('q_sel', 'Individually selected questions'), ('m_and_c', 'Mentions and comment responses')], max_length=16),
        ),
        migrations.AlterField(
            model_name='postrevision',
            name='email_address',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='questionwidget',
            name='style',
            field=models.TextField(blank=True, default="\n@import url('http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:300,400,700');\nbody {\n    overflow: hidden;\n}\n\n#container {\n    width: 200px;\n    height: 350px;\n}\nul {\n    list-style: none;\n    padding: 5px;\n    margin: 5px;\n}\nli {\n    border-bottom: #CCC 1px solid;\n    padding-bottom: 5px;\n    padding-top: 5px;\n}\nli:last-child {\n    border: none;\n}\na {\n    text-decoration: none;\n    color: #464646;\n    font-family: 'Yanone Kaffeesatz', sans-serif;\n    font-size: 15px;\n}\n", verbose_name='css for the widget'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='primary_language',
            field=models.CharField(choices=[('en', 'English')], default='en', max_length=16),
        ),
    ]
