# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement


class User(PoolElement):
    METHODS = {
        'info'     : 'user.info',
        'allocate' : 'user.allocate',
        'delete'   : 'user.delete',
        'passwd'   : 'user.passwd',
        'chgrp'    : 'user.chgrp'
    }

    XML_TYPES = {
            'id'       : int,
            'gid'      : int,
            'name'     : str,
            'gname'    : str,
            'password' : str,
            'enabled'  : bool,
    }

    ELEMENT_NAME = 'USER'

    @staticmethod
    def allocate(client, user, password):
        '''
        allocates a new user in OpenNebula

        ``user``
           username for the new user

        ``password``
           password for the new user
        '''
        user_id = client.call(User.METHODS['allocate'], user, password)
        return user_id

    def __init__(self, xml, client):
        super(User, self).__init__(xml, client)
        self.id = self['ID'] if self['ID'] else None

    def change_passwd(self, new_password):
        '''
        Changes the password for the given user.

        ``new_password``
           The new password
        '''
        self.client.call(User.METHODS['passwd'], self.id, new_password)

    def chgrp(self, gid):
        '''
        Changes the main group

        ``gid``
            New group id. Set to -1 to leave the current one
        '''
        self.client.call(User.METHODS['chgrp'], self.id, gid)

    def __repr__(self):
        return '<oca.User("%s")>' % self.name


class UserPool(Pool):
    METHODS = {
            'info' : 'userpool.info',
    }

    def __init__(self, client):
        super(UserPool, self).__init__('USER_POOL', 'POOL', client)

    def _factory(self, xml):
        u = User(xml, self.client)
        u._convert_types()
        return u

