# -*- coding: utf-8 -*-
import os
import unittest

from mock import Mock

import oca


class TestVmTemplatePool(unittest.TestCase):
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/templatepool.xml')).read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.VmTemplatePool(self.client)
        pool.info()
        assert len(pool) == 2
