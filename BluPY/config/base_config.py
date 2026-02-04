import netifaces # type: ignore

class BaseConfig:
    '''
    Class base config.

    Utility methods for subnet mask conversion and obtaining active IP.
    '''
    @staticmethod
    def mask_to_cidr(mask):
        '''
        Converts a subnet mask from dotted decimal format to CIDR notation.

        '''
        if "/" in mask:
            return mask.replace("/", "")
        
        parts = map(int, mask.split('.'))
        return sum(bin(part).count('1') for part in parts)
    
    @staticmethod
    def get_first_active_ip():
        '''
        Obtains the first active IP address from network interfaces.
        '''
        for iface in ["eth0","wlan0"]:
            try:
                addresses = netifaces.ifaddresses(iface)
                if netifaces.AF_INET in addresses:
                    return addresses[netifaces.AF_INET][0]['addr']
            except ValueError:
                # Interface not found or no addresses available
                continue
        return "No IP address"