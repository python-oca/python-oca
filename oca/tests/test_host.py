# -*- coding: UTF-8 -*-
import os
import unittest

from mock import Mock
from xml.etree import ElementTree as ET
from parameterized import parameterized_class

import oca


@parameterized_class([
    {'one_version': '4.10.0'},
    {'one_version': '5.4.0'},
    {'one_version': '6.0.0'},
])
class TestHost(unittest.TestCase):
    def setUp(self):
        self.client = oca.Client('test:test')
        self.client.call = Mock(return_value=self.one_version)
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/host.xml')).read()

        if self.one_version >= '5':
            xml_v5 = ET.fromstring(self.xml)
            [xml_v5.remove(vn_mad) for vn_mad in xml_v5.findall('VN_MAD')]
            self.xml = ET.tostring(xml_v5).decode('utf-8')

    def tearDown(self):
        version = self.client.one_version
        if version is not None and version >= '5':
            xml_types = oca.Host.XML_TYPES
            xml_types['vn_mad'] = oca.pool.extractString

    def test_instantiate(self):
        h = oca.Host(self.xml, self.client)
        self.client.call.assert_called_once_with('system.version')
        expected = 'vn_dummy' if self.one_version == '4.10.0' else None
        assert (getattr(h, 'vn_mad', None) == expected)

    def test_allocate(self):
        self.client.call = Mock(return_value=7)
        host_id = oca.Host.allocate(self.client, 'host', 'im_xen',
                                    'vmm_xen', 'tm_nfs')
        assert host_id == 7

    def test_enable(self):
        h = oca.Host(self.xml, self.client)
        self.client.call = Mock(return_value='')
        h.enable()
        self.client.call.assert_called_once_with('host.enable', '7', True)

    def test_disable(self):
        h = oca.Host(self.xml, self.client)
        self.client.call = Mock(return_value='')
        h.disable()
        self.client.call.assert_called_once_with('host.enable', '7', False)

    def test_states(self):
        for i in range(len(oca.Host.HOST_STATES)):
            h = oca.Host('<HOST><ID>2</ID><STATE>{0}</STATE></HOST>'.format(i),
                         self.client)
            assert h.str_state == oca.Host.HOST_STATES[i]
            assert h.short_state == oca.Host.SHORT_HOST_STATES[oca.Host.HOST_STATES[i]]

    def test_repr(self):
        h = oca.Host(self.xml, self.client)
        assert h.__repr__() == '<oca.Host("dummyhost")>'

    def test_host_share_repr(self):
        h = oca.Host(self.xml, self.client)
        h._convert_types()
        share = h.host_share
        assert repr(share) == '<oca.vm.HostShare()>'

    def test_host_vm_ids(self):
        h = oca.Host(self.xml, self.client)
        h._convert_types()
        vm_ids = list(h.vm_ids)
        assert vm_ids == [82, 84, 85, 95, 96]
