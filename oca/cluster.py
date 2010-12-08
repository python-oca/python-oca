# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement


class Cluster(PoolElement):
    METHODS = {
        'info'     : 'cluster.info',
        'allocate' : 'cluster.allocate',
        'delete'   : 'cluster.delete',
        'add'      : 'cluster.add',
        'remove'   : 'cluster.remove',
    }

    XML_TYPES = {
            'id'       : int,
            'name'     : str,
    }

    @staticmethod
    def allocate(client, name):
        cluster_id = client.call(Cluster.METHODS['allocate'], name)
        return cluster_id

    def __init__(self, xml, client):
        super(Cluster, self).__init__(xml, client)
        self.element_name = 'CLUSTER'
        self.id = self['ID'] if self['ID'] else None

    def add(self, host_id):
        self.client.call(self.METHODS['add'], host_id, self.id)

    def remove(self, host_id):
        self.client.call(self.METHODS['remove'], host_id)

    def __repr__(self):
        return '<oca.Cluster("%s")>' % self.name


class ClusterPool(Pool):
    METHODS = {
            'info' : 'clusterpool.info',
    }

    def __init__(self, client):
        super(ClusterPool, self).__init__('CLUSTER_POOL', 'CLUSTER', client)

    def factory(self, xml):
        c = Cluster(xml, self.client)
        c.convert_types()
        return c

    def __repr__(self):
        return '<oca.ClusterPool()>'

