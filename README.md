OCA - OpenNebula Cloud API
==========================

[![Build Status](https://travis-ci.org/python-oca/python-oca.svg?branch=master)](http://travis-ci.org/python-oca/python-oca)
[![Version](https://img.shields.io/badge/version-4.10.0.a1-brightgreen.svg)](https://github.com/python-oca/python-oca/releases)
[![License](https://img.shields.io/badge/license-Apache-brightgreen.svg)](http://www.apache.org/licenses/LICENSE-2.0.html)

About
-----
Python bindings for the XMLRPC OpenNebula Cloud API

Documentation
-------------
See http://python-oca.github.io/python-oca/index.html and http://docs.opennebula.org/4.10/integration/system_interfaces/api.html

All `allocate` functions are implemented as static methods.

Examples
--------
Allocating a new host:

    client = oca.Client('user:password', 'http:12.12.12.12:2633/RPC2')
    new_host_id = oca.Host.allocate(client, 'host_name', 'im_xen', 'vmm_xen', 'tm_nfs')
    hostpool = oca.HostPool(client)
    hostpool.info()
    vm = hostpool.get_by_id(new_host_id)
    print vm.name, vm.str_state

License
-------
OCA is licensed under the [Apache Software License](LICENSE)

Authors
-------
See [AUTHORS](AUTHORS)
