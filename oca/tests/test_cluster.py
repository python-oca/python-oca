# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, Cluster


class TestCluster:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/cluster.xml').read()

    def test_allocate(self):
        self.client.call = Mock(return_value=5)
        assert Cluster.allocate(self.client, self.xml) == 5

    def test_add(self):
        self.client.call = Mock(return_value='')
        c = Cluster(self.xml, self.client)
        assert c.add(2) is None

    def test_remove(self):
        self.client.call = Mock(return_value='')
        c = Cluster(self.xml, self.client)
        assert c.remove(2) is None

    def test_repr(self):
        c = Cluster(self.xml, self.client)
        assert c.__repr__() == '<oca.Cluster("Production")>'

