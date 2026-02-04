.. BT_Core documentation master file, created by
   sphinx-quickstart on Tue Feb  3 15:39:18 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BT_Core documentation
=====================

The BT_Core is a module develeped in Python to provides a simple configuration for collectors data acquisiton. 

It is designed to facilitate the setup and management of network connections, including both wired (**cable**) and 
wireless (**WiFi**) configurations. The module aims to streamline the process of connecting devices to networks, 
making it easier for users to establish reliable connections for data collection purposes.

.. toctree::
   :maxdepth: 2
   :caption: Application:

   source/application

.. toctree::
   :maxdepth: 2
   :caption: Services:

   services/bluetooth
   services/tcp
   services/udp

.. toctree::
   :maxdepth: 2
   :caption: Core Modules:

   core/configuration
   core/features
   utils/utils

.. toctree::
   :maxdepth: 2
   :caption: informations:

   releases/releases