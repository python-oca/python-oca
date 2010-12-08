# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement, ET


class VirtualNetwork(PoolElement):
    METHODS = {
        'info'     : 'vn.info',
        'allocate' : 'vn.allocate',
        'delete'   : 'vn.delete',
        'publish'  : 'vn.publish',
    }

    XML_TYPES = {
            'id'       : int,
            'uid'      : int,
            'name'     : str,
            'type'     : int,
            'bridge'   : str,
            'public'   : bool,
            'template' : ET.tostring,
            'leases'   : ET.tostring,
    }

    @staticmethod
    def allocate(client, template):
        vn_id = client.call(VirtualNetwork.METHODS['allocate'], template)
        return vn_id

    def __init__(self, xml, client):
        super(VirtualNetwork, self).__init__(xml, client)
        self.element_name = 'VNET'
        self.id = self['ID'] if self['ID'] else None

    def publish(self):
        self.client.call(self.METHODS['publish'], True)

    def unpublish(self):
        self.client.call(self.METHODS['publish'], False)

    def __repr__(self):
        return '<oca.VirtualNetwork("%s")>' % self.name


class VirtualNetworkPool(Pool):
    METHODS = {
            'info' : 'vnpool.info',
    }

    def __init__(self, client):
        super(VirtualNetworkPool, self).__init__('VNET_POOL', 'VNET', client)

    def factory(self, xml):
        v = VirtualNetwork(xml, self.client)
        v.convert_types()
        return v

    def __repr__(self):
        return '<oca.VirtualNetworkPool()>'

