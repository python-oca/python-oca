# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement


class User(PoolElement):
    METHODS = {
        'info'     : 'user.info',
        'allocate' : 'user.allocate',
        'delete'   : 'user.delete',
        'passwd'   : 'user.passwd',
    }

    XML_TYPES = {
            'id'       : int,
            'name'     : str,
            'password' : str,
            'enabled'  : bool,
    }

    @staticmethod
    def allocate(client, user, password):
        user_id = client.call(User.METHODS['allocate'], user, password)
        return user_id

    def __init__(self, xml, client):
        super(User, self).__init__(xml, client)
        self.element_name = 'USER'
        self.id = self['ID'] if self['ID'] else None

    def change_passwd(self, new_password):
        self.client.call(User.METHODS['passwd'], self.id, new_password)

    def __repr__(self):
        return '<oca.User("%s")>' % self.name


class UserPool(Pool):
    METHODS = {
            'info' : 'userpool.info',
    }

    def __init__(self, client):
        super(UserPool, self).__init__('USER_POOL', 'POOL', client)

    def factory(self, xml):
        u = User(xml, self.client)
        u.convert_types()
        return u

    def __repr__(self):
        return '<oca.UserPool()>'

