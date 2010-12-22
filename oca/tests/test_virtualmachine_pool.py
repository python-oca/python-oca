# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, VirtualMachinePool


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

