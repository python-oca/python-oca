# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, VirtualNetworkPool


class TestVirtualNetworkPool:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/vnetpool.xml').read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = VirtualNetworkPool(self.client)
        pool.info()
        assert len(list(pool)) == 2

    def test_repr(self):
        pool = VirtualNetworkPool(self.client)
        assert pool.__repr__() == '<oca.VirtualNetworkPool()>'

