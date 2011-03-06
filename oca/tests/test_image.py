# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, Image
from oca.pool import Template


IMAGE_TEMPLATE = '''NAME          = "Ubuntu Desktop"
PATH          = /home/cloud/images/ubuntu-desktop/disk.0
PUBLIC        = YES
DESCRIPTION   = "Ubuntu 10.04 desktop for students."'''


class TestImage:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/image.xml').read()

    def test_allocate(self):
        self.client.call = Mock(return_value=2)
        assert Image.allocate(self.client, IMAGE_TEMPLATE) == 2

    def test_enable(self):
        self.client.call = Mock(return_value='')
        h = Image(self.xml, self.client)
        assert h.enable() is None

    def test_disable(self):
        self.client.call = Mock(return_value='')
        h = Image(self.xml, self.client)
        assert h.disable() is None

    def test_update(self):
        self.client.call = Mock(return_value='')
        h = Image(self.xml, self.client)
        assert h.update('name', 'New name') is None

    def test_rmattr(self):
        self.client.call = Mock(return_value='')
        h = Image(self.xml, self.client)
        assert h.rmattr('name') is None

    def test_publish(self):
        self.client.call = Mock(return_value='')
        h = Image(self.xml, self.client)
        assert h.publish() is None

    def test_unpublish(self):
        self.client.call = Mock(return_value='')
        h = Image(self.xml, self.client)
        assert h.unpublish() is None

    def test_states(self):
        for i in range(len(Image.IMAGE_STATES)):
            h = Image('<IMAGE><ID>2</ID><STATE>%s</STATE></IMAGE>' % i,
                      self.client)
            assert h.str_state == Image.IMAGE_STATES[i]
            short_image_state = Image.SHORT_IMAGE_STATES[Image.IMAGE_STATES[i]]
            assert h.short_state == short_image_state

    def test_repr(self):
        h = Image(self.xml, self.client)
        assert h.__repr__() == '<oca.Image("MATLAB install CD")>'

    def test_types(self):
        for i in range(len(Image.IMAGE_TYPES)):
            h = Image('<IMAGE><ID>2</ID><TYPE>%s</TYPE></IMAGE>' % i,
                    self.client)
            assert h.str_type == Image.IMAGE_TYPES[i]
            short_image_type = Image.SHORT_IMAGE_TYPES[Image.IMAGE_TYPES[i]]
            assert h.short_type == short_image_type

    def test_template(self):
        i = Image(self.xml, self.client)
        i.convert_types()
        assert isinstance(i.template, Template)


