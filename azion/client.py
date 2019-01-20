from azion.session import Session
from azion.models import (
    Configuration, ErrorResponses, CacheSettings, Rule, Token,
    as_boolean, decode_json, filter_none, instance_from_data, many_of)


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

    def get_configuration(self, configuration_id):
        """Get configuration."""
        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id)
        response = self.session.get(url)
        json = decode_json(response, 200)
        return instance_from_data(Configuration, json)

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
        json.update({'id': configuration_id})
        return instance_from_data(ErrorResponses, json)

    def update_error_responses(self, configuration_id, cache_error_400=None,
                               cache_error_403=None, cache_error_404=None,
                               cache_error_405=None, cache_error_414=None,
                               cache_error_416=None, cache_error_501=None):
        """Update error responses of the configuration."""

        data = {
            'cache_error_400': cache_error_400,
            'cache_error_403': cache_error_403,
            'cache_error_404': cache_error_404,
            'cache_error_405': cache_error_405,
            'cache_error_414': cache_error_414,
            'cache_error_416': cache_error_416,
            'cache_error_501': cache_error_501,
        }

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'error_responses')
        response = self.session.patch(url, json=filter_none(data))

        response = self.session.get(url)
        json = decode_json(response, 200)
        json.update({'id': configuration_id})
        return instance_from_data(ErrorResponses, json)

    def list_cache_settings(self, configuration_id):
        """List cache settings of the configuration."""

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'cache_settings')

        response = self.session.get(url)
        json = decode_json(response, 200)
        return many_of(CacheSettings, json)

    def get_cache_settings(self, configuration_id, cache_id):
        """Get a cache settings of the configuration."""

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'cache_settings',
                                     cache_id)

        response = self.session.get(url)
        json = decode_json(response, 200)
        return instance_from_data(CacheSettings, json)

    def delete_cache_settings(self, configuration_id, cache_id):
        """Delete a cache settings of the configuration."""

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'cache_settings',
                                     cache_id)

        response = self.session.delete(url)
        return as_boolean(response, 204)

    def create_cache_settings(self, configuration_id,
                              name, browser_cache_settings='honor',
                              browser_cache_settings_maximum_ttl=None,
                              cdn_cache_settings='honor',
                              cdn_cache_settings_maximum_ttl=None,
                              cache_by_query_string='ignore',
                              query_string_fields='None',
                              enable_query_string_sort=False,
                              cache_by_cookies='ignore',
                              cookie_names=None,
                              adaptive_delivery_action='ignore',
                              device_group=None,
                              enable_caching_for_post=False):

        data = {
            'name': name,
            'browser_cache_settings': browser_cache_settings,
            'browser_cache_settings_maximum_ttl': browser_cache_settings_maximum_ttl,
            'cdn_cache_settings': cdn_cache_settings,
            'cdn_cache_settings_maximum_ttl': cdn_cache_settings_maximum_ttl,
            'cache_by_query_string': cache_by_query_string,
            'query_string_fields': query_string_fields,
            'enable_query_string_sort': enable_query_string_sort,
            'cache_by_cookies': cache_by_cookies,
            'cookie_names': cookie_names,
            'adaptive_delivery_action': adaptive_delivery_action,
            'device_group': device_group,
            'enable_caching_for_post': enable_caching_for_post
        }

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'cache_settings')

        response = self.session.post(url, json=filter_none(data))
        json = decode_json(response, 201)
        return instance_from_data(CacheSettings, json)

    def update_cache_settings(self, configuration_id, cache_id,
                              name=None,
                              browser_cache_settings=None,
                              browser_cache_settings_maximum_ttl=None,
                              cdn_cache_settings=None,
                              cdn_cache_settings_maximum_ttl=None,
                              cache_by_query_string=None,
                              query_string_fields=None,
                              enable_query_string_sort=None,
                              cache_by_cookies=None,
                              cookie_names=None,
                              adaptive_delivery_action=None,
                              device_group=None,
                              enable_caching_for_post=None):

        data = {
            'name': name,
            'browser_cache_settings': browser_cache_settings,
            'browser_cache_settings_maximum_ttl': browser_cache_settings_maximum_ttl,
            'cdn_cache_settings': cdn_cache_settings,
            'cdn_cache_settings_maximum_ttl': cdn_cache_settings_maximum_ttl,
            'cache_by_query_string': cache_by_query_string,
            'query_string_fields': query_string_fields,
            'enable_query_string_sort': enable_query_string_sort,
            'cache_by_cookies': cache_by_cookies,
            'cookie_names': cookie_names,
            'adaptive_delivery_action': adaptive_delivery_action,
            'device_group': device_group,
            'enable_caching_for_post': enable_caching_for_post
        }

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'cache_settings',
                                     cache_id)

        response = self.session.patch(url, json=filter_none(data))
        json = decode_json(response, 200)
        return instance_from_data(CacheSettings, json)

    def list_rules_engine(self, configuration_id, phase):
        """List rules from a phase of rules engine of the configuration."""

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'rules_engine',
                                     phase,
                                     'rules')

        response = self.session.get(url)
        json = decode_json(response, 200)
        return many_of(Rule, json)

    def get_rules_engine(self, configuration_id, phase, rule_id):
        """Get rule from a phase of rules engine of the configuration."""

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'rules_engine',
                                     phase,
                                     'rules',
                                     rule_id)

        response = self.session.get(url)
        json = decode_json(response, 200)
        return instance_from_data(Rule, json)

    def delete_rules_engine(self, configuration_id, phase, rule_id):
        """Delete a rule from rules engine of the configuration."""

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'rules_engine',
                                     phase,
                                     'rules',
                                     rule_id)

        response = self.session.delete(url)
        return as_boolean(response, 204)

    def create_rules_engine(self, configuration_id,
                            name, phase, criteria,
                            behaviors, order=None):

        data = {
            'name': name,
            'phase': phase,
            'criteria': criteria,
            'behaviors': behaviors,
            'order': order
        }

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'rules_engine',
                                     phase,
                                     'rules')

        response = self.session.post(url, json=filter_none(data))
        json = decode_json(response, 201)
        return instance_from_data(Configuration, json)

    def update_rules_engine(self, configuration_id, phase,
                            rule_id, name, criteria=None,
                            behaviors=None, order=None):

        data = {
            'name': name,
            'phase': phase,
            'criteria': criteria,
            'behaviors': behaviors,
            'order': order
        }

        url = self.session.build_url('content_delivery',
                                     'configurations',
                                     configuration_id,
                                     'rules_engine',
                                     phase,
                                     'rule',
                                     rule_id)

        response = self.session.patch(url, json=filter_none(data))
        json = decode_json(response, 200)
        return instance_from_data(CacheSettings, json)
