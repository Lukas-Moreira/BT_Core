Features of BT_Core
===================
 
Status Collector
----------------

.. autoclass:: BluPY.config.status_handler.StatusHandler

**Methods:**

.. autofunction:: BluPY.config.status_handler.StatusHandler.handle

.. code-block:: python

    # Create a client socket (this is just an example, in practice you would get this from the Bluetooth server)
    client_sock, client_info = server_sock.accept()

    # Create a StatusHandler instance
    status_handler = StatusHandler()

    # Handle the status and send it via Bluetooth
    status_handler.handle(client_sock)


Test connection
----------------

.. autofunction:: BluPY.config.test_handler.TestHandler

**Methods:**

.. autofunction:: BluPY.config.test_handler.TestHandler.handle

.. code-block:: python

    # Create a TestHandler instance (this is just an example, you would typically get the IP from a bluetooth message)
    test_handler = TestHandler("192.168.0.100")

    # Execute the test and save the result
    test_handler.handle()

Collector Integration
---------------------

.. autofunction:: BluPY.config.integracoes_handler.IntegracaoHandler

.. note:: This feature has been implemented, but has not been fully tested.

Maintenance Handler
-------------------

.. autofunction:: BluPY.config.maintenance_handler.MaintenanceHandler

.. note:: This feature has not yet been implemented. It is planned for future development.

