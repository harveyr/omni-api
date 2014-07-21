import base


class StashClient(base.ClientBase):
    def __init__(self, url_base, username, password):
        self.url_base = url_base
        self.auth = (username, password)

    def get_url(self, path, **kwargs):
        url = self.url_base + '/rest/api/1.0' + path

        kwargs['auth'] = self.auth
        
        return super(StashClient, self).get_url(
            url,
            load_json=True,
            verify=False,
            **kwargs
        )

    def get_projects(self):
        result = self.get_url('/projects')

        return [StashProject(p) for p in result['values']]

    def get_repos(self, count=None):
        repos = []
        params = {'limit': 200}

        result = self.get_url('/repos', params=params)
        repos += result['values']

        while not result['isLastPage']:
            if count and len(repos) >= count:
                break

            params['start'] = result['nextPageStart']
            result = self.get_url('/repos', params=params)
            repos += result['values']

        return [StashRepo(r) for r in repos]


class StashRepo(base.DataItem):
    @property
    def clone_url(self):
        return self.data['cloneUrl']

    @property
    def id(self):
        return self.data['id']

    @property
    def link_url(self):
        return self.data['link']['url']

    @property
    def name(self):
        return self.data['name']

    @property
    def project_data(self):
        return self.data['project']

    @property
    def project_name(self):
        return self.project_data['name']

    @property
    def project_key(self):
        return self.project_data['key']

    @property
    def project_name(self):
        return self.project_data['name']

    @property
    def slug(self):
        return self.project_data['slug']


class StashProject(base.DataItem):

    @property
    def key(self):
        return self.data['key']

    @property
    def link(self):
        return self.data['link']['url']

    @property
    def description(self):
        return self.data['description']

    @property
    def name(self):
        return self.data['name']

    @property
    def is_public(self):
        return self.data['public']

    @property
    def type(self):
        return self.data['type']

