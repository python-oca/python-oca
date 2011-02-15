User Guide
==========

Examples
--------

Allocating new host::

   client = oca.Client('user:password', 'http:12.12.12.12:2633/RPC2')
   new_host_id = oca.Host.allocate(client, 'host_name', 'im_xen', 'vmm_xen', 'tm_nfs')
   hostpool = oca.HostPool(client)
   hostpool.info()
   vm = hostpool.get_by_id(new_host_id)
   print vm.name, vm.str_state


