import requests
from requests_oauthlib import OAuth1
from dateutil.parser import parse as parse_date


class ClientBase(object):
    """
    Abstract parent class for API clients.
    """

    def _finish_request(self, request, load_json=False):
        if request.status_code > 299:
            raise ValueError(
                'Request failed with {} to {}: {}'.format(
                    request.status_code,
                    request.url,
                    request.content
                )
            )

        if load_json:
            return request.json()

        return request

    def get_url(self, url, load_json=False, **kwargs):
        request = requests.get(url, **kwargs)

        return self._finish_request(
            request,
            load_json=load_json
        )

    def post_url(self, url, load_json=False, **kwargs):
        request = requests.post(url, **kwargs)

        return self._finish_request(
            request,
            load_json=load_json
        )



    @staticmethod
    def get_oauth_token(key, secret):
        return OAuth1(key, secret)


class DataItem(object):
    """
    Simple wrapper around response json.
    """

    def __init__(self, data):
        self.data = data

    @staticmethod
    def parse_date(date_str):
        return parse_date(date_str)
