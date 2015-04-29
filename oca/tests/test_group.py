# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca


class TestGroup:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/group.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=3)
        assert oca.Group.allocate(self.client, 'test') == 3

    def test_delete(self):
        self.client.call = Mock()
        group = oca.Group(self.xml, self.client)
        group.delete()
        self.client.call.assert_called_once_with('group.delete', '1')

    def test_repr(self):
        self.client.call = Mock()
        group = oca.Group(self.xml, self.client)
        assert repr(group) == '<oca.Group("users")>'

    def test_convert_types(self):
        group = oca.Group(self.xml, None)
        group._convert_types()
        assert group.id == 1
        assert group.name == "users"
        assert group.template.hello == "world"
        assert group.users == [1,2]

