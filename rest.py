
import json
from urlparse import urlparse
import urllib2
import time

PUT = "PUT"
POST = "POST"
PATCH = "PATCH"
X_HTTP_METHOD_OVERRIDE = 'X-HTTP-Method-Override'


class RequestWithMethod(urllib2.Request):

    def __init__(self, *args, **kwargs):
        self._method = kwargs.get('method', None)
        headers = kwargs.get('headers', {})
        if 'method' in kwargs:
            del kwargs['method']
        if self._method == PUT:
            self._method = POST
            headers[X_HTTP_METHOD_OVERRIDE] = PUT
        if self._method == PATCH:
            self._method = POST
            headers[X_HTTP_METHOD_OVERRIDE] = PATCH
        if headers:
            kwargs['headers'] = headers
        urllib2.Request.__init__(self, *args, **kwargs)

    def get_method(self):
        if self._method:
            return self._method
        else:
            return urllib2.Request.get_method(self)

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

    def open_server_url(self, url, data=None, authorization=None, method=None):
        url = "{0}{1}".format(self.server, url)
        req = RequestWithMethod(url=url, data=data, method=method)
        if data:
            req.add_header('Content-Type', 'application/json')
        if authorization:
            req.add_header('AUTHORIZATION_KEY',authorization)
        return self.opener.open(req)

    def open_url(self, url, data=None, authorization=None, method=None):
        req = RequestWithMethod(url=url, data=data, method=method)
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
    authorization = 'dda672f828fa6fc0949f4eb7340d2208830cd057d49cf2e53f404eebd562359c'

    def __init__(self, *args, **kwargs):
        super(RobotClient, self).__init__(*args, **kwargs)
        self.aliases = dict()

    def robots(self):
        if not self.connected:
            self.connect()
        data = json.loads(self.open_server_url(self.api_root + '/robot2/?limit=0', authorization=self.authorization).read())
        assert 'objects' in data
        return map(lambda o: o['uuid'], data['objects'])

    def abilities(self):
        if not self.connected:
            self.connect()
        data = json.loads(self.open_server_url(self.api_root + '/ability/?limit=0', authorization=self.authorization).read())
        assert 'objects' in data
        return map(lambda o: o['name'], data['objects'])

    def robots_aliases(self):
        if not self.connected:
            self.connect()
        data = json.loads(self.open_server_url(self.api_root + '/robot2/?limit=0', authorization=self.authorization).read())
        assert 'objects' in data
        aliases = map(lambda o: (o['uuid'], o['alias']), data['objects'])
        def first(x):
            return x[0]
        def swap(x):
            return x[1], x[0]
        self.aliases = dict(filter(first,map(swap,aliases)))
        return aliases

    def set_alias(self, robot, alias):
        if not self.connected:
            self.connect()
        data = dict(uuid=robot, alias=alias)
        result = self.open_server_url(self.api_root + '/robot2/{0}/'.format(robot), data=json.dumps(data), authorization=self.authorization, method='PUT')

    def get_data(self, robot):
        if not self.connected:
            self.connect()
        if robot in self.aliases:
            robot = self.aliases[robot]
        data = json.loads(self.open_server_url(self.api_root + '/robot2/{0}/'.format(robot), authorization=self.authorization).read())
        return data

    def create_robot(self):
        if not self.connected:
            self.connect()
        data = dict()
        result = self.open_server_url(self.api_root + '/robot2/', data=json.dumps(data))
        return self.extract_location(result, Exception('Could not create robot'))
