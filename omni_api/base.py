import requests
from requests_oauthlib import OAuth1
from dateutil.parser import parse as parse_date


class ClientBase:

    @classmethod
    def get_url(cls, url, load_json=False, **kwargs):
        request = requests.get(url, **kwargs)

        if request.status_code > 299:
            raise ValueError(
                'Request to {} failed ({}): {}'.format(
                    request.url,
                    request.status_code,
                    request.content
                )
            )

        if load_json:
            return request.json()

        return request

    @staticmethod
    def get_oauth_token(key, secret):
        return OAuth1(key, secret)


class DataItem:

    def __init__(self, data):
        self.data = data

    @staticmethod
    def parse_date(date_str):
        return parse_date(date_str)
