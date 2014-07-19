import json
from omni_api.base import ClientBase, DataItem


class JiveClient(ClientBase):
    def __init__(self, url_base, username, password):
        self.url_base = url_base
        self.auth = (username, password)

    def api_url(self, path):
        return self.url_base + '/api/core/v3' + path

    def get_url(self, url, **kwargs):
        kwargs['auth'] = self.auth

        request = super(JiveClient, self).get_url(url, **kwargs)

        # Because ... Jive?
        content = request.content.replace(
            "throw 'allowIllegalResourceCall is false.';",
            ''
        )

        try:
            return json.loads(content)
        except ValueError:
            raise ValueError(
                'Could not decode to json: {}'.format(request.content)
            )

    def get_activity(self, count=100):
        url = self.api_url('/activities')

        params = {
            # 'fields': '@summary',
            'count': count,
        }
        
        result = self.get_url(url, params=params)

        items = [
            ContentItem(i) for i in result['list']
            if i['object'].get('updated')
        ]

        items.sort(key=lambda x: x.updated, reverse=True)
        
        return items


class ContentItem(DataItem):
    @property
    def title(self):
        return self.data.get('title')

    @property
    def actor_name(self):
        return self.data['actor']['displayName']

    @property
    def summary(self):
        return self.data['object']['summary']

    @property
    def updated(self):
        try:
            return self.parse_date(self.data['object']['updated'])
        except KeyError:
            return None

    @property
    def object_type(self):
        return self.data['object']['objectType'].split('jive:')[-1]

    @property
    def verb(self):
        return self.data['verb'].split('jive:')[-1]

    @property
    def url(self):
        return self.data['object']['url']
