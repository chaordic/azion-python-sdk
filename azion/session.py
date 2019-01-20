import requests
from azion.__version__ import __version__ as version


class Session(requests.Session):
    auth = None

    def __init__(self):
        super(Session, self).__init__()
        self.headers.update({
            'Accept': 'application/json; version=2',
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent': 'azion-python-sdk/{}'.format(version)
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
