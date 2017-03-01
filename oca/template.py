# -*- coding: UTF-8 -*-
from .pool import Pool, PoolElement, Template


class VmTemplate(PoolElement):
    METHODS = {
        'info': 'template.info',
        'allocate': 'template.allocate',
        'delete': 'template.delete',
        'update': 'template.update',
        'publish': 'template.publish',
        'chown': 'template.chown',
        'instantiate': 'template.instantiate',
        'clone': 'template.clone',
    }

    XML_TYPES = {
        'id': int,
        'uid': int,
        'gid': int,
        'name': str,
        'uname': str,
        'gname': str,
        'regtime': int,
        'template': ['TEMPLATE', Template]
    }

    ELEMENT_NAME = 'VMTEMPLATE'

    @staticmethod
    def allocate(client, template):
        """
        Allocates a new template in OpenNebula

        ``client``
           oca.Client object

        ``template``
           a string containing the template contents
        """
        template_id = client.call(VmTemplate.METHODS['allocate'], template)
        return template_id

    def __init__(self, xml, client):
        super(VmTemplate, self).__init__(xml, client)
        self.id = self['ID'] if self['ID'] else None

    def update(self, template, update_type=0):
        """
        Replaces the template contents.

        ``template``
            The new template contents.
        ``update_type``
            Update type: 0: replace the whole template. 1: Merge new template with the existing one.
        """
        self.client.call(VmTemplate.METHODS['update'], self.id, template, update_type)

    def publish(self):
        """
        Publishes a template.
        """
        self.client.call(VmTemplate.METHODS['publish'], self.id, True)

    def unpublish(self):
        """
        Unpublishes a template.
        """
        self.client.call(VmTemplate.METHODS['publish'], self.id, False)

    def chown(self, uid=-1, gid=-1):
        """
        Changes the ownership of a template.

        ``uid``
            The User ID of the new owner. If set to -1, the owner is not changed.
        ``gid``
             The Group ID of the new group. If set to -1, the group is not changed.
        """
        self.client.call(VmTemplate.METHODS['chown'], self.id, uid, gid)

    def instantiate(self, name='', pending=False, extra_template=''):
        """
        Creates a VM instance from a VmTemplate

        ``name``
            name of the VM instance
        ``pending``
            False to create the VM on pending (default), True to create it on hold.
        ``extra_template``
            A string containing an extra template to be merged with the one being instantiated
        """
        return self.client.call(VmTemplate.METHODS['instantiate'], self.id, name, pending, extra_template)

    def __repr__(self):
        return '<oca.VmTemplate("%s")>' % self.name


class VmTemplatePool(Pool):
    METHODS = {
        'info': 'templatepool.info',
    }

    def __init__(self, client):
        super(VmTemplatePool, self).__init__('VMTEMPLATE_POOL', 'VMTEMPLATE', client)

    # def info(self,

    def _factory(self, xml):
        i = VmTemplate(xml, self.client)
        i._convert_types()
        return i
