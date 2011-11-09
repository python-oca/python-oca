# -*- coding: UTF-8 -*-
import os

from mock import Mock
from nose.tools import raises

import oca
import oca.pool


class TestVirtualMachinePool:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/vmpool.xml')).read()

    def test_vm_pool_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VirtualMachinePool(self.client)
        pool.info()
        assert len(list(pool)) == 3

    def test_iterate_before_info(self):
        pool = oca.VirtualMachinePool(self.client)
        assert list(pool) == []

    def test_get_by_id(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VirtualMachinePool(self.client)
        pool.info()
        assert  pool.get_by_id(8).id == 8

    def test_get_by_name(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VirtualMachinePool(self.client)
        pool.info()
        assert  pool.get_by_name('vm-in').name == 'vm-in'

    @raises(oca.pool.WrongIdError)
    def test_wrong_get_by_id(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VirtualMachinePool(self.client)
        pool.info()
        pool.get_by_id(1010011010)

    @raises(oca.pool.WrongNameError)
    def test_wrong_get_by_name(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VirtualMachinePool(self.client)
        pool.info()
        pool.get_by_name('wrong-vm-name')
