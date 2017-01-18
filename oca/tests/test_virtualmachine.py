# -*- coding: UTF-8 -*-
import os
import unittest

from mock import Mock
from nose.tools import raises

import oca
import oca.pool


class TestVirtualMachine(unittest.TestCase):
    def setUp(self):
        self.client = oca.Client('test:test')
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
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
        vm.deploy(3)
        self.client.call.assert_called_once_with('vm.deploy', '6', 3)

    def test_migrate(self):
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
        vm.migrate(3)
        self.client.call.assert_called_once_with('vm.migrate', '6', 3, False)

    def test_live_migrate(self):
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
        vm.live_migrate(3)
        self.client.call.assert_called_once_with('vm.migrate', '6', 3, True)

    def test_save_disk(self):
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
        vm.save_disk(1, 2)
        self.client.call.assert_called_once_with('vm.savedisk', '6', 1, 2)

    def test_actions(self):
        oca.client = oca.Client('test:test')
        vm = oca.VirtualMachine(self.xml, self.client)
        for action in ['terminate', 'terminate_hard', 'poweroff', 'poweroff_hard',
                       'hold', 'release', 'stop', 'cancel', 'suspend', 'resume',
                       'reboot', 'finalize', 'resched', 'unresched',
                       'undeploy', 'undeploy_hard']:
            self.client.call = Mock(return_value='')
            getattr(vm, action)()
            if action in ('terminate_hard', 'poweroff_hard', 'undeploy_hard', 'reboot_hard'):
                action = action.replace("_", "-")
            self.client.call.assert_called_once_with('vm.action', action, '6')

    def test_delete(self):
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
        vm.delete()
        self.client.call.assert_called_once_with('vm.recover', '6', 3)

    def test_delete_with_recreate(self):
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
        vm.delete(recreate=True)
        self.client.call.assert_called_once_with('vm.recover', '6', 4)

    def test_updateconf(self):
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
        _conf = """CONTEXT = [ETH0_IP = 10.0.0.1\nNETWORK = YES]"""
        vm.updateconf(_conf)
        self.client.call.assert_called_once_with('vm.updateconf', '6', _conf)

    def test_recover(self):
        vm = oca.VirtualMachine(self.xml, self.client)
        for operation in [0, 1, 2, 3, 4]:
            self.client.call = Mock(return_value='')
            vm.recover(operation)
            self.client.call.assert_called_once_with('vm.recover', '6', operation)

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
        self.client.call = Mock(return_value='')
        vm = oca.VirtualMachine(self.xml, self.client)
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
