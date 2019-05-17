# -*- coding: UTF-8 -*-
from setuptools import setup
import setuptools
import os
import sys

__version__ = '4.15.1'


# borrowed from Pylons project
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

EXTRAS_REQUIRE = {}
INSTALL_REQUIRES = []

if int(setuptools.__version__.split(".", 1)[0]) < 18:
    if sys.version_info[0:2] < (3, 0):
        INSTALL_REQUIRES.append("future")
else:
    EXTRAS_REQUIRE[":python_version<'3.0'"] = ['future']

setup(name='oca',
      version=__version__,
      description='Python Bindings for XMLRPC OpenNebula Cloud API',
      long_description=README + '\n\n' + CHANGES,
      test_suite='nose.collector',
      classifiers=['Development Status :: 3 - Alpha',
                   'License :: OSI Approved :: Apache Software License',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent'],
      keywords='opennebula cloud xmlrpc',
      author=u'Łukasz Oleś, Matthias Schmitz, Michael Schmidt',
      url='https://github.com/python-oca/python-oca',
      license='Apache License 2.0',
      extras_require=EXTRAS_REQUIRE,
      install_requires=INSTALL_REQUIRES,
      packages=['oca'])
