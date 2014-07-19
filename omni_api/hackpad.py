from omni_api.base import ClientBase, DataItem


class HackpadClient(ClientBase):
    def __init__(self, client_id, secret):
        self.auth = self.get_oauth_token(client_id, secret)

    def get_url(self, url, **kwargs):
        kwargs['auth'] = self.auth

        return super(HackpadClient, self).get_url(
            url,
            load_json=True,
            **kwargs
        )

    def search(self, query):
        url = 'https://hackpad.com/api/1.0/search'
        params = {
            'q': query,
        }

        result = self.get_url(url, params=params)

        return [HackPad(i) for i in result]


class HackPad(DataItem):

    @property
    def id(self):
        return self.data['id']

    @property
    def creator_id(self):
        return self.data['creatorId']

    @property
    def domain_id(self):
        return self.data['domainId']

    @property
    def last_edited(self):
        return self.parse_date(self.data['lastEditedDate'])

    @property
    def last_editor_id(self):
        return self.data['lastEditorId']

    @property
    def snippet(self):
        """Markup"""
        return self.data['snippet']

    @property
    def title(self):
        return self.data['title']
