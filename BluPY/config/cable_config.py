import subprocess
from .base_config import BaseConfig

class CableConfig(BaseConfig):
    '''
    Class to configure wired network connections using nmcli.

    Parameters:
        - ip   (str): Static IP address.
        - msk  (str): Subnet mask.
        - gw   (str): Default gateway.
    '''
    def __init__(self, ip, msk, gw):
        self.ip = ip
        self.msk = msk
        self.gw = gw

    def apply(self):
        '''
        Method to apply the wired network configuration.
        '''
        print("[CableConfig]: Applying wired network configuration...")
        try:
            subprocess.run(["sudo", "nmcli", "connection", "delete", "ETHEMPRESA"], check=False)

            subnet = self.mask_to_cidr(self.msk)
            subprocess.run([
                "sudo", "nmcli", "con", "add", "type", "ethernet",
                "con-name", "ETHEMPRESA", "ifname", "eth0",
                "ip4", f"{self.ip}/{subnet}", "gw4", self.gw
            ], check=True)

            subprocess.run(["sudo", "nmcli", "con", "mod", "ETHEMPRESA", "ipv4.method", "manual"], check=True)
            subprocess.run(["sudo", "nmcli", "connection", "up", "ETHEMPRESA"], check=True)

            print("[CableConfig]: Configuration applied successfully.")
        except subprocess.CalledProcessError as e:
            print(f"[CableConfig]: Error: {e}")