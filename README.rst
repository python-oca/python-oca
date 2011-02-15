##############################################
OCA - OpenNebula Cloud Api
##############################################

:Version: 0.2

About
-----

Bindings for XMLRPC OpenNebula Cloud API

Documentation
-------------
see http://lukaszo.github.com/python-oca/index.html and http://www.opennebula.org/documentation:rel2.0:api

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

Łukasz Oleś

