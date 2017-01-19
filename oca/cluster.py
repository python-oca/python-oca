# -*- coding: UTF-8 -*-
from .pool import Pool, PoolElement, Template, extractString


class Cluster(PoolElement):
    METHODS = {
        # 'info'     : 'cluster.info',
        'allocate': 'cluster.allocate',
        'delete': 'cluster.delete',
        # 'enable'   : 'cluster.enable',
        # 'update'   : 'cluster.update'
    }

    XML_TYPES = {
        'id': int,
        'name': extractString,
        'host_ids': ['HOSTS', lambda hosts: [int(host_id.text) for host_id in hosts]],
        'datastore_ids': ['DATASTORES', lambda datastores: [int(datastore_id.text) for datastore_id in datastores]],
        'vnet_ids': ['VNETS', lambda vnets: [int(vnet_id.text) for vnet_id in vnets]],
        'template': ['TEMPLATE', Template],
    }

    ELEMENT_NAME = 'CLUSTER'

    @staticmethod
    def allocate(client, cluster_name):
        """
        Adds a cluster to the cluster list

        Arguments

        ``cluster_name``
           Clustername to add
        """
        cluster_id = client.call(Cluster.METHODS['allocate'], cluster_name)
        return cluster_id

    def __init__(self, xml, client):
        super(Cluster, self).__init__(xml, client)
        self._convert_types()

    def __repr__(self):
        return '<oca.Cluster("%s")>' % self.name


class ClusterPool(Pool):
    METHODS = {
        'info': 'clusterpool.info',
    }

    def __init__(self, client):
        super(ClusterPool, self).__init__('CLUSTER_POOL', 'CLUSTER', client)

    def _factory(self, xml):
        c = Cluster(xml, self.client)
        return c
