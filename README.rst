##############################################
OCA - OpenNebula Cloud Api
##############################################
:Version: 4.10.0-a1
:status:
  .. image:: https://travis-ci.org/python-oca/python-oca.svg
     :target: https://travis-ci.org/python-oca/python-oca

About
-----

Bindings for XMLRPC OpenNebula Cloud API

Documentation
-------------
see http://python-oca.github.com/python-oca/index.html and http://docs.opennebula.org/4.10/integration/system_interfaces/api.html

All `allocate` functions are implemented as static methods.

Examples
--------

Allocating new host::

    client = oca.Client('user:password', 'http:12.12.12.12:2633/RPC2')
    new_host_id = oca.Host.allocate(client, 'host_name', 'im_xen', 'vmm_xen', 'tm_nfs')
    hostpool = oca.HostPool(client)
    hostpool.info()
    vm = hostpool.get_by_id(new_host_id)
    print vm.name, vm.str_state

License
-------

OCA is under Apache Software License

Authors
-------

See AUTHORS file


