# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, Host


class TestHost:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/host.xml').read()

    def test_allocate(self):
        self.client.call = Mock(return_value=7)
        host_id = Host.allocate(self.client, 'host', 'im_xen',
                               'vmm_xen', 'tm_nfs')
        assert host_id == 7

    def test_enable(self):
        self.client.call = Mock(return_value='')
        h = Host(self.xml, self.client)
        assert h.enable() is None

    def test_disable(self):
        self.client.call = Mock(return_value='')
        h = Host(self.xml, self.client)
        assert h.disable() is None

    def test_states(self):
        for i in range(len(Host.HOST_STATES)):
            h = Host('<HOST><ID>2</ID><STATE>%s</STATE></HOST>' % i,
                     self.client)
            assert h.str_state == Host.HOST_STATES[i]
            assert h.short_state == Host.SHORT_HOST_STATES[Host.HOST_STATES[i]]

    def test_repr(self):
        h = Host(self.xml, self.client)
        assert h.__repr__() == '<oca.Host("dummyhost")>'

