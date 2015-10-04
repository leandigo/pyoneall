# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from warnings import warn

try:
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen
except ImportError:
    # https://github.com/PythonCharmers/python-future/issues/167
    from urllib2 import HTTPError, Request, urlopen

from future import standard_library

standard_library.install_aliases()

from base64 import standard_b64encode
from json import dumps, loads
from re import compile
from sys import version

from .base import OADict
from .classes import Users, Connections, Connection, User, BadOneAllCredentials

__version__ = '0.2.3'


class OneAll(object):
    """
    A worker for the OneAll REST API.
    """
    DEFAULT_API_DOMAIN = 'https://{site_name}.api.oneall.com'
    FORMAT__JSON = 'json'

    bindings = {}
    _version_info = (__version__, 'pyoneall', __version__, version.split()[0])

    def __init__(self, site_name, public_key, private_key, base_url=None, ua_prefix=None):
        """
        :param str site_name: The name of the OneAll site
        :param str public_key: API public key for the site
        :param str private_key: API private key for the site
        :param str base_url: An alternate format for the API URL
        :param str ua_prefix: DEPRECATED and ignored. Will be removed.
        """
        self.base_url = base_url if base_url else OneAll.DEFAULT_API_DOMAIN.format(site_name=site_name)
        self.public_key = public_key
        self.private_key = private_key
        if ua_prefix is not None:
            warn('The argument ua_prefix is no longer used. Use set_version() instead.', DeprecationWarning, 1)

    def _exec(self, action, params=None, post_params=None):
        """
        Execute an API action

        :param str action: The action to be performed. Translated to REST call
        :param dict params: Additional GET parameters for action
        :param dict post_params: POST parameters for action
        :returns dict: The JSON result of the call in a dictionary format
        """
        request_url = '%s/%s.%s' % (self.base_url, action, OneAll.FORMAT__JSON)
        if params:
            for ix, (param, value) in enumerate(params.items()):
                request_url += "%s%s=%s" % (('?' if ix == 0 else '&'), param, value)
        req = Request(request_url, dumps(post_params) if post_params else None, {'Content-Type': 'application/json'})
        token = '%s:%s' % (self.public_key, self.private_key)
        auth = standard_b64encode(token.encode())
        req.add_header('Authorization', 'Basic %s' % auth.decode())
        req.add_header('User-Agent', self._get_user_agent_string())
        try:
            request = urlopen(req)
        except HTTPError as e:
            if e.code == 401:
                raise BadOneAllCredentials
            else:
                raise
        return loads(request.read().decode())

    def _paginated(self, action, data, page_number=1, last_page=1, fetch_all=False, rtype=OADict):
        """
        Wrapper for paginated API calls. Constructs a response object consisting of one or more pages for paginated
        calls such as /users/ or /connections/. Returned object will have the ``pagination`` attribute equaling the
        the ``pagination`` value of the last page that was loaded.

        :param str action: The action to be performed.
        :param str data: The data attribute that holds the response payload
        :param int page_number: The first page number to load
        :param int last_page: The last page number to load
        :param bool fetch_all: Whether to fetch all records or not
        :param type rtype: The return type of the of the method
        :returns OADict: The API call result
        """
        oa_object = rtype()
        while page_number <= last_page or fetch_all:
            response = OADict(**self._exec(action, {'page': page_number})).response
            page = getattr(response.result.data, data)
            oa_object.count = getattr(oa_object, 'count', 0) + getattr(page, 'count', 0)
            oa_object.entries = getattr(oa_object, 'entries', []) + getattr(page, 'entries', [])
            oa_object.pagination = page.pagination
            oa_object.response = response
            page_number += 1
            if page.pagination.current_page == page.pagination.total_pages:
                break
        return oa_object

    def users(self, page_number=1, last_page=1, fetch_all=False):
        """
        Get users

        :param int page_number: The first page number to load
        :param int last_page: The last page number to load
        :param bool fetch_all: Whether to fetch all records or not
        :returns Users: The users objects
        """
        users = self._paginated('users', 'users', page_number, last_page, fetch_all, Users)
        users.oneall = self
        [setattr(entry, 'oneall', self) for entry in users.entries]
        return users

    def user(self, user_token):
        """
        Get a user by user token

        :param str user_token: The user token
        :returns User: The user object
        """
        response = OADict(**self._exec('users/%s' % (user_token,))).response
        user = User(**response.result.data.user)
        user.response = response
        user.oneall = self
        return user

    def user_contacts(self, user_token):
        """
        Get user's contacts by user token

        :param str user_token: The user token
        :returns OADict: User's contacts object
        """
        response = OADict(**self._exec('users/%s/contacts' % (user_token,))).response
        user_contacts = OADict(**response.result.data.identities)
        user_contacts.response = response
        return user_contacts

    def connections(self, page_number=1, last_page=1, fetch_all=False):
        """
        Get connections

        :param int page_number: The first page number to load
        :param int last_page: The last page number to load
        :param bool fetch_all: Whether to fetch all records or not
        :returns Users: The connections
        """
        connections = self._paginated('connections', 'connections', page_number, last_page, fetch_all,
                                      rtype=Connections)
        connections.oneall = self
        [setattr(entry, 'oneall', self) for entry in connections.entries]
        return connections

    def connection(self, connection_token):
        """
        Get connection details by connection token

        :param str connection_token: The connection token
        :returns Connection: The requested connection
        """
        response = OADict(**self._exec('connection/%s' % (connection_token,))).response
        connection = Connection(**response.result.data)
        connection.response = response
        return connection

    def publish(self, user_token, post_params):
        """
        Publish a message on behalf of the user

        :param str user_token: The user token
        :param dict post_params: The message in the format described in OneAll documentation
        :returns OADict: The API response
        """
        return OADict(**self._exec('users/%s/publish' % user_token, post_params=post_params))

    def set_version(self, social_version, platform_name, platform_version):
        """
        Sets the version informed to OneAll.com in User-Agent strings. This info is used by OneAll.com to keep track of
        which implementations are in use; all languages and environments.

        :param str social_version: PEP-440 compliant version number of client code.
        :param str platform_name: Name of platform, no spaces.
                                  Make sure it's unique so your library project won't be confused with someone else's.
        :param str platform_version: PEP-440 compliant version number of platform, e.g. Django or Flask version.
        """
        result = (social_version, platform_name, platform_version, version.split()[0])
        invalid = tuple(filter(compile(r'[\s/]').search, result))
        if invalid:
            raise ValueError('The following values are invalid: [%s]' % ','.join(invalid))
        self._version_info = result

    def _get_user_agent_string(self):
        ua = 'SocialLogin/%s %s/%s-%s pyoneall +http://oneall.com' % self._version_info
        print(ua)
        return ua
