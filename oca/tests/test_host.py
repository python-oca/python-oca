# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca


class TestHost:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                         'tests/fixtures/host.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=7)
        host_id = oca.Host.allocate(self.client, 'host', 'im_xen',
                               'vmm_xen', 'tm_nfs')
        assert host_id == 7

    def test_enable(self):
        self.client.call = Mock(return_value='')
        h = oca.Host(self.xml, self.client)
        h.enable()
        self.client.call.assert_called_once_with('host.enable', '7', True)

    def test_disable(self):
        self.client.call = Mock(return_value='')
        h = oca.Host(self.xml, self.client)
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
        vm_ids = h.vm_ids
        assert vm_ids == [82,84,85,95,96]
