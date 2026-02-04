import subprocess
from .base_config import BaseConfig

class WiFiConfig(BaseConfig):
    '''
    Class to configure Wi-Fi settings on a Linux system using nmcli.

    Parameters:
        - ssid (str): Wi-Fi network name.
        - pwd  (str): Wi-Fi network password.
        - ip   (str): Static IP address.
        - msk  (str): Subnet mask.
        - gw   (str): Default gateway.
    '''
    def __init__(self, ssid, pwd, ip, msk, gw):
        self.ssid = ssid
        self.pwd = pwd
        self.ip = ip
        self.msk = msk
        self.gw = gw

    def apply(self):
        '''
        Apply the Wi-Fi configuration using nmcli.
        '''
        print("[WiFiConfig]: Applying Wi-Fi configuration...")
        try:
            subprocess.run(["sudo", "nmcli", "connection", "delete", self.ssid], check=False)

            subprocess.run([
                "sudo", "nmcli", "dev", "wifi",
                "connect", self.ssid, "password",
                self.pwd , "ifname", "wlan0"
            ], check=True)

            subnet = self.mask_to_cidr(self.msk)
            subprocess.run([
                "sudo", "nmcli", "connection", "modify", self.ssid,
                "ifname", "wlan0", "ip4", f"{self.ip}/{subnet}",
                "gw4", self.gw, "ipv4.method", "manual"
            ], check=True)

            subprocess.run(["sudo", "nmcli", "connection", "up", self.ssid], check=True)

            print("[WiFiConfig]: Configuration applied successfully.")

        except subprocess.CalledProcessError as e:
            print(f"[WiFiConfig]: Error: {e}")