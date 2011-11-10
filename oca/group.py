# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement


class Group(PoolElement):
    METHODS = {
        'info'     : 'group.info',
        'allocate' : 'group.allocate',
        'delete'   : 'group.delete',
    }

    XML_TYPES = {
            'id'          : int,
            'name'        : str,
            'users'       : ['USERS', lambda users: [int(i.text) for i in users]]
    }

    ELEMENT_NAME = 'GROUP'

    @staticmethod
    def allocate(client, group_name):
        '''
        Allocates a new group in OpenNebula

        Arguments

        ``client``
           oca.Client object

        ``group``
           a string containing the group name
        '''
        group_id = client.call(Group.METHODS['allocate'], group_name)
        return group_id

    def __init__(self, xml, client):
        super(Group, self).__init__(xml, client)
        self.id = self['ID'] if self['ID'] else None

    def __repr__(self):
        return '<oca.Group("%s")>' % self.name


class GroupPool(Pool):
    METHODS = {
            'info' : 'grouppool.info',
    }

    def __init__(self, client):
        super(GroupPool, self).__init__('GROUP_POOL', 'POOL', client)

    def _factory(self, xml):
        i = Group(xml, self.client)
        i._convert_types()
        return i

