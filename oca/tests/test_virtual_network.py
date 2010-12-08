# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, VirtualNetwork


VN_TEMPLATE = '''NAME = "Red LAN"
TYPE = RANGED
PUBLIC = NO
BRIDGE = vbr0
NETWORK_SIZE    = C
NETWORK_ADDRESS = 192.168.0.0'''


class TestVirtualNetwork:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/vnet.xml').read()

    def test_allocate(self):
        self.client.call = Mock(return_value=2)
        assert VirtualNetwork.allocate(self.client, VN_TEMPLATE) == 2

    def test_publish(self):
        self.client.call = Mock(return_value='')
        h = VirtualNetwork(self.xml, self.client)
        assert h.publish() is None

    def test_unpublish(self):
        self.client.call = Mock(return_value='')
        h = VirtualNetwork(self.xml, self.client)
        assert h.unpublish() is None

    def test_repr(self):
        h = VirtualNetwork(self.xml, self.client)
        assert h.__repr__() == '<oca.VirtualNetwork("Red LAN")>'

