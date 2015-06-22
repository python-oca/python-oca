# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca


class TestCluster:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/cluster.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=3)
        assert oca.Cluster.allocate(self.client, 'test') == 3

    def test_repr(self):
        self.client.call = Mock()
        cluster = oca.Cluster(self.xml, self.client)
        assert repr(cluster) == '<oca.Cluster("oneCluster")>'

    def test_convert_types(self):
        cluster = oca.Cluster(self.xml, None)
        cluster._convert_types()
        assert cluster.id == 101
        assert cluster.name == "oneCluster"
        assert cluster.host_ids == [2,3]
        assert cluster.datastore_ids == [4,5]
        assert cluster.vnet_ids == [6,7]
        assert cluster.template.reserved_cpu is None
