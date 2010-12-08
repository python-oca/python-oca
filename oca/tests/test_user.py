# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, User


class TestUser:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/user.xml').read()

    def test_allocate(self):
        self.client.call = Mock(return_value=1)
        assert User.allocate(self.client, 'jon', 'secret') == 1

    def test_repr(self):
        u = User(self.xml, self.client)
        assert u.__repr__() == '<oca.User("dan")>'

    def test_change_passwd(self):
        self.client.call = Mock(return_value='')
        u = User(self.xml, self.client)
        assert u.change_passwd('secret2') is None

    def test_delete(self):
        self.client.call = Mock(return_value='')
        vm = User(self.xml, self.client)
        assert vm.delete() is None

