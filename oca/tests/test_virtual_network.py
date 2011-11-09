# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca


VN_TEMPLATE = '''NAME = "Red LAN"
TYPE = RANGED
PUBLIC = NO
BRIDGE = vbr0
NETWORK_SIZE    = C
NETWORK_ADDRESS = 192.168.0.0'''


class TestVirtualNetwork:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/vnet.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=2)
        assert oca.VirtualNetwork.allocate(self.client, VN_TEMPLATE) == 2

    def test_publish(self):
        self.client.call = Mock(return_value='')
        h = oca.VirtualNetwork(self.xml, self.client)
        h.publish()
        self.client.call.assert_called_once_with('vn.publish', '3', True)

    def test_unpublish(self):
        self.client.call = Mock(return_value='')
        h = oca.VirtualNetwork(self.xml, self.client)
        h.unpublish()
        self.client.call.assert_called_once_with('vn.publish', '3', False)

    def test_repr(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        assert h.__repr__() == '<oca.VirtualNetwork("Red LAN")>'

    def test_chown(self):
        self.client.call = Mock(return_value='')
        h = oca.VirtualNetwork(self.xml, self.client)
        h.chown(2, 2)
        self.client.call.assert_called_once_with('vn.chown', '3', 2, 2)
