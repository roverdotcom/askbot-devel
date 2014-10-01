# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AskbotUser'
        db.create_table(u'askbot_askbotuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='askbot_user', unique=True, to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='w', max_length=2)),
            ('is_fake', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_isvalid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_key', self.gf('django.db.models.fields.CharField')(max_length=32, null=True)),
            ('reputation', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('gravatar', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('avatar_type', self.gf('django.db.models.fields.CharField')(default='n', max_length=1)),
            ('gold', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('silver', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('bronze', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('questions_per_page', self.gf('django.db.models.fields.SmallIntegerField')(default=10)),
            ('last_seen', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('real_name', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('country', self.gf('django_countries.fields.CountryField')(max_length=2, blank=True)),
            ('show_country', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('about', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('interesting_tags', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ignored_tags', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('subscribed_tags', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('email_signature', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('show_marked_tags', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('email_tag_filter_strategy', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('display_tag_filter_strategy', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('new_response_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('seen_response_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('consecutive_days_visit_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('languages', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=128)),
            ('twitter_access_token', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
            ('twitter_handle', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('social_sharing_mode', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('askbot', ['AskbotUser'])

        # Adding M2M table for field following on 'AskbotUser'
        m2m_table_name = db.shorten_name(u'askbot_askbotuser_following')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_askbotuser', models.ForeignKey(orm['askbot.askbotuser'], null=False)),
            ('to_askbotuser', models.ForeignKey(orm['askbot.askbotuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_askbotuser_id', 'to_askbotuser_id'])

        # Adding model 'Tag'
        db.create_table(u'askbot_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_tags', to=orm['askbot.AskbotUser'])),
            ('language_code', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=16)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('used_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='deleted_tags', null=True, to=orm['askbot.AskbotUser'])),
            ('tag_wiki', self.gf('django.db.models.fields.related.OneToOneField')(related_name='described_tag', unique=True, null=True, to=orm['askbot.Post'])),
        ))
        db.send_create_signal('askbot', ['Tag'])

        # Adding unique constraint on 'Tag', fields ['name', 'language_code']
        db.create_unique(u'askbot_tag', ['name', 'language_code'])

        # Adding M2M table for field suggested_by on 'Tag'
        m2m_table_name = db.shorten_name(u'askbot_tag_suggested_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('tag', models.ForeignKey(orm['askbot.tag'], null=False)),
            ('askbotuser', models.ForeignKey(orm['askbot.askbotuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['tag_id', 'askbotuser_id'])

        # Adding model 'MarkedTag'
        db.create_table(u'askbot_markedtag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_selections', to=orm['askbot.Tag'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tag_selections', to=orm['askbot.AskbotUser'])),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('askbot', ['MarkedTag'])

        # Adding model 'TagSynonym'
        db.create_table(u'askbot_tagsynonym', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source_tag_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('target_tag_name', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owned_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tag_synonyms', to=orm['askbot.AskbotUser'])),
            ('auto_rename_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_auto_rename_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=16)),
        ))
        db.send_create_signal('askbot', ['TagSynonym'])

        # Adding model 'ActivityAuditStatus'
        db.create_table('askbot_activityauditstatus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Activity'])),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
        ))
        db.send_create_signal('askbot', ['ActivityAuditStatus'])

        # Adding unique constraint on 'ActivityAuditStatus', fields ['user', 'activity']
        db.create_unique('askbot_activityauditstatus', ['user_id', 'activity_id'])

        # Adding model 'Activity'
        db.create_table(u'askbot_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'])),
            ('activity_type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('active_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Post'], null=True)),
            ('is_auditted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('summary', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('askbot', ['Activity'])

        # Adding M2M table for field receiving_users on 'Activity'
        m2m_table_name = db.shorten_name(u'askbot_activity_receiving_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('activity', models.ForeignKey(orm['askbot.activity'], null=False)),
            ('askbotuser', models.ForeignKey(orm['askbot.askbotuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['activity_id', 'askbotuser_id'])

        # Adding model 'EmailFeedSetting'
        db.create_table(u'askbot_emailfeedsetting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subscriber', self.gf('django.db.models.fields.related.ForeignKey')(related_name='notification_subscriptions', to=orm['askbot.AskbotUser'])),
            ('feed_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('frequency', self.gf('django.db.models.fields.CharField')(default='n', max_length=8)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('reported_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('askbot', ['EmailFeedSetting'])

        # Adding unique constraint on 'EmailFeedSetting', fields ['subscriber', 'feed_type']
        db.create_unique(u'askbot_emailfeedsetting', ['subscriber_id', 'feed_type'])

        # Adding model 'GroupMembership'
        db.create_table(u'askbot_groupmembership', (
            (u'authusergroups_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.AuthUserGroups'], unique=True, primary_key=True)),
            ('level', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('askbot', ['GroupMembership'])

        # Adding model 'Group'
        db.create_table('askbot_group', (
            (u'group_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.Group'], unique=True, primary_key=True)),
            ('logo_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
            ('description', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='described_group', unique=True, null=True, to=orm['askbot.Post'])),
            ('moderate_email', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('moderate_answers_to_enquirers', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('openness', self.gf('django.db.models.fields.SmallIntegerField')(default=2)),
            ('preapproved_emails', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('preapproved_email_domains', self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True)),
            ('is_vip', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('read_only', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('askbot', ['Group'])

        # Adding model 'BulkTagSubscription'
        db.create_table(u'askbot_bulktagsubscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('askbot', ['BulkTagSubscription'])

        # Adding M2M table for field tags on 'BulkTagSubscription'
        m2m_table_name = db.shorten_name(u'askbot_bulktagsubscription_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bulktagsubscription', models.ForeignKey(orm['askbot.bulktagsubscription'], null=False)),
            ('tag', models.ForeignKey(orm['askbot.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bulktagsubscription_id', 'tag_id'])

        # Adding M2M table for field users on 'BulkTagSubscription'
        m2m_table_name = db.shorten_name(u'askbot_bulktagsubscription_users')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bulktagsubscription', models.ForeignKey(orm['askbot.bulktagsubscription'], null=False)),
            ('askbotuser', models.ForeignKey(orm['askbot.askbotuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bulktagsubscription_id', 'askbotuser_id'])

        # Adding M2M table for field groups on 'BulkTagSubscription'
        m2m_table_name = db.shorten_name(u'askbot_bulktagsubscription_groups')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('bulktagsubscription', models.ForeignKey(orm['askbot.bulktagsubscription'], null=False)),
            ('group', models.ForeignKey(orm['askbot.group'], null=False))
        ))
        db.create_unique(m2m_table_name, ['bulktagsubscription_id', 'group_id'])

        # Adding model 'ThreadToGroup'
        db.create_table('askbot_thread_groups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Thread'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Group'])),
            ('visibility', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
        ))
        db.send_create_signal('askbot', ['ThreadToGroup'])

        # Adding unique constraint on 'ThreadToGroup', fields ['thread', 'group']
        db.create_unique('askbot_thread_groups', ['thread_id', 'group_id'])

        # Adding model 'Thread'
        db.create_table(u'askbot_thread', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('tagnames', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('view_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('favourite_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('answer_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('last_activity_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('last_activity_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='unused_last_active_in_threads', to=orm['askbot.AskbotUser'])),
            ('language_code', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=16)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('closed_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'], null=True, blank=True)),
            ('closed_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('close_reason', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('accepted_answer', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['askbot.Post'])),
            ('answer_accepted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='score')),
        ))
        db.send_create_signal('askbot', ['Thread'])

        # Adding M2M table for field tags on 'Thread'
        m2m_table_name = db.shorten_name(u'askbot_thread_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thread', models.ForeignKey(orm['askbot.thread'], null=False)),
            ('tag', models.ForeignKey(orm['askbot.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thread_id', 'tag_id'])

        # Adding M2M table for field followed_by on 'Thread'
        m2m_table_name = db.shorten_name(u'askbot_thread_followed_by')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('thread', models.ForeignKey(orm['askbot.thread'], null=False)),
            ('askbotuser', models.ForeignKey(orm['askbot.askbotuser'], null=False))
        ))
        db.create_unique(m2m_table_name, ['thread_id', 'askbotuser_id'])

        # Adding model 'QuestionView'
        db.create_table(u'askbot_questionview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewed', to=orm['askbot.Post'])),
            ('who', self.gf('django.db.models.fields.related.ForeignKey')(related_name='question_views', to=orm['askbot.AskbotUser'])),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('askbot', ['QuestionView'])

        # Adding model 'FavoriteQuestion'
        db.create_table(u'askbot_favorite_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Thread'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_favorite_questions', to=orm['askbot.AskbotUser'])),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('askbot', ['FavoriteQuestion'])

        # Adding model 'DraftQuestion'
        db.create_table(u'askbot_draftquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300, null=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
            ('tagnames', self.gf('django.db.models.fields.CharField')(max_length=125, null=True)),
        ))
        db.send_create_signal('askbot', ['DraftQuestion'])

        # Adding model 'AnonymousQuestion'
        db.create_table(u'askbot_anonymousquestion', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('wiki', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('ip_addr', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'], null=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('tagnames', self.gf('django.db.models.fields.CharField')(max_length=125)),
            ('is_anonymous', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('askbot', ['AnonymousQuestion'])

        # Adding model 'PostToGroup'
        db.create_table('askbot_post_groups', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Post'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Group'])),
        ))
        db.send_create_signal('askbot', ['PostToGroup'])

        # Adding unique constraint on 'PostToGroup', fields ['post', 'group']
        db.create_unique('askbot_post_groups', ['post_id', 'group_id'])

        # Adding model 'Post'
        db.create_table('askbot_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post_type', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('old_question_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, unique=True, null=True, blank=True)),
            ('old_answer_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, unique=True, null=True, blank=True)),
            ('old_comment_id', self.gf('django.db.models.fields.PositiveIntegerField')(default=None, unique=True, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='comments', null=True, to=orm['askbot.Post'])),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='posts', null=True, blank=True, to=orm['askbot.Thread'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='posts', to=orm['askbot.AskbotUser'])),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('deleted_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('deleted_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='deleted_posts', null=True, to=orm['askbot.AskbotUser'])),
            ('wiki', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('wikified_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('locked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('locked_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='locked_posts', null=True, to=orm['askbot.AskbotUser'])),
            ('locked_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0, db_column='score')),
            ('vote_up_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('vote_down_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('offensive_flag_count', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('last_edited_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('last_edited_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='last_edited_posts', null=True, to=orm['askbot.AskbotUser'])),
            ('html', self.gf('django.db.models.fields.TextField')(null=True)),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(default='en-us', max_length=16)),
            ('summary', self.gf('django.db.models.fields.TextField')(null=True)),
            ('is_anonymous', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('askbot', ['Post'])

        # Adding model 'PostRevision'
        db.create_table(u'askbot_postrevision', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='revisions', null=True, to=orm['askbot.Post'])),
            ('revision', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='postrevisions', to=orm['askbot.AskbotUser'])),
            ('revised_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('summary', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('approved', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('approved_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'], null=True, blank=True)),
            ('approved_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('by_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('email_address', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=300, blank=True)),
            ('tagnames', self.gf('django.db.models.fields.CharField')(default='', max_length=125, blank=True)),
            ('is_anonymous', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ip_addr', self.gf('django.db.models.fields.IPAddressField')(default='0.0.0.0', max_length=15)),
        ))
        db.send_create_signal('askbot', ['PostRevision'])

        # Adding unique constraint on 'PostRevision', fields ['post', 'revision']
        db.create_unique(u'askbot_postrevision', ['post_id', 'revision'])

        # Adding model 'PostFlagReason'
        db.create_table(u'askbot_postflagreason', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('details', self.gf('django.db.models.fields.related.ForeignKey')(related_name='post_reject_reasons', to=orm['askbot.Post'])),
        ))
        db.send_create_signal('askbot', ['PostFlagReason'])

        # Adding model 'DraftAnswer'
        db.create_table(u'askbot_draftanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='draft_answers', to=orm['askbot.Thread'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='draft_answers', to=orm['askbot.AskbotUser'])),
            ('text', self.gf('django.db.models.fields.TextField')(null=True)),
        ))
        db.send_create_signal('askbot', ['DraftAnswer'])

        # Adding model 'AnonymousAnswer'
        db.create_table(u'askbot_anonymousanswer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('session_key', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('wiki', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('added_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('ip_addr', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'], null=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='anonymous_answers', to=orm['askbot.Post'])),
        ))
        db.send_create_signal('askbot', ['AnonymousAnswer'])

        # Adding model 'ReplyAddress'
        db.create_table('askbot_replyaddress', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='reply_addresses', null=True, to=orm['askbot.Post'])),
            ('reply_action', self.gf('django.db.models.fields.CharField')(default='auto_answer_or_comment', max_length=32)),
            ('response_post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='edit_addresses', null=True, to=orm['askbot.Post'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'])),
            ('allowed_from_email', self.gf('django.db.models.fields.EmailField')(max_length=150)),
            ('used_at', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True)),
        ))
        db.send_create_signal('askbot', ['ReplyAddress'])

        # Adding model 'Vote'
        db.create_table(u'askbot_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['askbot.AskbotUser'])),
            ('voted_post', self.gf('django.db.models.fields.related.ForeignKey')(related_name='votes', to=orm['askbot.Post'])),
            ('vote', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('voted_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('askbot', ['Vote'])

        # Adding unique constraint on 'Vote', fields ['user', 'voted_post']
        db.create_unique(u'askbot_vote', ['user_id', 'voted_post_id'])

        # Adding model 'BadgeData'
        db.create_table(u'askbot_badgedata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('awarded_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
        ))
        db.send_create_signal('askbot', ['BadgeData'])

        # Adding model 'Award'
        db.create_table(u'askbot_award', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='award_user', to=orm['askbot.AskbotUser'])),
            ('badge', self.gf('django.db.models.fields.related.ForeignKey')(related_name='award_badge', to=orm['askbot.BadgeData'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('awarded_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('notified', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('askbot', ['Award'])

        # Adding model 'Repute'
        db.create_table(u'askbot_repute', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.AskbotUser'])),
            ('positive', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('negative', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Post'], null=True, blank=True)),
            ('reputed_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('reputation_type', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=128, null=True)),
        ))
        db.send_create_signal('askbot', ['Repute'])

        # Adding model 'AskWidget'
        db.create_table(u'askbot_askwidget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Group'], null=True, blank=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Tag'], null=True, blank=True)),
            ('include_text_field', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('inner_style', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('outer_style', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('askbot', ['AskWidget'])

        # Adding model 'QuestionWidget'
        db.create_table(u'askbot_questionwidget', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('question_number', self.gf('django.db.models.fields.PositiveIntegerField')(default=7)),
            ('tagnames', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.Group'], null=True, blank=True)),
            ('search_query', self.gf('django.db.models.fields.CharField')(default='', max_length=50, null=True, blank=True)),
            ('order_by', self.gf('django.db.models.fields.CharField')(default='-added_at', max_length=18)),
            ('style', self.gf('django.db.models.fields.TextField')(default="\n@import url('http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:300,400,700');\nbody {\n    overflow: hidden;\n}\n\n#container {\n    width: 200px;\n    height: 350px;\n}\nul {\n    list-style: none;\n    padding: 5px;\n    margin: 5px;\n}\nli {\n    border-bottom: #CCC 1px solid;\n    padding-bottom: 5px;\n    padding-top: 5px;\n}\nli:last-child {\n    border: none;\n}\na {\n    text-decoration: none;\n    color: #464646;\n    font-family: 'Yanone Kaffeesatz', sans-serif;\n    font-size: 15px;\n}\n", blank=True)),
        ))
        db.send_create_signal('askbot', ['QuestionWidget'])

        # Adding model 'ImportRun'
        db.create_table(u'askbot_importrun', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('command', self.gf('django.db.models.fields.TextField')(default='')),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('askbot', ['ImportRun'])

        # Adding model 'ImportedObjectInfo'
        db.create_table(u'askbot_importedobjectinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('old_id', self.gf('django.db.models.fields.IntegerField')()),
            ('new_id', self.gf('django.db.models.fields.IntegerField')()),
            ('model', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('run', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['askbot.ImportRun'])),
            ('extra_info', self.gf('picklefield.fields.PickledObjectField')()),
        ))
        db.send_create_signal('askbot', ['ImportedObjectInfo'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['user', 'voted_post']
        db.delete_unique(u'askbot_vote', ['user_id', 'voted_post_id'])

        # Removing unique constraint on 'PostRevision', fields ['post', 'revision']
        db.delete_unique(u'askbot_postrevision', ['post_id', 'revision'])

        # Removing unique constraint on 'PostToGroup', fields ['post', 'group']
        db.delete_unique('askbot_post_groups', ['post_id', 'group_id'])

        # Removing unique constraint on 'ThreadToGroup', fields ['thread', 'group']
        db.delete_unique('askbot_thread_groups', ['thread_id', 'group_id'])

        # Removing unique constraint on 'EmailFeedSetting', fields ['subscriber', 'feed_type']
        db.delete_unique(u'askbot_emailfeedsetting', ['subscriber_id', 'feed_type'])

        # Removing unique constraint on 'ActivityAuditStatus', fields ['user', 'activity']
        db.delete_unique('askbot_activityauditstatus', ['user_id', 'activity_id'])

        # Removing unique constraint on 'Tag', fields ['name', 'language_code']
        db.delete_unique(u'askbot_tag', ['name', 'language_code'])

        # Deleting model 'AskbotUser'
        db.delete_table(u'askbot_askbotuser')

        # Removing M2M table for field following on 'AskbotUser'
        db.delete_table(db.shorten_name(u'askbot_askbotuser_following'))

        # Deleting model 'Tag'
        db.delete_table(u'askbot_tag')

        # Removing M2M table for field suggested_by on 'Tag'
        db.delete_table(db.shorten_name(u'askbot_tag_suggested_by'))

        # Deleting model 'MarkedTag'
        db.delete_table(u'askbot_markedtag')

        # Deleting model 'TagSynonym'
        db.delete_table(u'askbot_tagsynonym')

        # Deleting model 'ActivityAuditStatus'
        db.delete_table('askbot_activityauditstatus')

        # Deleting model 'Activity'
        db.delete_table(u'askbot_activity')

        # Removing M2M table for field receiving_users on 'Activity'
        db.delete_table(db.shorten_name(u'askbot_activity_receiving_users'))

        # Deleting model 'EmailFeedSetting'
        db.delete_table(u'askbot_emailfeedsetting')

        # Deleting model 'GroupMembership'
        db.delete_table(u'askbot_groupmembership')

        # Deleting model 'Group'
        db.delete_table('askbot_group')

        # Deleting model 'BulkTagSubscription'
        db.delete_table(u'askbot_bulktagsubscription')

        # Removing M2M table for field tags on 'BulkTagSubscription'
        db.delete_table(db.shorten_name(u'askbot_bulktagsubscription_tags'))

        # Removing M2M table for field users on 'BulkTagSubscription'
        db.delete_table(db.shorten_name(u'askbot_bulktagsubscription_users'))

        # Removing M2M table for field groups on 'BulkTagSubscription'
        db.delete_table(db.shorten_name(u'askbot_bulktagsubscription_groups'))

        # Deleting model 'ThreadToGroup'
        db.delete_table('askbot_thread_groups')

        # Deleting model 'Thread'
        db.delete_table(u'askbot_thread')

        # Removing M2M table for field tags on 'Thread'
        db.delete_table(db.shorten_name(u'askbot_thread_tags'))

        # Removing M2M table for field followed_by on 'Thread'
        db.delete_table(db.shorten_name(u'askbot_thread_followed_by'))

        # Deleting model 'QuestionView'
        db.delete_table(u'askbot_questionview')

        # Deleting model 'FavoriteQuestion'
        db.delete_table(u'askbot_favorite_question')

        # Deleting model 'DraftQuestion'
        db.delete_table(u'askbot_draftquestion')

        # Deleting model 'AnonymousQuestion'
        db.delete_table(u'askbot_anonymousquestion')

        # Deleting model 'PostToGroup'
        db.delete_table('askbot_post_groups')

        # Deleting model 'Post'
        db.delete_table('askbot_post')

        # Deleting model 'PostRevision'
        db.delete_table(u'askbot_postrevision')

        # Deleting model 'PostFlagReason'
        db.delete_table(u'askbot_postflagreason')

        # Deleting model 'DraftAnswer'
        db.delete_table(u'askbot_draftanswer')

        # Deleting model 'AnonymousAnswer'
        db.delete_table(u'askbot_anonymousanswer')

        # Deleting model 'ReplyAddress'
        db.delete_table('askbot_replyaddress')

        # Deleting model 'Vote'
        db.delete_table(u'askbot_vote')

        # Deleting model 'BadgeData'
        db.delete_table(u'askbot_badgedata')

        # Deleting model 'Award'
        db.delete_table(u'askbot_award')

        # Deleting model 'Repute'
        db.delete_table(u'askbot_repute')

        # Deleting model 'AskWidget'
        db.delete_table(u'askbot_askwidget')

        # Deleting model 'QuestionWidget'
        db.delete_table(u'askbot_questionwidget')

        # Deleting model 'ImportRun'
        db.delete_table(u'askbot_importrun')

        # Deleting model 'ImportedObjectInfo'
        db.delete_table(u'askbot_importedobjectinfo')


    models = {
        'askbot.activity': {
            'Meta': {'object_name': 'Activity'},
            'active_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'activity_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_auditted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Post']", 'null': 'True'}),
            'receiving_users': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'received_activity'", 'symmetrical': 'False', 'to': "orm['askbot.AskbotUser']"}),
            'recipients': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'incoming_activity'", 'symmetrical': 'False', 'through': "orm['askbot.ActivityAuditStatus']", 'to': "orm['askbot.AskbotUser']"}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.activityauditstatus': {
            'Meta': {'unique_together': "(('user', 'activity'),)", 'object_name': 'ActivityAuditStatus'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Activity']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.anonymousanswer': {
            'Meta': {'object_name': 'AnonymousAnswer'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'anonymous_answers'", 'to': "orm['askbot.Post']"}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'wiki': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'askbot.anonymousquestion': {
            'Meta': {'object_name': 'AnonymousQuestion'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session_key': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'wiki': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'askbot.askbotuser': {
            'Meta': {'object_name': 'AskbotUser'},
            'about': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'avatar_type': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '1'}),
            'bronze': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'consecutive_days_visit_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'display_tag_filter_strategy': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'email_isvalid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_key': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'email_signature': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_tag_filter_strategy': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followed_by'", 'symmetrical': 'False', 'to': "orm['askbot.AskbotUser']"}),
            'gold': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'gravatar': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ignored_tags': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'interesting_tags': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_fake': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'languages': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '128'}),
            'last_seen': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'new_response_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'questions_per_page': ('django.db.models.fields.SmallIntegerField', [], {'default': '10'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'reputation': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'seen_response_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'show_country': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'show_marked_tags': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'silver': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'social_sharing_mode': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'w'", 'max_length': '2'}),
            'subscribed_tags': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'twitter_access_token': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'twitter_handle': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'askbot_user'", 'unique': 'True', 'to': u"orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'askbot.askwidget': {
            'Meta': {'object_name': 'AskWidget'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'include_text_field': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'inner_style': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'outer_style': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Tag']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'askbot.award': {
            'Meta': {'object_name': 'Award'},
            'awarded_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'badge': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'award_badge'", 'to': "orm['askbot.BadgeData']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'award_user'", 'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.badgedata': {
            'Meta': {'ordering': "('slug',)", 'object_name': 'BadgeData'},
            'awarded_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'awarded_to': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'badges'", 'symmetrical': 'False', 'through': "orm['askbot.Award']", 'to': "orm['askbot.AskbotUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        'askbot.bulktagsubscription': {
            'Meta': {'ordering': "['-date_added']", 'object_name': 'BulkTagSubscription'},
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['askbot.Group']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['askbot.Tag']", 'symmetrical': 'False'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['askbot.AskbotUser']", 'symmetrical': 'False'})
        },
        'askbot.draftanswer': {
            'Meta': {'object_name': 'DraftAnswer'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'draft_answers'", 'to': "orm['askbot.AskbotUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'draft_answers'", 'to': "orm['askbot.Thread']"})
        },
        'askbot.draftquestion': {
            'Meta': {'object_name': 'DraftQuestion'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125', 'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True'})
        },
        'askbot.emailfeedsetting': {
            'Meta': {'unique_together': "(('subscriber', 'feed_type'),)", 'object_name': 'EmailFeedSetting'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'feed_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '8'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reported_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'notification_subscriptions'", 'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.favoritequestion': {
            'Meta': {'object_name': 'FavoriteQuestion', 'db_table': "u'askbot_favorite_question'"},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Thread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_favorite_questions'", 'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.group': {
            'Meta': {'object_name': 'Group', '_ormbases': [u'auth.Group']},
            'description': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'described_group'", 'unique': 'True', 'null': 'True', 'to': "orm['askbot.Post']"}),
            u'group_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True', 'primary_key': 'True'}),
            'is_vip': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'moderate_answers_to_enquirers': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'moderate_email': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'openness': ('django.db.models.fields.SmallIntegerField', [], {'default': '2'}),
            'preapproved_email_domains': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'preapproved_emails': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'read_only': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'askbot.groupmembership': {
            'Meta': {'object_name': 'GroupMembership', '_ormbases': ['auth.AuthUserGroups']},
            u'authusergroups_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.AuthUserGroups']", 'unique': 'True', 'primary_key': 'True'}),
            'level': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'askbot.importedobjectinfo': {
            'Meta': {'object_name': 'ImportedObjectInfo'},
            'extra_info': ('picklefield.fields.PickledObjectField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'new_id': ('django.db.models.fields.IntegerField', [], {}),
            'old_id': ('django.db.models.fields.IntegerField', [], {}),
            'run': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.ImportRun']"})
        },
        'askbot.importrun': {
            'Meta': {'object_name': 'ImportRun'},
            'command': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'askbot.markedtag': {
            'Meta': {'object_name': 'MarkedTag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_selections'", 'to': "orm['askbot.Tag']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tag_selections'", 'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.post': {
            'Meta': {'object_name': 'Post'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'posts'", 'to': "orm['askbot.AskbotUser']"}),
            'comment_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'deleted_posts'", 'null': 'True', 'to': "orm['askbot.AskbotUser']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'group_posts'", 'symmetrical': 'False', 'through': "orm['askbot.PostToGroup']", 'to': "orm['askbot.Group']"}),
            'html': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '16'}),
            'last_edited_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_edited_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_edited_posts'", 'null': 'True', 'to': "orm['askbot.AskbotUser']"}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'locked_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'locked_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'locked_posts'", 'null': 'True', 'to': "orm['askbot.AskbotUser']"}),
            'offensive_flag_count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'old_answer_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'old_comment_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'old_question_id': ('django.db.models.fields.PositiveIntegerField', [], {'default': 'None', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comments'", 'null': 'True', 'to': "orm['askbot.Post']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'score'"}),
            'post_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'posts'", 'null': 'True', 'blank': 'True', 'to': "orm['askbot.Thread']"}),
            'vote_down_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'vote_up_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'wiki': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'wikified_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'askbot.postflagreason': {
            'Meta': {'object_name': 'PostFlagReason'},
            'added_at': ('django.db.models.fields.DateTimeField', [], {}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']"}),
            'details': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'post_reject_reasons'", 'to': "orm['askbot.Post']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'askbot.postrevision': {
            'Meta': {'ordering': "('-revision',)", 'unique_together': "(('post', 'revision'),)", 'object_name': 'PostRevision'},
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'approved_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'approved_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']", 'null': 'True', 'blank': 'True'}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'postrevisions'", 'to': "orm['askbot.AskbotUser']"}),
            'by_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_address': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_addr': ('django.db.models.fields.IPAddressField', [], {'default': "'0.0.0.0'", 'max_length': '15'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'revisions'", 'null': 'True', 'to': "orm['askbot.Post']"}),
            'revised_at': ('django.db.models.fields.DateTimeField', [], {}),
            'revision': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'tagnames': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '125', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '300', 'blank': 'True'})
        },
        'askbot.posttogroup': {
            'Meta': {'unique_together': "(('post', 'group'),)", 'object_name': 'PostToGroup', 'db_table': "'askbot_post_groups'"},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Post']"})
        },
        'askbot.questionview': {
            'Meta': {'object_name': 'QuestionView'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewed'", 'to': "orm['askbot.Post']"}),
            'when': ('django.db.models.fields.DateTimeField', [], {}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_views'", 'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.questionwidget': {
            'Meta': {'object_name': 'QuestionWidget'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Group']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order_by': ('django.db.models.fields.CharField', [], {'default': "'-added_at'", 'max_length': '18'}),
            'question_number': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'search_query': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'style': ('django.db.models.fields.TextField', [], {'default': '"\\n@import url(\'http://fonts.googleapis.com/css?family=Yanone+Kaffeesatz:300,400,700\');\\nbody {\\n    overflow: hidden;\\n}\\n\\n#container {\\n    width: 200px;\\n    height: 350px;\\n}\\nul {\\n    list-style: none;\\n    padding: 5px;\\n    margin: 5px;\\n}\\nli {\\n    border-bottom: #CCC 1px solid;\\n    padding-bottom: 5px;\\n    padding-top: 5px;\\n}\\nli:last-child {\\n    border: none;\\n}\\na {\\n    text-decoration: none;\\n    color: #464646;\\n    font-family: \'Yanone Kaffeesatz\', sans-serif;\\n    font-size: 15px;\\n}\\n"', 'blank': 'True'}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'askbot.replyaddress': {
            'Meta': {'object_name': 'ReplyAddress'},
            'address': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'allowed_from_email': ('django.db.models.fields.EmailField', [], {'max_length': '150'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'reply_addresses'", 'null': 'True', 'to': "orm['askbot.Post']"}),
            'reply_action': ('django.db.models.fields.CharField', [], {'default': "'auto_answer_or_comment'", 'max_length': '32'}),
            'response_post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edit_addresses'", 'null': 'True', 'to': "orm['askbot.Post']"}),
            'used_at': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.repute': {
            'Meta': {'object_name': 'Repute'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'negative': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'positive': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Post']", 'null': 'True', 'blank': 'True'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'reputation_type': ('django.db.models.fields.SmallIntegerField', [], {}),
            'reputed_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']"})
        },
        'askbot.tag': {
            'Meta': {'ordering': "('-used_count', 'name')", 'unique_together': "(('name', 'language_code'),)", 'object_name': 'Tag'},
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_tags'", 'to': "orm['askbot.AskbotUser']"}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'deleted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deleted_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'deleted_tags'", 'null': 'True', 'to': "orm['askbot.AskbotUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '16'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'suggested_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'suggested_tags'", 'symmetrical': 'False', 'to': "orm['askbot.AskbotUser']"}),
            'tag_wiki': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'described_tag'", 'unique': 'True', 'null': 'True', 'to': "orm['askbot.Post']"}),
            'used_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'askbot.tagsynonym': {
            'Meta': {'object_name': 'TagSynonym'},
            'auto_rename_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '16'}),
            'last_auto_rename_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'owned_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tag_synonyms'", 'to': "orm['askbot.AskbotUser']"}),
            'source_tag_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'target_tag_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        'askbot.thread': {
            'Meta': {'object_name': 'Thread'},
            'accepted_answer': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['askbot.Post']"}),
            'added_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'answer_accepted_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'answer_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'approved': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'close_reason': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'closed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'closed_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.AskbotUser']", 'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'favorited_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'unused_favorite_threads'", 'symmetrical': 'False', 'through': "orm['askbot.FavoriteQuestion']", 'to': "orm['askbot.AskbotUser']"}),
            'favourite_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'followed_by': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followed_threads'", 'symmetrical': 'False', 'to': "orm['askbot.AskbotUser']"}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'group_threads'", 'symmetrical': 'False', 'through': "orm['askbot.ThreadToGroup']", 'to': "orm['askbot.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'default': "'en-us'", 'max_length': '16'}),
            'last_activity_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_activity_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'unused_last_active_in_threads'", 'to': "orm['askbot.AskbotUser']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_column': "'score'"}),
            'tagnames': ('django.db.models.fields.CharField', [], {'max_length': '125'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'threads'", 'symmetrical': 'False', 'to': "orm['askbot.Tag']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'view_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'askbot.threadtogroup': {
            'Meta': {'unique_together': "(('thread', 'group'),)", 'object_name': 'ThreadToGroup', 'db_table': "'askbot_thread_groups'"},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['askbot.Thread']"}),
            'visibility': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        'askbot.vote': {
            'Meta': {'unique_together': "(('user', 'voted_post'),)", 'object_name': 'Vote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['askbot.AskbotUser']"}),
            'vote': ('django.db.models.fields.SmallIntegerField', [], {}),
            'voted_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'voted_post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes'", 'to': "orm['askbot.Post']"})
        },
        'auth.authusergroups': {
            'Meta': {'unique_together': "(('group', 'user'),)", 'object_name': 'AuthUserGroups', 'db_table': "'auth_user_groups'", 'managed': 'False'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['askbot']
