# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement, ET


class Image(PoolElement):
    METHODS = {
        'info'     : 'image.info',
        'allocate' : 'image.allocate',
        'delete'   : 'image.delete',
        'update'   : 'image.update',
        'rmattr'   : 'image.rmattr',
        'enable'   : 'image.enable',
        'publish'  : 'image.publish',
    }

    XML_TYPES = {
            'id'          : int,
            'uid'         : int,
            'name'        : str,
            'type'        : int,
            'public'      : int,
            'persistent'  : int,
            'regtime'     : int,
            'source'      : str,
            'state'       : int,
            'running_vms' : int,
            'template'    : ET.tostring,
    }

    IMAGE_STATES = ['INIT', 'READY', 'USED', 'DISABLED']

    SHORT_IMAGE_STATES = {
            "INIT"      : "init",
            "READY"     : "rdy",
            "USED"      : "used",
            "DISABLED"  : "disa"
    }

    IMAGE_TYPES = ['OS', 'CDROM', 'DATABLOCK']

    SHORT_IMAGE_TYPES = {
            "OS"         : "OS",
            "CDROM"      : "CD",
            "DATABLOCK"  : "DB"
    }

    @staticmethod
    def allocate(client, template):
        image_id = client.call(Image.METHODS['allocate'], template)
        return image_id

    def __init__(self, xml, client):
        super(Image, self).__init__(xml, client)
        self.element_name = 'IMAGE'
        self.id = self['ID'] if self['ID'] else None

    def update(self, attr, value):
        self.client.call(self.METHODS['update'], self.id, attr, value)

    def rmattr(self, attr):
        self.client.call(self.METHODS['rmattr'], self.id, attr)

    def enable(self):
        data = self.client.call(self.METHODS['enable'], self.id, True)

    def disable(self):
        data = self.client.call(self.METHODS['enable'], self.id, False)

    def publish(self):
        data = self.client.call(self.METHODS['publish'], self.id, True)

    def unpublish(self):
        data = self.client.call(self.METHODS['publish'], self.id, False)

    @property
    def str_state(self):
        return self.IMAGE_STATES[int(self.state)]

    @property
    def short_state(self):
        return self.SHORT_IMAGE_STATES[self.str_state]

    @property
    def str_type(self):
        return self.IMAGE_TYPES[int(self.type)]

    @property
    def short_type(self):
        return self.SHORT_IMAGE_TYPES[self.str_type]

    def __repr__(self):
        return '<oca.Image("%s")>' % self.name


class ImagePool(Pool):
    METHODS = {
            'info' : 'imagepool.info',
    }

    def __init__(self, client):
        super(ImagePool, self).__init__('IMAGE_POOL', 'POOL', client)

    def factory(self, xml):
        i = Image(xml, self.client)
        i.convert_types()
        return i

    def __repr__(self):
        return '<oca.ImagePool()>'

