Utils for Network Configuration
===============================

This document provides examples and explanations for configuring network settings using the BluPY library.

CIDR to Netmask
----------------

.. autofunction:: BluPY.config.base_config.BaseConfig.mask_to_cidr

**Implementation**

.. code-block:: python

    from BluPY.config.base_config import BaseConfig

    netmask = "255.255.255.255"
    cidr = BaseConfig.mask_to_cidr(netmask)
    print(cidr)  # Output: 32

Get First Active IP
-------------------

.. autofunction:: BluPY.config.base_config.BaseConfig.get_first_active_ip

**Implementation**

.. code-block:: python

    from BluPY.config.base_config import BaseConfig

    ip = BaseConfig.get_first_active_ip()
    print(ip)  # Output: e.g., "192.168.1.1"

.. note::

    It was implemented, tested, but not used in the final version of BluPY.z