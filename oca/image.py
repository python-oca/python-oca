# -*- coding: UTF-8 -*-
from pool import Pool, PoolElement, Template


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
            'template'     : ['TEMPLATE', Template],
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
        '''
        Allocates a new image in OpenNebula

        Arguments

        ``client``
           oca.Client object

        ``template``
           a string containing the template of the image
        '''
        image_id = client.call(Image.METHODS['allocate'], template)
        return image_id

    def __init__(self, xml, client):
        super(Image, self).__init__(xml, client)
        self.element_name = 'IMAGE'
        self.id = self['ID'] if self['ID'] else None

    def update(self, attr, value):
        '''
        Modifies an image attribute

        Arguments

        ``attr``
           the name of the attribute to update

        ``value``
           the new value for the attribute
        '''
        self.client.call(self.METHODS['update'], self.id, attr, value)

    def rmattr(self, attr):
        '''
        Removes an image attribute

        Arguments

        ``attr``
           the name of the attribute to remove
        '''
        self.client.call(self.METHODS['rmattr'], self.id, attr)

    def enable(self):
        '''
        Enables an image
        '''
        data = self.client.call(self.METHODS['enable'], self.id, True)

    def disable(self):
        '''
        Disables an image
        '''
        data = self.client.call(self.METHODS['enable'], self.id, False)

    def publish(self):
        '''
        Publishes an image
        '''
        data = self.client.call(self.METHODS['publish'], self.id, True)

    def unpublish(self):
        '''
        Unpublishes an image
        '''
        data = self.client.call(self.METHODS['publish'], self.id, False)

    @property
    def str_state(self):
        '''
        String representation of image state.
        One of 'INIT', 'READY', 'USED', 'DISABLED'
        '''
        return self.IMAGE_STATES[int(self.state)]

    @property
    def short_state(self):
        '''
        Short string representation of image state.
        One of 'init', 'rdy', 'used', 'disa'
        '''
        return self.SHORT_IMAGE_STATES[self.str_state]

    @property
    def str_type(self):
        '''
        String representation of image type.
        One of 'OS', 'CDROM', 'DATABLOCK'
        '''
        return self.IMAGE_TYPES[int(self.type)]

    @property
    def short_type(self):
        '''
        Short string representation of image type.
        One of 'OS', 'CD', 'DB'
        '''
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

