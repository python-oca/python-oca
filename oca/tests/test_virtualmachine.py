# -*- coding: utf-8 -*-
import os
import unittest

from mock import Mock
from nose.tools import raises
from parameterized import parameterized_class

import oca
import oca.pool

@parameterized_class([
    {'one_version': '4.10.0'},
    {'one_version': '5.4.0'},
    {'one_version': '6.0.0'},
])
class TestVirtualMachine(unittest.TestCase):
    def setUp(self):
        self.client = oca.Client('test:test')
        self.client.call = Mock(return_value=self.one_version)
        self.client.call.reset_mock()
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/vm.xml')).read()

    def test_new_with_id(self):
        vm = oca.VirtualMachine.new_with_id(self.client, 1)
        assert vm.id == 1

    def test_acces_items_using_brackets(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        assert vm['name'] == 'vm-example'
        assert vm['ID'] == '6'
        assert vm['last_poll'] == '1277729095'
        assert vm['state'] == '3'
        assert vm['lcm_state'] == '3'
        assert vm['stime'] == '1277375180'
        assert vm['etime'] == '0'
        assert vm['deploy_id'] == 'dummy'

    def test_acces_items_not_using_brackets(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        assert vm.name == 'vm-example'
        assert vm.ID == '6'
        assert vm.last_poll == '1277729095'
        assert vm.state == '3'
        assert vm.lcm_state == '3'
        assert vm.stime == '1277375180'
        assert vm.etime == '0'
        assert vm.deploy_id == 'dummy'

    @raises(IndexError)
    def test_raise_exception_Index_Error_when_using_brackets(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        vm['wrong_name']

    def test_convert_types(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        vm._convert_types()
        assert vm.name == 'vm-example'
        assert vm.id == 6
        assert vm.last_poll == 1277729095
        assert vm.state == 3
        assert vm.lcm_state == 3
        assert vm.stime == 1277375180
        assert vm.etime == 0
        assert vm.deploy_id == 'dummy'
        assert isinstance(vm.template, oca.pool.Template)

    def test_allocate(self):
        self.client.call = Mock(return_value=3)
        assert oca.VirtualMachine.allocate(self.client, '<VM></VM>') == 3

    def test_deploy(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        self.client.call = Mock(return_value='')
        vm.deploy(3)
        self.client.call.assert_called_once_with('vm.deploy', '6', 3)

    def test_migrate(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        self.client.call = Mock(return_value='')
        vm.migrate(3)
        self.client.call.assert_called_once_with('vm.migrate', '6', 3, False)

    def test_live_migrate(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        self.client.call = Mock(return_value='')
        vm.live_migrate(3)
        self.client.call.assert_called_once_with('vm.migrate', '6', 3, True)

    def test_save_disk(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        self.client.call = Mock(return_value='')
        vm.save_disk(1, 2)
        self.client.call.assert_called_once_with('vm.savedisk', '6', 1, 2)

    def test_actions(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        for action in ['shutdown', 'shutdown_hard', 'poweroff', 'poweroff_hard',
                       'hold', 'release', 'stop', 'cancel', 'suspend', 'resume',
                       'reboot', 'finalize', 'delete', 'resched', 'unresched',
                       'terminate', 'terminate_hard']:
            self.client.call = Mock(return_value='')
            getattr(vm, action)()
            if self.one_version >= '5':
                if action in ('shutdown', 'shutdown_hard'):
                    action = action.replace("shutdown", "terminate")
            elif action in ('terminate', 'terminate_hard'):
                    action = action.replace("terminate", "shutdown")
            if action in ('shutdown_hard', 'terminate_hard', 'poweroff_hard', 'undeploy_hard'):
                action = action.replace("_", "-")
            self.client.call.assert_called_once_with('vm.action', action, '6')

    def test_repr(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        assert vm.__repr__() == '<oca.VirtualMachine("vm-example")>'

    def test_states(self):
        for i in range(len(oca.VirtualMachine.VM_STATE)):
            vm = oca.VirtualMachine('<VM><ID>2</ID><STATE>%s</STATE></VM>' % i,
                                    self.client)
            assert vm.str_state == oca.VirtualMachine.VM_STATE[i]
            state = oca.VirtualMachine.SHORT_VM_STATES[oca.VirtualMachine.VM_STATE[i]]
            assert vm.short_state == state

    def test_lcm_states(self):
        for i in range(len(oca.VirtualMachine.LCM_STATE)):
            xml = '<VM><ID>2</ID><LCM_STATE>%s</LCM_STATE></VM>' % i
            vm = oca.VirtualMachine(xml, self.client)
            assert vm.str_lcm_state == oca.VirtualMachine.LCM_STATE[i]
            lcm = oca.VirtualMachine.SHORT_LCM_STATES[oca.VirtualMachine.LCM_STATE[i]]
            assert vm.short_lcm_state == lcm

    def test_resubmit(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        self.client.call = Mock(return_value='')
        vm.resubmit()
        self.client.call.assert_called_once_with('vm.action', 'resubmit', '6')

    def test_History_repr(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        vm._convert_types()
        history = vm.history_records[0]
        assert repr(history) == '<oca.vm.History("seq=0")>'

    def test_no_history_records_element(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        vm.xml.remove(vm.xml.find('HISTORY_RECORDS'))
        vm._convert_types()
        assert vm.history_records == []

    def test_user_template_variables(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        vm._convert_types()
        greeting = vm.user_template.greeting
        assert greeting == "Hello World"

    def test_update(self):
        pass
