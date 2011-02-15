# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, HostPool


class TestHostPool:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/hostpool.xml').read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = HostPool(self.client)
        pool.info()
        assert len(list(pool)) == 2

    def test_repr(self):
        pool = HostPool(self.client)
        assert pool.__repr__() == '<oca.HostPool()>'

