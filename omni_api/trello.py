import urllib

from omni_api import base


class TrelloClient(base.ClientBase):
    CLIENT_NAME = 'OmniApi'

    def __init__(self, api_key, api_token):
        self.api_key = api_key
        self.api_token = api_token

    @classmethod
    def _request_base_params(cls):
        return {
            'name': 'OmniApi',
        }

    @staticmethod
    def api_url(path):
        return 'https://api.trello.com/1' + path

    def get_url(self, path, **kwargs):
        url = 'https://api.trello.com/1' + path

        params = kwargs.get('params', {})
        params.update({
            'name': self.CLIENT_NAME,
            'key': self.api_key,
            'token': self.api_token,
        })

        kwargs['params'] = params

        return super(TrelloClient, self).get_url(url, load_json=True, **kwargs)

    @classmethod
    def get_trello_token_html_url(cls, api_key):
        params = {
            'key': api_key,
            'name': cls.CLIENT_NAME,
            'expiration': 'never',
            'response_type': 'token',
            'scope': 'read,write'
        }

        encoded = urllib.urlencode(params)

        return 'https://trello.com/1/authorize' + '?' + encoded

    def get_me(self):
        data = self.get_url('/members/me')

        return TrelloMe(data)

    def get_board(self, board_id):
        data = self.get_url('/boards/' + board_id)

        return TrelloBoard(data)

    def get_boards(self, member_id):
        data = self.get_url('/members/{}/boards'.format(member_id))

        return [TrelloBoard(b) for b in data]


class TrelloBoard(base.DataItem):

    @property
    def id(self):
        return self.data['id']

    @property
    def name(self):
        return self.data['name']

    @property
    def pinned(self):
        return self.data['pinned']

    @property
    def url(self):
        return self.data['url']

    @property
    def short_url(self):
        return self.data['shortUrl']


class TrelloMe(base.DataItem):

    @property
    def id(self):
        return self.data['id']

    @property
    def board_ids(self):
        return self.data['idBoards']

    @property
    def name(self):
        return self.data['fullName']

    @property
    def url(self):
        return self.data['url']


class TrelloCard(base.DataItem):

    @property
    def description(self):
        return self.data['desc']

    @property
    def name(self):
        return self.data['name']

    @property
    def id(self):
        return self.data['id']

    @property
    def short_id(self):
        return self.data['idShort']

    @property
    def board_id(self):
        return self.data['idBoard']

    @property
    def url(self):
        return self.data['url']

    @property
    def short_url(self):
        return self.data['shortUrl']

    @property
    def list_id(self):
        return self.data['idList']

