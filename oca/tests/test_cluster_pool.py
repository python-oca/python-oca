# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, ClusterPool


class TestClusterPool:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/clusterpool.xml').read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = ClusterPool(self.client)
        pool.info()
        assert len(list(pool)) == 3

    def test_repr(self):
        pool = ClusterPool(self.client)
        assert pool.__repr__() == '<oca.ClusterPool()>'

