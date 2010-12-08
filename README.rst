##############################################
OCA
##############################################

:Version: 0.1

About
-----

Bindings for XMLRPC OpenNebula Cloud API

Documentation
-------------
see http://www.opennebula.org/documentation:rel2.0:api

All `allocate` functions are implemented as static methods.

Examples
--------

Allocating new host:

    client = oca.Client('user:password', 'http:12.12.12.12:2633:/RPC2')
    new_host_id = oca.Host.allocate(client, 'host_name', 'im_xen', 'vmm_xen', 'tm_nfs')
    hostpool = oca.HostPool(client)
    hostpool.info()
    for i in hostpool:
        if i.id == new_host_id:
            vm = i
            break
    print i.name, i.str_state

License
-------

OCA is under Apache Software License

Authors
-------

Łukasz Oleś

