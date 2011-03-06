# -*- coding: UTF-8 -*-
from mock import Mock
from nose.tools import raises

from oca import Client, os, OpenNebulaException, socket


class TestClient:
    def test_secret(self):
        c = Client('test:test')
        assert c.one_auth == 'test:a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'

    def test_one_auth(self):
        os.environ["ONE_AUTH"] = 'fixtures/one_auth'
        try:
            c = Client()
            secret = 'test:a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'
            assert c.one_auth == secret
        finally:
            os.environ["ONE_AUTH"] = ''

    def test_default_user_path(self):
        Client.DEFAULT_ONE_AUTH = 'fixtures/one_auth'
        c = Client()
        assert c.one_auth == 'test:a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'

    @raises(OpenNebulaException)
    def test_wrong_default_user_path(self):
        Client.DEFAULT_ONE_AUTH = '/ad/ads/a/das/d/sad/sad/sa/d/one_auth'
        c = Client()

    @raises(OpenNebulaException)
    def test_invalid_secret(self):
        c = Client('testtest')

    def test_with_plain(self):
        c = Client('test:plain:a94a8fe5ccb19ba61c4c0873d391e987982fbbd3')
        assert c.one_auth == 'test:a94a8fe5ccb19ba61c4c0873d391e987982fbbd3'

    def test_addres(self):
        c = Client('test:test',  "http://8.8.8.8:2633/RPC2")
        assert c.one_address == "http://8.8.8.8:2633/RPC2"

    def test_one_xml_rpc(self):
        os.environ["ONE_XMLRPC"] = "http://8.8.8.8:2633/RPC2"
        try:
            c = Client()
            assert c.one_address == "http://8.8.8.8:2633/RPC2"
        finally:
            os.environ["ONE_XMLRPC"] = ''

    def test_defaul_xmlrpc(self):
        c = Client('test:test')
        assert c.one_address == Client.DEFAULT_ONE_ADDRESS

    def test_return_two_values_call(self):
        c = Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = lambda x: [1, '2']
        assert c.call('test_method') == '2'

    def test_return_one_value_call(self):
        c = Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = lambda x: [1]
        assert c.call('test_method') == ''

    @raises(OpenNebulaException)
    def test_retrurn_error_code_0_call(self):
        c = Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = lambda x: [0, '2']
        c.call('test_method')

    @raises(socket.error)
    def test_connection_error(self):
        c = Client('test:test')
        c.server.one = Mock()
        c.server.one.test_method = Mock(side_effect=socket.error(1))
        c.call('test_method')

