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

    def _base_params(self):
        return {
            'name': self.CLIENT_NAME,
            'key': self.api_key,
            'token': self.api_token,
        }

    def get_url(self, path, **kwargs):
        url = 'https://api.trello.com/1' + path

        params = kwargs.get('params', {})
        params.update(self._base_params())

        kwargs['params'] = params

        return super(TrelloClient, self).get_url(url, load_json=True, **kwargs)

    def post_url(self, url, **kwargs):
        data = kwargs.get('data', {})
        data.update(self._base_params())
        
        kwargs['data'] = data
        
        return super(TrelloClient, self).post_url(url, **kwargs)

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

        boards = [TrelloBoard(b) for b in data]
        filtered = [b for b in boards if not b.closed and b.last_activity]
        filtered.sort(key=lambda x: x.last_activity, reverse=True)

        return filtered

    def get_lists(self, board_id):
        data = self.get_url('/boards/{}/lists'.format(board_id))

        return [TrelloList(l) for l in data]

    def create_card(self, list_id, name, desc='Created with OmniApi'):
        url = '/cards'

        data = {
            'name': name,
            'idList': list_id,
            'desc': desc,
        }

        self.post_url(
            url,
            data=data
        )


class TrelloList(base.DataItem):

    @property
    def id(self):
        return self.data['id']

    @property
    def name(self):
        return self.data['name']


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

    @property
    def closed(self):
        return self.data['closed']

    @property
    def last_activity(self):
        date_str = self.data['dateLastActivity']

        if date_str:
            return self.parse_date(date_str)

        return None

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

