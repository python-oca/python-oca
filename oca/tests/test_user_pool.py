# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, UserPool


class TestUserPool:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/userpool.xml').read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = UserPool(self.client)
        pool.info()
        assert len(list(pool)) == 2

    def test_repr(self):
        pool = UserPool(self.client)
        assert pool.__repr__() == '<oca.UserPool()>'

