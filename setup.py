# -*- coding: UTF-8 -*-
__version__ = '4.10.0-a1'

import os

# from distutils.core import setup
from setuptools import setup

# borrowed from Pylons project
here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()
except IOError:
    README = CHANGES = ''

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
      packages=['oca'])
