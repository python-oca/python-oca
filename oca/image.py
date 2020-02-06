# -*- coding: utf-8 -*-
from .pool import Pool, PoolElement, Template, extractString


class Image(PoolElement):
    METHODS = {
        'info': 'image.info',
        'allocate': 'image.allocate',
        'delete': 'image.delete',
        'update': 'image.update',
        'enable': 'image.enable',
        'publish': 'image.publish',
        'chmod': 'image.chmod',
        'chown': 'image.chown',
        'persistent': 'image.persistent',
        'clone': 'image.clone',
    }

    XML_TYPES = {
        'id': int,
        'uid': int,
        'gid': int,
        'uname': extractString,
        'gname': extractString,
        'name': extractString,
        # 'permissions' : ???,
        'type': int,
        'disk_type': int,
        'persistent': int,
        'regtime': int,
        'source': extractString,
        'path': extractString,
        'fstype': extractString,
        'size': int,
        'state': int,
        'running_vms': int,
        'cloning_ops': int,
        'cloning_id': int,
        'datastore_id': int,
        'datastore': extractString,
        'vm_ids': ["VMS", lambda vms: [int(vm_id.text) for vm_id in vms]],
        'clone_ids': ["CLONES", lambda clones: [int(clone_id.text) for clone_id in clones]],
        'template': ['TEMPLATE', Template],
    }

    INIT = 0
    READY = 1
    USED = 2
    DISABLED = 3
    IMAGE_STATES = ['INIT', 'READY', 'USED', 'DISABLED', 'LOCKED', 'ERROR', 'CLONE', 'DELETE', 'USED_PERS']

    SHORT_IMAGE_STATES = {
        "INIT": "init",
        "READY": "rdy",
        "USED": "used",
        "DISABLED": "disa",
        "LOCKED": "lock",
        "ERROR": "err",
        "CLONE": "clon",
        "DELETE": "dele",
        "USED_PERS": "used"
    }

    IMAGE_TYPES = ['OS', 'CDROM', 'DATABLOCK']

    SHORT_IMAGE_TYPES = {
        "OS": "OS",
        "CDROM": "CD",
        "DATABLOCK": "DB"
    }

    ELEMENT_NAME = 'IMAGE'

    @staticmethod
    def allocate(client, template, datastore):
        """
        Allocates a new image in OpenNebula

        Arguments

        ``client``
           oca.Client object

        ``template``
           a string containing the template of the image
        ``datastore``
          the datastore id where the image is to be allocated
        """
        image_id = client.call(Image.METHODS['allocate'], template, datastore)
        return image_id

    def __init__(self, xml, client):
        super(Image, self).__init__(xml, client)
        self.id = self['ID'] if self['ID'] else None

    def update(self, template):
        """
        Replaces the template contents

        Arguments

        ``template``
            New template contents
        """
        self.client.call(self.METHODS['update'], self.id, template)

    def enable(self):
        """
        Enables an image
        """
        self.client.call(self.METHODS['enable'], self.id, True)

    def disable(self):
        """
        Disables an image
        """
        self.client.call(self.METHODS['enable'], self.id, False)

    def publish(self):
        """
        Publishes an image
        """
        self.client.call(self.METHODS['publish'], self.id, True)

    def unpublish(self):
        """
        Unpublishes an image
        """
        self.client.call(self.METHODS['publish'], self.id, False)

    def set_persistent(self):
        """
        Set Image as persistent
        """
        self.client.call(self.METHODS['persistent'], self.id, True)

    def set_nonpersistent(self):
        """
        Set Image as non persistent
        """
        self.client.call(self.METHODS['persistent'], self.id, False)

    def chown(self, uid, gid):
        """
        Changes the owner/group

        Arguments

        ``uid``
            New owner id. Set to -1 to leave current value
        ``gid``
            New group id. Set to -1 to leave current value
        """
        self.client.call(self.METHODS['chown'], self.id, uid, gid)

    def chmod(self, owner_u, owner_m, owner_a, group_u, group_m, group_a, other_u, other_m, other_a):
        """
        Changes the permission bits

        Arguments

        ``owner_u``
            User USE bit. Set to -1 to leave current value
        ``owner_m``
            User MANAGE bit. Set to -1 to leave current value
        ``owner_a``
            User ADMIN bit. Set to -1 to leave current value
        ``group_u``
            Group USE bit. Set to -1 to leave current value
        ``group_m``
            Group MANAGE bit. Set to -1 to leave current value
        ``group_a``
            Group ADMIN bit. Set to -1 to leave current value
        ``other_u``
            Other USE bit. Set to -1 to leave current value
        ``other_m``
            Other MANAGE bit. Set to -1 to leave current value
        ``other_a``
            Other ADMIN bit. Set to -1 to leave current value
        """
        self.client.call(self.METHODS['chmod'], self.id, owner_u, owner_m, owner_a, group_u, group_m, group_a, other_u,
                         other_m, other_a)

    def clone(self, name='', datastore_id=-1):
        """
        Creates a clone of an image
        ``name``
            name of a target element
        ``datastore_id``
            The ID of the target datastore. Optional, can be set to -1 to use the current one.
        """
        self.client.call(self.METHODS['clone'], self.id, name, datastore_id)

    @property
    def str_state(self):
        """
        String representation of image state.
        One of 'INIT', 'READY', 'USED', 'DISABLED', 'LOCKED', 'ERROR', 'CLONE', 'DELETE', 'USED_PERS'
        """
        return self.IMAGE_STATES[int(self.state)]

    @property
    def short_state(self):
        """
        Short string representation of image state.
        One of 'init', 'rdy', 'used', 'disa', 'lock', 'err', 'clon', 'dele', 'used'
        """
        return self.SHORT_IMAGE_STATES[self.str_state]

    @property
    def str_type(self):
        """
        String representation of image type.
        One of 'OS', 'CDROM', 'DATABLOCK'
        """
        return self.IMAGE_TYPES[int(self.type)]

    @property
    def short_type(self):
        """
        Short string representation of image type.
        One of 'OS', 'CD', 'DB'
        """
        return self.SHORT_IMAGE_TYPES[self.str_type]

    def __repr__(self):
        return '<oca.Image("%s")>' % self.name


class ImagePool(Pool):
    METHODS = {
        'info': 'imagepool.info',
    }

    def __init__(self, client):
        super(ImagePool, self).__init__('IMAGE_POOL', 'IMAGE', client)

    def _factory(self, xml):
        i = Image(xml, self.client)
        i._convert_types()
        return i
