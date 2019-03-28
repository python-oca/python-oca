# -*- coding: UTF-8 -*-
import http.client
import os
import re
import socket
import xmlrpc.client

from .cluster import Cluster, ClusterPool
from .datastore import Datastore, DatastorePool
from .exceptions import OpenNebulaException
from .group import Group, GroupPool
from .host import Host, HostPool
from .image import Image, ImagePool
from .template import VmTemplate, VmTemplatePool
from .user import User, UserPool
from .vm import VirtualMachine, VirtualMachinePool
from .vn import VirtualNetwork, VirtualNetworkPool

CONNECTED = -3
ALL = -2
CONNECTED_AND_GROUP = -1


class TimeoutHTTPConnection(http.client.HTTPConnection):
    def connect(self):
        http.client.HTTPConnection.connect(self)
        self.sock.settimeout(self.timeout)


class TimeoutHTTP(http.client.HTTPConnection):
    _connection_class = TimeoutHTTPConnection

    def set_timeout(self, timeout):
        self._conn.timeout = timeout


class ProxiedTransport(xmlrpc.client.Transport):
    def __init__(self, timeout=socket._GLOBAL_DEFAULT_TIMEOUT, *args, **kwargs):
        xmlrpc.client.Transport.__init__(self, *args, **kwargs)
        self.timeout = timeout

    def set_proxy(self, proxy):
        self.proxy = proxy

    def make_connection(self, host):
        self.realhost = host
        h = http.client.HTTPConnection(self.proxy)
        return h

    def send_request(self, connection, handler, request_body):
        connection.putrequest("POST", 'http://%s%s' % (self.realhost, handler))

    def send_host(self, connection, host):
        connection.putheader('Host', self.realhost)


class Client(object):
    """
    The client class, represents the connection with the core and handles the
    xml-rpc calls(see http://www.opennebula.org/documentation:rel3.2:api)
    """
    DEFAULT_ONE_AUTH = "~/.one/one_auth"
    ONE_AUTH_RE = re.compile('^(.+?):(.+)$')
    DEFAULT_ONE_ADDRESS = "http://localhost:2633/RPC2"

    def __init__(self, secret=None, address=None, proxy=None):
        self.one_version = None

        if secret:
            one_secret = secret
        elif "ONE_AUTH" in os.environ and os.environ["ONE_AUTH"]:
            one_auth = os.path.expanduser(os.environ["ONE_AUTH"])
            with open(one_auth) as f:
                one_secret = f.read().strip()
        elif os.path.exists(os.path.expanduser(self.DEFAULT_ONE_AUTH)):
            with open(os.path.expanduser(self.DEFAULT_ONE_AUTH)) as f:
                one_secret = f.read().strip()
        else:
            raise OpenNebulaException('ONE_AUTH file not present')

        one_secret = self.ONE_AUTH_RE.match(one_secret)
        if one_secret:
            user = one_secret.groups()[0]
            password = one_secret.groups()[1]
        else:
            raise OpenNebulaException("Authorization file malformed")

        self.one_auth = '{0}:{1}'.format(user, password)

        if address:
            self.one_address = address
        elif "ONE_XMLRPC" in os.environ and os.environ["ONE_XMLRPC"]:
            self.one_address = os.environ["ONE_XMLRPC"]
        else:
            self.one_address = self.DEFAULT_ONE_ADDRESS

        if proxy:
            p = ProxiedTransport(timeout=100)
            p.set_proxy(proxy)
            self.server = xmlrpc.client.ServerProxy(self.one_address, transport=p)
        else:
            self.server = xmlrpc.client.ServerProxy(self.one_address)

    def call(self, function, *args):
        """
        Calls rpc function.

        Arguments

        ``function``
           OpenNebula xmlrpc funtcion name (without preceding 'one.')

        ``args``
           function arguments

        """
        try:
            func = getattr(self.server.one, function)
            ret = func(self.one_auth, *args)
            try:
                is_success, data, return_code = ret
            except ValueError:
                data = ''
                is_success = False
        except socket.error as e:
            # connection error
            raise e
        if not is_success:
            raise OpenNebulaException(data)
        return data

    def version(self):
        """
        Get the version of the connected OpenNebula server.
        """
        self.one_version = self.call('system.version')
        return self.one_version


__all__ = [Client, OpenNebulaException, Host, HostPool, VirtualMachine,
           VirtualMachinePool, User, UserPool,
           Image, ImagePool, VirtualNetwork, VirtualNetworkPool,
           Group, GroupPool, VmTemplate, VmTemplatePool, ALL, CONNECTED,
           Cluster, ClusterPool, Datastore, DatastorePool]
