# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca


class TestDatastore:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/datastore.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=3)
        assert oca.Datastore.allocate(self.client, 'test') == 3

    def test_repr(self):
        self.client.call = Mock()
        datastore = oca.Datastore(self.xml, self.client)
        assert repr(datastore) == '<oca.Datastore("Custom-DS")>'

    def test_convert_types(self):
        cluster = oca.Datastore(self.xml, None)
        cluster._convert_types()
        assert cluster.id == 100
        assert cluster.name == "Custom-DS"
        assert cluster.uid == 0
        assert cluster.gid == 0
        assert cluster.uname == 'oneadmin'
        assert cluster.gname == 'oneadmin'
        assert cluster.ds_mad == 'fs'
        assert cluster.tm_mad == 'ssh'
        assert cluster.base_path == '/var/lib/one//datastores/100'
        assert cluster.type == 0
        assert cluster.disk_type == 0
        assert cluster.cluster_id == -1
        assert cluster.cluster == ""
        assert cluster.total_mb == 9952
        assert cluster.free_mb == 8999
        assert cluster.used_mb == 425
        assert cluster.image_ids == [2,3]
        assert cluster.template.disk_type == 'FILE'
