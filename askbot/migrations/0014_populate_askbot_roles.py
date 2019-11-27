# -*- coding: utf-8 -*-


from django.db import migrations, models
from askbot.utils.console import ProgressBar

MOD_ROLES = ('recv_feedback',
             'recv_mod_alerts')

ADMIN_ROLES = ('terminate_accounts',
               'download_user_data')

def populate_askbot_roles(apps, schema_editor):
    Role = apps.get_model('askbot', 'Role')
    UserProfile = apps.get_model('askbot', 'UserProfile')
    User = apps.get_model('auth', "User")
    profiles = UserProfile.objects.filter(status__in=('m', 'd'))
    count = profiles.count()
    message = 'Assigning roles {} to the admins and the moderators'
    message = message.format(', '.join(MOD_ROLES + ADMIN_ROLES))
    for profile in ProgressBar(profiles.iterator(), count, message):
        user = User.objects.get(askbot_profile__auth_user_ptr=profile.pk)

        if profile.status == 'd':
            for role in ADMIN_ROLES + MOD_ROLES:
                Role.objects.create(user=user, role=role)
        else:
            for role in MOD_ROLES:
                Role.objects.create(user=user, role=role)


class Migration(migrations.Migration):

    dependencies = [
        ('askbot', '0013_auto_20181013_1857'),
    ]

    operations = [
        migrations.RunPython(populate_askbot_roles)
    ]
