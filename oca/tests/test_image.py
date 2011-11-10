# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca
import oca.pool


IMAGE_TEMPLATE = '''NAME          = "Ubuntu Desktop"
PATH          = /home/cloud/images/ubuntu-desktop/disk.0
PUBLIC        = YES
DESCRIPTION   = "Ubuntu 10.04 desktop for students."'''


class TestImage:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                         'tests/fixtures/image.xml')).read()

    def test_allocate(self):
        self.client.call = Mock(return_value=2)
        assert oca.Image.allocate(self.client, IMAGE_TEMPLATE) == 2

    def test_enable(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        h.enable()
        self.client.call.assert_called_once_with('image.enable', '1', True)

    def test_disable(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        h.disable()
        self.client.call.assert_called_once_with('image.enable', '1', False)

    def test_update(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        new_content = 'DEV_PREFIX=hd\nNAME=Debian\nTYPE=OS'
        h.update(new_content)
        self.client.call.assert_called_once_with('image.update', '1',
                                                    new_content)

    def test_publish(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        assert h.publish() is None

    def test_unpublish(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        assert h.unpublish() is None

    def test_set_persistent(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        h.set_persistent()
        self.client.call.assert_called_once_with('image.persistent',
                                                '1', True)

    def test_set_nonpersistent(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        h.set_nonpersistent()
        self.client.call.assert_called_once_with('image.persistent',
                                                '1', False)

    def test_states(self):
        for i in range(len(oca.Image.IMAGE_STATES)):
            h = oca.Image('<IMAGE><ID>2</ID><STATE>%s</STATE></IMAGE>' % i,
                      self.client)
            assert h.str_state == oca.Image.IMAGE_STATES[i]
            short_image_state = oca.Image.SHORT_IMAGE_STATES[oca.Image.IMAGE_STATES[i]]
            assert h.short_state == short_image_state

    def test_repr(self):
        h = oca.Image(self.xml, self.client)
        assert h.__repr__() == '<oca.Image("MATLAB install CD")>'

    def test_types(self):
        for i in range(len(oca.Image.IMAGE_TYPES)):
            h = oca.Image('<IMAGE><ID>2</ID><TYPE>%s</TYPE></IMAGE>' % i,
                    self.client)
            assert h.str_type == oca.Image.IMAGE_TYPES[i]
            short_image_type = oca.Image.SHORT_IMAGE_TYPES[oca.Image.IMAGE_TYPES[i]]
            assert h.short_type == short_image_type

    def test_template(self):
        i = oca.Image(self.xml, self.client)
        i._convert_types()
        assert isinstance(i.template, oca.pool.Template)

    def test_chown(self):
        self.client.call = Mock(return_value='')
        h = oca.Image(self.xml, self.client)
        h.chown(10, 10)
        self.client.call.assert_called_once_with('image.chown',
                                                '1', 10, 10)
