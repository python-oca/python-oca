# -*- coding: UTF-8 -*-
import os
import socket
import unittest

from mock import Mock
from nose.tools import raises

import oca


class TestClient(unittest.TestCase):
    def setUp(self):
        try:
            del os.environ["ONE_AUTH"]
        except KeyError:
            pass

    def test_secret(self):
        c = oca.Client('test:test')
        assert c.one_auth == 'test:test'

    def test_one_auth(self):
        os.environ["ONE_AUTH"] = os.path.join(os.path.dirname(oca.__file__),
                                              'tests/fixtures/one_auth')
        try:
            c = oca.Client()
            secret = 'test:test'
            assert c.one_auth == secret
        finally:
            os.environ["ONE_AUTH"] = ''

    def test_default_user_path(self):
        os.environ["ONE_AUTH"] = os.path.join(os.path.dirname(oca.__file__),
                                              'tests/fixtures/one_auth')
        c = oca.Client()
        assert c.one_auth == 'test:test'

    @raises(oca.OpenNebulaException)
    def test_wrong_default_user_path(self):
        oca.Client.DEFAULT_ONE_AUTH = '/ad/ads/a/das/d/sad/sad/sa/d/one_auth'
        c = oca.Client()

    @raises(oca.OpenNebulaException)
    def test_invalid_secret(self):
        os.environ["ONE_AUTH"] = os.path.join(os.path.dirname(oca.__file__),
                                              'tests/fixtures/one_auth')
        c = oca.Client('testtest')

    def test_addres(self):
        c = oca.Client('test:test', "http://8.8.8.8:2633/RPC2")
        assert c.one_address == "http://8.8.8.8:2633/RPC2"

    def test_one_xml_rpc(self):
        os.environ["ONE_AUTH"] = os.path.join(os.path.dirname(oca.__file__),
                                              'tests/fixtures/one_auth')
        os.environ["ONE_XMLRPC"] = "http://8.8.8.8:2633/RPC2"
        try:
            c = oca.Client()
            assert c.one_address == "http://8.8.8.8:2633/RPC2"
        finally:
            os.environ["ONE_XMLRPC"] = ''

    def test_defaul_xmlrpc(self):
        c = oca.Client('test:test')
        assert c.one_address == oca.Client.DEFAULT_ONE_ADDRESS

    def test_version(self):
        c = oca.Client('test:test')
        assert c.one_version is None
        c.call = Mock(return_value='1.0.0')
        assert c.version() == '1.0.0'
        c.call.assert_called_once_with('system.version')
        assert c.one_version == '1.0.0'

    def test_return_two_values_call(self):
        c = oca.Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = lambda x: [True, '2', 0]
        assert c.call('test_method') == '2'

    def test_return_one_value_call(self):
        c = oca.Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = lambda x: [True, '', 0]
        assert c.call('test_method') == ''

    @raises(oca.OpenNebulaException)
    def test_retrurn_error_code_0_call(self):
        c = oca.Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = lambda x: [False, '2', 1]
        c.call('test_method')

    @raises(oca.OpenNebulaException)
    def test_invalid_call(self):
        c = oca.Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = lambda x: [False, '2']
        c.call('test_method')

    @raises(socket.error)
    def test_connection_error(self):
        c = oca.Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = Mock(side_effect=socket.error(1))
        c.call('test_method')
