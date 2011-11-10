# -*- coding: UTF-8 -*-
import xmlrpclib
import os
import hashlib
import re
import socket

from host import Host, HostPool
from vm import VirtualMachine, VirtualMachinePool
from user import User, UserPool
from image import Image, ImagePool
from vn import VirtualNetwork, VirtualNetworkPool
from group import Group, GroupPool
from template import VmTemplate, VmTemplatePool
from exceptions import OpenNebulaException


CONNECTED = -3
ALL = -2
CONNECTED_ADN_GROUP = -1


class Client(object):
    '''
    The client class, represents the connection with the core and handles the
    xml-rpc calls(see http://www.opennebula.org/documentation:rel3.0:api)
    '''
    DEFAULT_ONE_AUTH = "~/.one/one_auth"
    ONE_AUTH_RE = re.compile('^(.+?):(.+)$')
    DEFAULT_ONE_ADDRESS = "http://localhost:2633/RPC2"

    def __init__(self, secret=None, address=None):
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

        if password.startswith('plain:'):
            password = password.split(':', 1)[1]
        else:
            password = hashlib.sha1(password).hexdigest()
        self.one_auth = '{0}:{1}'.format(user, password)

        if address:
            self.one_address = address
        elif "ONE_XMLRPC" in os.environ and os.environ["ONE_XMLRPC"]:
            self.one_address = os.environ["ONE_XMLRPC"]
        else:
            self.one_address = self.DEFAULT_ONE_ADDRESS

        self.server = xmlrpclib.ServerProxy(self.one_address)

    def call(self, function, *args):
        '''
        Calls rpc function.

        Arguments

        ``function``
           OpenNebula xmlrpc funtcion name (without preceding 'one.')

        ``args``
           function arguments

        '''
        try:
            func = getattr(self.server.one, function)
            ret = func(self.one_auth, *args)
            try:
                is_success, data, return_code = ret
            except ValueError:
                data = ''
                is_success = False
        except socket.error, e:
            #connection error
            raise e
        if not is_success:
            raise OpenNebulaException(data)
        return data

__all__ = [Client, OpenNebulaException, Host, HostPool, VirtualMachine,
        VirtualMachinePool, User, UserPool,
        Image, ImagePool, VirtualNetwork, VirtualNetworkPool,
        Group, GroupPool, VmTemplate, VmTemplatePool, ALL, CONNECTED]

