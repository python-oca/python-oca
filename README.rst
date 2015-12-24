##############################################
OCA - OpenNebula Cloud Api
##############################################

:Version: 4.10.0
:TravisCI Status:
  .. image:: https://travis-ci.org/python-oca/python-oca.svg
     :target: https://travis-ci.org/python-oca/python-oca

About
-----

Bindings for XMLRPC OpenNebula Cloud API

Documentation
-------------
See http://python-oca.github.io/python-oca/index.html and http://docs.opennebula.org/4.10/integration/system_interfaces/api.html

All `allocate` functions are implemented as static methods.

Examples
--------

Show all running virtual machines::

   client = oca.Client('user:password', 'http://12.12.12.12:2633/RPC2')
   client.version()
   vm_pool = oca.VirtualMachinePool(c)
   vm_pool.info()
   for vm in vm_pool:
       print "%s (memory: %s MB)" % ( vm.name, vm.template.memory)


License
-------

OCA is under Apache Software License

Authors
-------

See AUTHORS file
