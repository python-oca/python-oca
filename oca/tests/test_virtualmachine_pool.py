# -*- coding: UTF-8 -*-
from mock import Mock
from nose.tools import raises

from oca import Client, VirtualMachinePool
from oca.pool import WrongNameError, WrongIdError


class TestVirtualMachinePool:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/vmpool.xml').read()

    def test_vm_pool_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = VirtualMachinePool(self.client)
        pool.info()
        assert len(list(pool)) == 3

    def test_repr(self):
        pool = VirtualMachinePool(self.client)
        assert pool.__repr__() == '<oca.VirtualMachinePool()>'

    def test_iterate_before_info(self):
        pool = VirtualMachinePool(self.client)
        assert list(pool) == []

    def test_get_by_id(self):
        self.client.call = Mock(return_value=self.xml)
        pool = VirtualMachinePool(self.client)
        pool.info()
        assert  pool.get_by_id(8).id == 8

    def test_get_by_name(self):
        self.client.call = Mock(return_value=self.xml)
        pool = VirtualMachinePool(self.client)
        pool.info()
        assert  pool.get_by_name('vm-in').name == 'vm-in'

    @raises(WrongIdError)
    def test_wrong_get_by_id(self):
        self.client.call = Mock(return_value=self.xml)
        pool = VirtualMachinePool(self.client)
        pool.info()
        pool.get_by_id(1010011010)

    @raises(WrongNameError)
    def test_wrong_get_by_name(self):
        self.client.call = Mock(return_value=self.xml)
        pool = VirtualMachinePool(self.client)
        pool.info()
        pool.get_by_name('wrong-vm-name')
