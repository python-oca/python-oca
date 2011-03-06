# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement, Template


class Host(PoolElement):
    METHODS = {
        'info'     : 'host.info',
        'allocate' : 'host.allocate',
        'delete'   : 'host.delete',
        'enable'   : 'host.enable'
    }

    HOST_STATES = ['INIT', 'MONITORING', 'MONITORED', 'ERROR', 'DISABLED']

    SHORT_HOST_STATES = {
        'INIT'          : 'on',
        'MONITORING'    : 'on',
        'MONITORED'     : 'on',
        'ERROR'         : 'err',
        'DISABLED'      : 'off'
    }

    XML_TYPES = {
        'id'            : int,
        'name'          : str,
        'state'         : int,
        'im_mad'        : str,
        'vm_mad'        : str,
        'tm_mad'        : str,
        'last_mon_time' : int,
        'cluster'       : str,
        'template'      : ['TEMPLATE', Template],
        'host_share'    : ['HOST_SHARE', Template],
    }

    @staticmethod
    def allocate(client, hostname, im, vmm, tm):
        '''
        Adds a host to the host list

        Arguments

        ``hostname``
           Hostname machine to add

        ``im``
           Information manager'

        ``vmm``
           Virtual machine manager.

        ``tm``
           Transfer manager
        '''
        host_id = client.call(Host.METHODS['allocate'], hostname, im, vmm, tm)
        return host_id

    def __init__(self, xml, client):
        super(Host, self).__init__(xml, client)
        self.element_name = 'HOST'
        self.id = self['ID'] if self['ID'] else None

    def enable(self):
        '''
        Enable this host
        '''
        self.client.call(self.METHODS['enable'], self.id, True)

    def disable(self):
        '''
        Disable this host.
        '''
        self.client.call(self.METHODS['enable'], self.id, False)

    @property
    def str_state(self):
        '''
        String representation of host state.
        One of 'INIT', 'MONITORING', 'MONITORED', 'ERROR', 'DISABLED'
        '''
        return self.HOST_STATES[int(self.state)]

    @property
    def short_state(self):
        '''
        Short string representation of host state. One of 'on', 'off', 'err'
        '''
        return self.SHORT_HOST_STATES[self.str_state]

    def __repr__(self):
        return '<oca.Host("%s")>' % self.name


class HostPool(Pool):
    METHODS = {
            'info' : 'hostpool.info',
    }

    def __init__(self, client):
        super(HostPool, self).__init__('HOST_POOL', 'HOST', client)

    def factory(self, xml):
        h = Host(xml, self.client)
        h.convert_types()
        return h

    def __repr__(self):
        return '<oca.HostPool()>'

