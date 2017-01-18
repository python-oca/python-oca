# -*- coding: UTF-8 -*-
import os
import unittest

from mock import Mock

import oca


class TestVmTemplate(unittest.TestCase):
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/template.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=3)
        assert oca.VmTemplate.allocate(self.client, 'name=a') == 3

    def test_delete(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.delete()
        self.client.call.assert_called_once_with('template.delete',
                                                            '1', False)

    def test_delete_with_disk_images(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.delete(delete_disk_images=True)
        self.client.call.assert_called_once_with('template.delete',
                                                            '1', True)

    def test_update(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.update('name=b')
        self.client.call.assert_called_once_with('template.update',
                                                            '1', 'name=b', 0)

    def test_publish(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.publish()
        self.client.call.assert_called_once_with('template.publish',
                                                            '1', True)

    def test_unpublish(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.unpublish()
        self.client.call.assert_called_once_with('template.publish',
                                                            '1', False)

    def test_chown(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.chown(2, 3)
        self.client.call.assert_called_once_with('template.chown',
                                                            '1', 2, 3)

    def test_clone(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.clone('cloned')
        self.client.call.assert_called_once_with('template.clone',
                                                            '1', 'cloned', False)

    def test_clone_with_disk_images(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.clone('cloned', clone_disk_images=True)
        self.client.call.assert_called_once_with('template.clone',
                                                            '1', 'cloned', True)

    def test_instantiate_with_default_name(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.instantiate()
        self.client.call.assert_called_once_with('template.instantiate',
                                                            '1', '', False, '', False)

    def test_instantiate_with_custom_name(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.instantiate('asd')
        self.client.call.assert_called_once_with('template.instantiate',
                                                            '1', 'asd', False, '', False)

    def test_instantiate_with_default_name_and_context(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.instantiate('', False, 'VCPU=4')
        self.client.call.assert_called_once_with('template.instantiate',
                                                            '1', '', False, 'VCPU=4', False)

    def test_instantiate_with_custom_name_and_context(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.instantiate('asd', False, 'VCPU=4')
        self.client.call.assert_called_once_with('template.instantiate',
                                                            '1', 'asd', False, 'VCPU=4', False)

    def test_instantiate_with_disk_images(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        template.instantiate('', False, '', True)
        self.client.call.assert_called_once_with('template.instantiate',
                                                            '1', '', False, '', True)

    def test_repr(self):
        self.client.call = Mock()
        template = oca.VmTemplate(self.xml, self.client)
        assert repr(template) == '<oca.VmTemplate("test1")>'
