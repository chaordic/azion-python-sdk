import requests
from azion.__version__ import __version__ as version
from azion.models import (
    Configuration, ErrorResponses, Origin, Token, as_boolean,
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

    def get_configurations(self, configuration_id):
        """Get configuration."""
        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id)
        response = self.session.get(url)
        json = decode_json(response, 200)
        return many_of(Configuration, json)

    def delete_configuration(self, configuration_id):
        """Delete a configuration.
        :param int configuration_id:
            Configuration ID.
        """
        url = self.session.build_url(
            'content_delivery', 'configurations', configuration_id)
        response = self.session.delete(url)
        return as_boolean(response, 204)

    def create_configuration(self, name, origin_address, origin_host_header,
                             cname=None, cname_access_only=False,
                             delivery_protocol='http',
                             digital_certificate=None,
                             origin_protocol_policy='preserve',
                             browser_cache_settings=False,
                             browser_cache_settings_maximum_ttl=0,
                             cdn_cache_settings='honor',
                             cdn_cache_settings_maximum_ttl=0):

        data = {
            'name': name, 'origin_address': origin_address,
            'origin_host_header': origin_host_header,
            'cname': cname, 'cname_access_only': cname_access_only,
            'delivery_protocol': delivery_protocol,
            'digital_certificate': digital_certificate,
            'origin_protocol_policy': origin_protocol_policy,
            'browser_cache_settings': browser_cache_settings,
            'browser_cache_settings_maximum_ttl': browser_cache_settings_maximum_ttl,
            'cdn_cache_settings': cdn_cache_settings,
            'cdn_cache_settings_maximum_ttl': cdn_cache_settings_maximum_ttl
        }

        url = self.session.build_url('content_delivery', 'configurations')
        response = self.session.post(url, json=filter_none(data))
        json = decode_json(response, 201)
        return instance_from_data(Configuration, json)

    def update_configuration(self, configuration_id, name=None,
                             cname=None, cname_access_only=None,
                             delivery_protocol=None,
                             digital_certificate=None,
                             rawlogs=None, active=None,
                             application_aceleration=None):

        data = {
            'name': name,
            'cname': cname, 'cname_access_only': cname_access_only,
            'delivery_protocol': delivery_protocol,
            'digital_certificate': digital_certificate,
            'rawlogs': rawlogs,
            'active': active,
            'application_aceleration': application_aceleration
        }

        url = self.session.build_url(
            'content_delivery', 'configurations', configuration_id)
        response = self.session.patch(url, json=filter_none(data))
        json = decode_json(response, 200)
        return instance_from_data(Configuration, json)

    def list_error_responses(self, configuration_id):
        """List error responses of the configuration."""
        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'error_responses')

        response = self.session.get(url)
        json = decode_json(response, 200)
        return many_of(ErrorResponses, json)



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
