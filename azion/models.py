import pendulum

import azion.exceptions as exceptions


def instance_from_data(model, data):
    if not data:
        return None
    return model(data)


def many_of(model, data):
    if not data:
        return []
    return [instance_from_data(model, resource) for
            resource in data]


def decode_json(response, excepted_status_code):
    """Decode a JSON response.
    """

    # Bad request is interpreted as a falsey value.
    # So we compare it with `None`.
    if response is None:
        return None

    status_code = response.status_code
    if status_code != excepted_status_code:
        if status_code >= 400:
            raise exceptions.handle_error(response)

    return response.json()


def as_boolean(response, expected_status_code):
    if response:
        if response.status_code == expected_status_code:
            return True
        if response.status_code >= 400:
            raise exceptions.handle_error(response)
    return False


def filter_none(data):
    return {key: value for key, value in data.items() if value is not None}


def to_date(date):
    """Convert a string to a datetime object.
    """
    return pendulum.parse(date)


class Token(object):
    """Model representing the authorized token retrieved
    from the API.
    """

    def __init__(self, data):
        self.load_data(data)

    def load_data(self, data):
        self.token = data['token']
        self.created_at = to_date(data['created_at'])
        self.expires_at = to_date(data['expires_at'])

    def __repr__(self):
        return '<TokenAuth [{}]>'.format(self.token[:6])


class Configuration(object):
    """Model representing the configuration retrieved
    from the API.
    """

    def __init__(self, data):
        self.load_data(data)

    def __repr__(self):
        return '<Configuration [{} ({})]>'.format(self.name,
                                                  self.domain_name)

    def load_data(self, data):
        self.id = data['id']
        self.name = data['name']
        self.domain_name = data['domain_name']
        self.active = data['active']
        self.delivery_protocol = data['delivery_protocol']
        self.digital_certificate = data['digital_certificate']
        self.cname = data['cname']
        self.cname_access_only = data['cname_access_only']
        self.rawlogs = data['rawlogs']
        self.application_aceleration = data['application_aceleration']


class ErrorResponses(object):
    """Model representing the error responses configuration 
    retrieved from the API.
    """

    def __init__(self, data):
        self.load_data(data)

    def __repr__(self):
        return '<ErrorResponses [{} ({})]>'.format(self.name,
                                                   self.domain_name)

    def load_data(self, data):
        self.cache_error_400 = data['cache_error_400']
        self.cache_error_403 = data['cache_error_403']
        self.cache_error_404 = data['cache_error_404']
        self.cache_error_405 = data['cache_error_405']
        self.cache_error_414 = data['cache_error_414']
        self.cache_error_416 = data['cache_error_416']
        self.cache_error_501 = data['cache_error_501']


class Address(object):
    """Model representing an Address - a related resource
    of `Origin` model.
    """

    def __init__(self, data):
        self.load_data(data)

    def load_data(self, data):
        self.address = data['address']
        self.weight = data['weight']
        self.server_role = data['server_role']
        self.is_active = data['is_active']


class Origin(object):
    """Model representing the Origin retrieved
    from the API.
    """

    def __init__(self, data):
        self.load_data(data)

    def __repr__(self):
        return '<Origin [{}]>'.format(self.name)

    def load_data(self, data):
        self.id = data['id']
        self.name = data['name']
        self.origin_type = data['origin_type']
        self.method = data['method']
        self.host_header = data['host_header']
        self.origin_protocol_policy = data['origin_protocol_policy']
        self.addresses = many_of(Address, data['addresses'])
        self.connection_timeout = data['connection_timeout']
        self.timeout_between_bytes = data['timeout_between_bytes']