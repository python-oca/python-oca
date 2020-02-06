# -*- coding: utf-8 -*-
import os
import unittest

from mock import Mock

import oca


class TestGroupPool(unittest.TestCase):
    def setUp(self):
        self.client = oca.Client('test:test')
        self.xml = open(os.path.join(os.path.dirname(oca.__file__),
                                     'tests/fixtures/grouppool.xml')).read()

    def test_info(self):
        self.client.call = Mock(return_value=self.xml)
        pool = oca.GroupPool(self.client)
        pool.info()
        assert len(pool) == 2
