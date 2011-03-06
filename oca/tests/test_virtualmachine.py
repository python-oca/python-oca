# -*- coding: UTF-8 -*-
from mock import Mock
from nose.tools import raises

from oca import Client, VirtualMachine
from oca.pool import Template


class TestUser:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/vm.xml').read()

    def test_acces_items_using_brackets(self):
        vm = VirtualMachine(self.xml, self.client)
        assert vm['name'] == 'vm-example'
        assert vm['ID'] == '6'
        assert vm['last_poll'] == '1277729095'
        assert vm['state'] == '3'
        assert vm['lcm_state'] == '3'
        assert vm['stime'] == '1277375180'
        assert vm['etime'] == '0'
        assert vm['deploy_id'] == 'dummy'
        assert vm['memory'] == '512'
        assert vm['cpu'] == '1'
        assert vm['net_tx'] == '12345'
        assert vm['net_rx'] == '0'

    def test_acces_items_not_using_brackets(self):
        vm = VirtualMachine(self.xml, self.client)
        assert vm.name == 'vm-example'
        assert vm.ID == '6'
        assert vm.last_poll == '1277729095'
        assert vm.state == '3'
        assert vm.lcm_state == '3'
        assert vm.stime == '1277375180'
        assert vm.etime == '0'
        assert vm.deploy_id == 'dummy'
        assert vm.memory == '512'
        assert vm.cpu == '1'
        assert vm.net_tx == '12345'
        assert vm.net_rx == '0'

    @raises(IndexError)
    def test_raise_exception_Index_Error_when_using_brackets(self):
        vm = VirtualMachine(self.xml, self.client)
        vm['wrong_name']

    def test_convert_types(self):
        vm = VirtualMachine(self.xml, self.client)
        vm.convert_types()
        assert vm.name == 'vm-example'
        assert vm.id == 6
        assert vm.last_poll == 1277729095
        assert vm.state == 3
        assert vm.lcm_state == 3
        assert vm.stime == 1277375180
        assert vm.etime == 0
        assert vm.deploy_id == 'dummy'
        assert vm.memory == 512
        assert vm.cpu == 1
        assert vm.net_tx == 12345
        assert vm.net_rx == 0
        assert isinstance(vm.template, Template)

    def test_allocate(self):
        self.client.call = Mock(return_value=3)
        assert VirtualMachine.allocate(self.client, '<VM></VM>') == 3

    def test_deploy(self):
        self.client.call = Mock(return_value='')
        vm = VirtualMachine(self.xml, self.client)
        assert vm.deploy(3) is None

    def test_migrate(self):
        self.client.call = Mock(return_value='')
        vm = VirtualMachine(self.xml, self.client)
        assert vm.migrate(3) is None

    def test_live_migrate(self):
        self.client.call = Mock(return_value='')
        vm = VirtualMachine(self.xml, self.client)
        assert vm.live_migrate(3) is None

    def test_save_disk(self):
        self.client.call = Mock(return_value='')
        vm = VirtualMachine(self.xml, self.client)
        assert vm.save_disk(1, 2) is None

    def test_actions(self):
        client = Client('test:test')
        vm = VirtualMachine(self.xml, self.client)
        for action in ['shutdown', 'hold', 'release', 'stop', 'cancel',
                'suspend', 'resume', 'restart', 'finalize']:
            self.client.call = Mock(return_value='')
            assert getattr(vm, action)() is None

    def test_repr(self):
        vm = VirtualMachine(self.xml, self.client)
        assert vm.__repr__() == '<oca.VirtualMachine("vm-example")>'

    def test_states(self):
        for i in range(len(VirtualMachine.VM_STATE)):
            vm = VirtualMachine('<VM><ID>2</ID><STATE>%s</STATE></VM>' % i,
                                self.client)
            assert vm.str_state == VirtualMachine.VM_STATE[i]
            state = VirtualMachine.SHORT_VM_STATES[VirtualMachine.VM_STATE[i]]
            assert vm.short_state == state

    def test_lcm_states(self):
        for i in range(len(VirtualMachine.LCM_STATE)):
            xml = '<VM><ID>2</ID><LCM_STATE>%s</LCM_STATE></VM>' % i
            vm = VirtualMachine(xml, self.client)
            assert vm.str_lcm_state == VirtualMachine.LCM_STATE[i]
            lcm = VirtualMachine.SHORT_LCM_STATES[VirtualMachine.LCM_STATE[i]]
            assert vm.short_lcm_state == lcm

