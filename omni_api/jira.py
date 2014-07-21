import datetime
from omni_api import base
import base64

import pytz

TIMEZONE = pytz.timezone('US/Pacific')


class JiraClient(base.ClientBase):
    def __init__(self, url_base, username, password):
        if url_base[-1] == '/':
            url_base = url_base[:-1]

        self.url_base = url_base
        self.username = username
        self.auth = (username, password)

    def url(self, path):
        return self.url_base + '/rest/api/latest' + path

    def get_url(self, path, **kwargs):
        url = self.url(path)

        auth_header = base64.b64encode(':'.join(self.auth))

        kwargs['headers'] = {
            'Authorization': 'Basic ' + auth_header,
            'Content-Type': 'application/json',
        }

        return super(JiraClient, self).get_url(url, load_json=True, **kwargs)

    def get_user(self, username):
        params = {'username': username}

        result = self.get_url('/user', params=params)

        return JiraUser(result)

    def search_users(self, query):
        params = {'query': query}

        result = self.get_url('/user/search', params=params)

        return result

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


class JiraUser(base.DataItem):

    @property
    def active(self):
        return self.data['active']

    @property
    def display_name(self):
        return self.data['displayName']

    @property
    def email(self):
        return self.data['email']

    @property
    def key(self):
        return self.data['key']

    @property
    def name(self):
        return self.data['name']

    @property
    def avatar_urls(self):
        return self.data['avatarUrls']
