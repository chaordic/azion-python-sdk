import requests
import azion.__consts__ as consts


class Session(requests.Session):
    auth = None

    def __init__(self):
        super(Session, self).__init__()
        self.headers.update({
            'Accept': 'application/json; version=2',
            'Accept-Charset': 'utf-8',
            'Content-Type': 'application/json',
            'User-Agent': '{}'.format(consts.USER_AGENT)
        })
        self.base_url = consts.API_PUBLIC_ENDPOINT

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
