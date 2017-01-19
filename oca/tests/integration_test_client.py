# vim:  set fileencoding=utf8
# encoding:utf8
#
# Author: Matthias Schmitz <matthias@sigxcpu.org>

import os
import unittest

import oca


@unittest.skipUnless(os.environ.get('OCA_INT_TESTS', False),
                     "Skipping integration tests")
class IntTestClient(unittest.TestCase):
    def setUp(self):
        try:
            del os.environ["ONE_AUTH"]
        except KeyError:
            pass

        self.c = oca.Client(os.environ['OCA_INT_TESTS_ONE_AUTH'],
                            os.environ['OCA_INT_TESTS_ONE_XMLRPC'])

    def test_connection(self):
        self.assertIn(os.environ['OCA_INT_TESTS'], self.c.version())
