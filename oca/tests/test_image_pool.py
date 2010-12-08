# -*- coding: UTF-8 -*-
from mock import Mock

from oca import Client, ImagePool


class TestImagePool:
    def setUp(self):
        self.client = Client('test:test')
        self.xml = open('fixtures/imagepool.xml').read()

    def test_info(self):
        self.xml = self.xml.replace('\n', '')
        self.xml = self.xml.replace(' ', '')
        self.client.call = Mock(return_value=self.xml)
        pool = ImagePool(self.client)
        pool.info()
        assert len(list(pool)) == 3

    def test_repr(self):
        pool = ImagePool(self.client)
        assert pool.__repr__() == '<oca.ImagePool()>'

