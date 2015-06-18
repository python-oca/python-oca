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
        h._convert_types()
        h.publish()
        self.client.call.assert_called_once_with('vn.publish', 3, True)

    def test_unpublish(self):
        self.client.call = Mock(return_value='')
        h = oca.VirtualNetwork(self.xml, self.client)
        h._convert_types()
        h.unpublish()
        self.client.call.assert_called_once_with('vn.publish', 3, False)

    def test_repr(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        h._convert_types()
        assert h.__repr__() == '<oca.VirtualNetwork("Red LAN")>'

    def test_chown(self):
        self.client.call = Mock(return_value='')
        h = oca.VirtualNetwork(self.xml, self.client)
        h._convert_types()
        h.chown(2, 2)
        self.client.call.assert_called_once_with('vn.chown', 3, 2, 2)

    def test_address_ranges(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        h._convert_types()
        assert(2==len(h.address_ranges))
        assert(1==h.address_ranges[1].id)
        assert(0==h.address_ranges[0].id)
        assert(" 0 68719479930 1 68719545020"==h.address_ranges[0].allocated)
        assert("10.1.0.10"==h.address_ranges[0].ip)
        assert("00:22:44:66:88:aa"==h.address_ranges[0].mac)
        assert(507==h.address_ranges[0].size)
        assert("IP4"==h.address_ranges[0].type)
