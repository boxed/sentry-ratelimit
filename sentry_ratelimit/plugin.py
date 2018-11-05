# coding=utf-8
from datetime import timedelta, datetime

import re
from django import forms
from sentry.plugins import Plugin
from sentry.plugins.bases.notify import NotificationConfigurationForm
import sentry_ratelimit


class ratelimitConfigurationForm(NotificationConfigurationForm):
    patterns = forms.CharField(label='Regex patterns to match', required=True, widget=forms.Textarea)
    events_last_hour = forms.IntegerField(label='Events last hour', required=True, help_text='Number of events per hour to allow before flagging a regression')


class ratelimitMessage(Plugin):
    title = 'ratelimit'
    conf_key = 'ratelimit'
    slug = 'ratelimit'
    version = sentry_ratelimit.VERSION
    author = 'Anders Hovmöller'
    author_url = 'http://www.github.com/boxed'
    project_conf_form = ratelimitConfigurationForm

    def is_configured(self, project):
        return all(self.get_option(k, project) for k in ('patterns', 'events_last_hour'))

    def is_regression(self, group, event, **kwargs):
        patterns = self.get_option('patterns', event.project)
        message = event.message
        metadata_value = event.get_event_metadata('value')

        def matches_patterns(s):
            for p in patterns.split('\n'):
                if re.match(p, s):
                    return True
            return False

        if matches_patterns(message) or (metadata_value and matches_patterns(metadata_value)):
            events_last_hour = group.event_set.filter(datetime__gt=datetime.now() - timedelta(hours=1)).count()

            return events_last_hour > int(self.get_option('events_last_hour', event.project))
        else:
            return True
