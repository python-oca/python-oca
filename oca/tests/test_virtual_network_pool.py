# -*- coding: UTF-8 -*-
import os
import unittest

from mock import Mock

import oca


class TestVirtualNetworkPool(unittest.TestCase):
    def setUp(self):
        self.client = oca.Client('test:test')
        self.client.one_version = '4.10.0'
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/vnetpool.xml')).read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VirtualNetworkPool(self.client)
        pool.info()
        assert len(list(pool)) == 2
