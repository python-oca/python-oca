# -*- coding: UTF-8 -*-
import os
import unittest

from mock import Mock
from xml.etree import ElementTree as ET
from parameterized import parameterized_class

import oca

VN_TEMPLATE = """NAME = "Red LAN"
TYPE = RANGED
PUBLIC = NO
BRIDGE = vbr0
NETWORK_SIZE    = C
NETWORK_ADDRESS = 192.168.0.0"""


@parameterized_class([
    {'one_version': '4.10.0'},
    {'one_version': '5.4.0'},
    {'one_version': '6.0.0'},
])
class TestVirtualNetwork(unittest.TestCase):
    # one_version = '4.10.0'

    def setUp(self):
        self.client = oca.Client('test:test')
        self.client.call = Mock(return_value=self.one_version)
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/vnet.xml')).read()

        if self.one_version >= '5':
            xml_v5 = ET.fromstring(self.xml)
            vn_mad = ET.Element('VN_MAD')
            vn_mad.text = 'vn_dummy'
            xml_v5.append(vn_mad)
            self.xml = ET.tostring(xml_v5).decode('utf-8')

    def tearDown(self):
        version = self.client.one_version
        if version is not None and version >= '5':
            xml_types = oca.VirtualNetwork.XML_TYPES
            del xml_types['vn_mad']

    def test_instantiate(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        self.client.call.assert_called_once_with('system.version')
        expected = None if self.one_version == '4.10.0' else 'vn_dummy'
        assert (getattr(h, 'vn_mad', None) == expected)

    def test_allocate(self):
        self.client.call = Mock(return_value=2)
        assert oca.VirtualNetwork.allocate(self.client, VN_TEMPLATE) == 2

    def test_publish(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        self.client.call = Mock(return_value='')
        h._convert_types()
        h.publish()
        self.client.call.assert_called_once_with('vn.publish', 3, True)

    def test_unpublish(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        self.client.call = Mock(return_value='')
        h._convert_types()
        h.unpublish()
        self.client.call.assert_called_once_with('vn.publish', 3, False)

    def test_repr(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        h._convert_types()
        assert h.__repr__() == '<oca.VirtualNetwork("Red LAN")>'

    def test_chown(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        self.client.call = Mock(return_value='')
        h._convert_types()
        h.chown(2, 2)
        self.client.call.assert_called_once_with('vn.chown', 3, 2, 2)

    def test_address_ranges(self):
        h = oca.VirtualNetwork(self.xml, self.client)
        h._convert_types()
        assert (2 == len(h.address_ranges))
        assert (1 == h.address_ranges[1].id)
        assert (0 == h.address_ranges[0].id)
        assert (" 0 68719479930 1 68719545020" == h.address_ranges[0].allocated)
        assert ("10.1.0.10" == h.address_ranges[0].ip)
        assert ("00:22:44:66:88:aa" == h.address_ranges[0].mac)
        assert (507 == h.address_ranges[0].size)
        assert ("IP4" == h.address_ranges[0].type)
