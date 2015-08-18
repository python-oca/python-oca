# vim:  set fileencoding=utf8
# encoding:utf8
#
# Author: Matthias Schmitz <matthias@sigxcpu.org>

import unittest
import os
import oca


@unittest.skipUnless(os.environ.has_key('OCA_INT_TESTS'),
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
