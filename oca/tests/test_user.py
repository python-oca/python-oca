# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca


class TestUser:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/user.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=1)
        assert oca.User.allocate(self.client, 'jon', 'secret') == 1

    def test_repr(self):
        u = oca.User(self.xml, self.client)
        assert u.__repr__() == '<oca.User("dan")>'

    def test_change_passwd(self):
        self.client.call = Mock(return_value='')
        u = oca.User(self.xml, self.client)
        u.change_passwd('secret2')
        self.client.call.assert_called_once_with('user.passwd', '3', 'secret2')

    def test_delete(self):
        self.client.call = Mock(return_value='')
        vm = oca.User(self.xml, self.client)
        vm.delete()
        self.client.call.assert_called_once_with('user.delete', '3')

    def test_change_group(self):
        self.client.call = Mock(return_value='')
        vm = oca.User(self.xml, self.client)
        vm.chgrp(3)
        self.client.call.assert_called_once_with('user.chgrp', '3', 3)

