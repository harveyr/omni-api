from datetime import datetime, timedelta

from omni_api import base


class GithubClient(base.ClientBase):
    def __init__(self, access_token):
        self.access_token = access_token

    @staticmethod
    def api_url(path):
        return 'https://api.github.com' + path

    @classmethod
    def repo_url(cls, repo_path, suffix):
        return cls.api_url('/repos/{}/{}'.format(repo_path, suffix))

    def get_url(self, url, **kwargs):
        params = kwargs.get('params', {})
        params['access_token'] = self.access_token

        headers = {
            'Accept': 'application/vnd.github.v3+json',
        }

        kwargs['params'] = params
        kwargs['headers'] = headers

        return super(GithubClient, self).get_url(url, load_json=True, **kwargs)

    def get_prs(self, repo_path):
        url = self.repo_url(repo_path, 'pulls')
        result = self.get_url(url)

        prs = [PullRequest(p) for p in result]

        prs.sort(key=lambda x: x.updated, reverse=True)

        return prs

    def get_commits(self, repo_path, since=None, author=None):
        since = since or datetime.now() - timedelta(days=7)

        params = {
            'since': since.isoformat(),
        }

        if author:
            params['author'] = author

        url = self.repo_url(repo_path, 'commits')

        result = self.get_url(url, params=params)

        commits = [Commit(c) for c in result]

        commits.sort(key=lambda x: x.date, reverse=True)

        return commits


class DataClass(object):
    def __init__(self, data):
        self.data = data


class Commit(base.DataItem):
    
    @property
    def api_url(self):
        return self.data['url']

    @property
    def sha(self):
        return self.data['sha']

    @property
    def html_url(self):
        return self.data['html_url']

    @property
    def author_data(self):
        # Don't use `get`. The value might legitimately be None.
        data = self.data['author']

        return data or {}

    @property
    def author_name(self):
        return self.author_data['login']

    @property
    def committer_data(self):
        # Don't use `get`. The value might legitimately be None.
        data = self.data['committer']

        return data or {}

    @property
    def username(self):
        return (
            self.committer_data.get('login') or
            self.author_data.get('login')
        )

    @property
    def commit_data(self):
        return self.data['commit']

    @property
    def commit_message(self):
        return self.commit_data['message']

    @property
    def date(self):
        return self.parse_date(self.commit_data['committer']['date'])

    @property
    def sha(self):
        return self.data['sha']


class PullRequest(base.DataItem):

    @property
    def id(self):
        return self.data['id']

    @property
    def number(self):
        return self.data['number']

    @property
    def title(self):
        return self.data['title']

    @property
    def html_url(self):
        return self.data['html_url']

    @property
    def state(self):
        return self.data['state']

    @property
    def user_data(self):
        return self.data['user']

    @property
    def username(self):
        return self.user_data['login']

    @property
    def updated(self):
        return self.parse_date(self.data['updated_at'])
