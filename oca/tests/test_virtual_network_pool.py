# -*- coding: UTF-8 -*-
import os

from mock import Mock

import oca


class TestVirtualNetworkPool:
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/vnetpool.xml')).read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VirtualNetworkPool(self.client)
        pool.info()
        assert len(list(pool)) == 2

