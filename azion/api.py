import requests
from azion.__version__ import __version__ as version
from azion.models import (
    Configuration, Origin, Token, as_boolean,
    decode_json, filter_none, instance_from_data, many_of)


class Azion():

    def __init__(self, token=None, session=None):

        self.session = session or Session()

        if token:
            self.login(token)

    def auth(self, username, password):
        url = self.session.build_url('tokens')
        response = self.session.post(url, data={}, auth=(username, password))
        json = decode_json(response, 201)

        return instance_from_data(Token, json)

    def login(self, token):
        self.session.token_auth(token)

    def list_configurations(self):
        """List configurations."""
        url = self.session.build_url('content_delivery', 'configurations')
        response = self.session.get(url)
        json = decode_json(response, 200)
        return many_of(Configuration, json)


class Session(requests.Session):
    auth = None

    def __init__(self):
        super(Session, self).__init__()
        self.headers.update({
            'Accept': 'application/json; version=2',
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent': 'azion-sdk-python/{}'.format(version)
        })
        self.base_url = 'https://api.azionapi.net'

    def token_auth(self, token):
        self.headers.update({
            'Authorization': 'token {}'.format(token)
        })

    def build_url(self, *args, **kwargs):
        """Build a URL depending on the `base_url`
        attribute."""
        params = [kwargs.get('base_url') or self.base_url]
        params.extend(args)
        params = map(str, params)
        return '/'.join(params)
