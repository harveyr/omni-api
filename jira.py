import os
import datetime
from omni_api import base

import pytz

JIRA_HOST = 'https://tofurkey.urbanairship.com'
TIMEZONE = pytz.timezone('US/Pacific')


class JiraClient(base.ClientBase):
    def __init__(self, username=None, password=None):
        self.username = username
        self.auth = (self.username, password)

    @staticmethod
    def url(path):
        return JIRA_HOST + '/rest/api/2' + path

    def get_url(self, path, **kwargs):
        url = self.url(path)
        kwargs['auth'] = self.auth

        return super(JiraClient, self).get_url(url, load_json=True, **kwargs)

    def get_issue(self, issue):
        result = self.get_url('/issue/' + issue)

        return Issue(result)

    def get_users_issues(self, username=None, max_results=50):
        username = username or self.username

        jql = (
            'assignee={user} '
            'and resolution = Unresolved '
            'and status != Cancelled '
            'order by updated desc'
        ).format(user=username, max=max_results)

        result = self.get_url(
            '/search',
            params={
                'jql': jql,
                'maxResults': max_results
            }
        )

        return [Issue(i) for i in result['issues']]


class Issue(base.DataItem):

    def field(self, key):
        return self.data['fields'].get(key)

    @property
    def summary(self):
        return self.field('summary')

    @property
    def url(self):
        return self.data['self']

    @property
    def key(self):
        return self.data['key']

    @property
    def updated(self):
        return self.parse_date(self.field('updated'))

    @property
    def updated_age(self):
        now = datetime.datetime.now(TIMEZONE)

        return now - self.updated

    @property
    def created(self):
        return self.parse_date(self.field('created'))
