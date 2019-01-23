import os
from azion.session import Session
from azion.models import (
    Service, Configuration, ErrorResponses, CacheSettings, Rule, Token,
    as_boolean, decode_json, filter_none, instance_from_data, many_of)
import azion.__consts__ as consts
import azion.exceptions as exceptions


class BaseClient():

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

    def __call__(self, service):
        known_services = consts.AVAILABLE_SERVICES
        if service not in known_services:
            raise exceptions.UnknownServiceError

        return Service(self, service)
