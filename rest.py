
import json
from urlparse import urlparse
import urllib2
import time


class RestClient(object):

    apt_root = None

    def __init__(self, server, user, password):
        self.server = server
        self.user = user
        self.password = password
        self.keys = {}
        self.connected = False

    def authenticate(self, realm, uri):
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password(realm=realm,
                                  uri=uri,
                                  user=self.user,
                                  passwd=self.password)

        self.opener = urllib2.build_opener(auth_handler)

    def open_server_url(self, url, data=None, authorization=None):
        url = "{0}{1}".format(self.server, url)
        req = urllib2.Request(url=url, data=data)
        if data:
            req.add_header('Content-Type', 'application/json')
        if authorization:
            req.add_header('AUTHORIZATION_KEY',authorization)
        return self.opener.open(req)

    def open_url(self, url, data=None, authorization=None):
        req = urllib2.Request(url=url, data=data)
        if data:
            req.add_header('Content-Type', 'application/json')
        if authorization:
            req.add_header('AUTHORIZATION_KEY',authorization)
        return self.opener.open(req)

    def connect(self):
        self.authenticate("", self.server)
        self.connected = True
        result = None
        try:
            result = self.open_server_url(self.api_root).read()
            return json.loads(result)
        except Exception, e:
            print e
            print result
            raise e

    def extract_location(self, result, exception):
        if 'Location' not in result.headers:
            raise exception
        return urlparse(result.headers['Location']).path


class RobotClient(RestClient):

    api_root = '/leaf_api/v1'
    authorization = 'c5a69900b98f874e9d01532a78da2291642eabe72de5d3338b8c01ba1d52e0e7'

    def robots(self):
        if not self.connected:
            self.connect()
        data = json.loads(self.open_server_url(self.api_root + '/robot/?limit=0', authorization=self.authorization).read())
        assert 'objects' in data
        return map(lambda o: o['uuid'], data['objects'])

    def get_config(self, robot):
        if not self.connected:
            self.connect()
        data = json.loads(self.open_server_url(self.api_root + '/configuration/?limit=0&robot={0}'.format(robot)).read())
        assert 'objects' in data
        return map(lambda o: o['config_line'], data['objects'])

