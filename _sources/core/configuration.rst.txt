Network Configuration
=====================

Cable Configuration
-------------------

.. autoclass:: BluPY.config.cable_config.CableConfig
    :inherited-members:

**Example of usage:**

.. code-block:: python

    # Create a CableConfig instance with desired settings
    config = CableConfig(
        "192.168.1.100", 
        "255.255.255.0", 
        "192.168.1.1"
    )

    # Apply the configuration
    config.apply()

.. autofunction:: BluPY.config.cable_config.CableConfig.apply
    :inherited-members:

**Example of implementation:**

.. code-block:: bash

    # Get the subnet in CIDR notation from the subnet mask
    subnet = self.mask_to_cidr(self.msk)

    # Set configuration using nmcli
    subprocess.run([
        "sudo", "nmcli", "con", "add", "type", "ethernet",
        "con-name", "ETHEMPRESA", "ifname", "eth0",
        "ip4", f"{self.ip}/{subnet}", "gw4", self.gw
    ], check=True)


Wifi Configuration
------------------

.. autoclass:: BluPY.config.wifi_config.WiFiConfig
    :inherited-members:

**Example of usage:**

.. code-block:: python

    # Create a WifiConfig instance with desired settings
    config = WifiConfig(
        ssid="MySSID", 
        password="MyPassword", 
        ip="192.168.1.100",
        msk="255.255.255.0",
        gw="192.168.1.1"
    )

    # Apply the configuration
    config.apply()

.. autofunction:: BluPY.config.wifi_config.WiFiConfig.apply
    :inherited-members:

**Example of implementation:**

.. code-block:: python

    # Connect to the WiFi network
    subprocess.run([
        "sudo", "nmcli", "dev", "wifi",
        "connect", self.ssid, "password",
        self.pwd , "ifname", "wlan0"
    ], check=True)

    # Get the subnet in CIDR notation from the subnet mask
    subnet = self.mask_to_cidr(self.msk)

    # Set static IP configuration
    subprocess.run([
        "sudo", "nmcli", "connection", "modify", self.ssid,
        "ifname", "wlan0", "ip4", f"{self.ip}/{subnet}",
        "gw4", self.gw, "ipv4.method", "manual"
    ], check=True)