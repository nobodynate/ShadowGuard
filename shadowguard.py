import subprocess

class SHADOWGUARD():
    def __init__(self):
        self.interfaces = None
        self.latest_db = self.get_kismet_db()
        self.zero_to_five = None
        self.five_to_ten = None
        pass

    def init_interfaces(self):
        pass

    def monitor(self):
        """Checks that kismet is running and monitor mode enabled"""
        # Is Kismet Running?
        processes = subprocess.check_output('ps aux | grep kismet').decode('utf-8').splitlines()
        if len(processes) <= 2:
            raise "Kismet is not running!"
            exit()
        
        # Monitor Mode enabled?
        monitoring_interfaces = []
        for interface in self.interfaces:
            iw_output = subprocess.check_output('iwconfig').decode('utf-8')
            if "Mode:Monitor" not in iw_output:
                raise f"Monitor mode not enabled on {interface}"
                exit()

        # Return true if both checks pass
        return True

    def start_kismet(self):
        pass

    def get_kismet_db(self):
        pass

    def query_kismet(self):
        pass

    def get_macs_from(self, start_time, end_time):
        pass
    
    def get_ssid_from(self, start_time, end_time):
        pass

    def rotate_lists(self):
        pass

