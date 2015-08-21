# vim:  set fileencoding=utf8
# encoding:utf8
#
# Author: Matthias Schmitz <matthias@sigxcpu.org>

import unittest
import os
import oca
from oca.exceptions import OpenNebulaException

@unittest.skipUnless(os.environ.has_key('OCA_INT_TESTS'),
                     "Skipping integration tests")
class IntTestTemplate(unittest.TestCase):
    def setUp(self):
        try:
            del os.environ["ONE_AUTH"]
        except KeyError:
            pass

        self.c = oca.Client(os.environ['OCA_INT_TESTS_ONE_AUTH'], os.environ['OCA_INT_TESTS_ONE_XMLRPC'])

    def tearDown(self):
        print "teardown"
        vmp = oca.VirtualMachinePool(self.c)
        vmp.info()
        for vm in vmp:
            if vm.name.startswith('inttest_vm_'):
                vm.delete()

    def test_allocate(self):
        templ = oca.VmTemplate.allocate(self.c, '<VMTEMPLATE><NAME>inttest01</NAME><TEMPLATE/></VMTEMPLATE>')
        templ = oca.VmTemplate.allocate(self.c, '<VMTEMPLATE><NAME>inttest02</NAME><TEMPLATE/></VMTEMPLATE>')
        templ = oca.VmTemplate.allocate(self.c, '<VMTEMPLATE><NAME>inttest03</NAME><TEMPLATE/></VMTEMPLATE>')
        templ = oca.VmTemplate.allocate(self.c, '<VMTEMPLATE><NAME>inttest04</NAME><TEMPLATE/></VMTEMPLATE>')

    def test_allocate_with_same_name(self):
        with self.assertRaises(OpenNebulaException):
            templ = oca.VmTemplate.allocate(self.c, '<VMTEMPLATE><NAME>inttest01</NAME><TEMPLATE/></VMTEMPLATE>')


    def test_update(self):
        oca.VmTemplate.allocate(self.c, '<VMTEMPLATE><NAME>inttest_update01</NAME><TEMPLATE/></VMTEMPLATE>')
        tp = oca.VmTemplatePool(self.c)
        tp.info()
        templ = tp.get_by_name('inttest_update01')
        templ.update('MEMORY=1024 CPU=2')

    def test_delete(self):
        tp = oca.VmTemplatePool(self.c)
        tp.info()
        for tpl in tp:
            if tpl.name.startswith('inttest'):
                tpl.delete()

    def test_instantiate(self):
        templ = oca.VmTemplate.allocate(self.c, '<VMTEMPLATE><NAME>inttest_instantiate_me01</NAME><MEMORY>1234</MEMORY><CPU>2</CPU></VMTEMPLATE>')
        tp = oca.VmTemplatePool(self.c)
        tp.info()
        templ = tp.get_by_name('inttest_instantiate_me01')
        templ.instantiate('inttest_vm_instantiate_me01')
        vmpool = oca.VirtualMachinePool(self.c)
        vmpool.info()
        vm = vmpool.get_by_name('inttest_vm_instantiate_me01')
        self.assertEqual(vm.name, 'inttest_vm_instantiate_me01')

