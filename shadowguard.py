import subprocess
import time

class SHADOWGUARD():
    def __init__(self):
        self.monitor()
        self.init_logs()
        self.init_lists()

    def check_kismet(self):
        """Start kismet if it isn't already running"""
        processes = subprocess.getoutput('ps aux | grep kismet').splitlines()
        if len(processes) <= 2:
            self.start_kismet()

    def check_interfaces(self):
        """Put interfaces in monitor mode if not already"""
        monitoring_interfaces = []
        monitor_enabled = False
        while not monitor_enabled:
            iw_output = subprocess.getoutput('iwconfig')
            monitor_enabled = "Mode:Monitor" in iw_output
            if not monitor_enabled:
                print('Trying monitor mode')
                enable_monitor = [
                    'sudo ifconfig wlan0 down',
                    'sudo iwconfig wlan0 mode monitor',
                    'sudo ifconfig wlan0 up',
                    'sudo ifconfig wlan1 down',
                    'sudo iwconfig wlan1 mode monitor',
                    'sudo ifconfig wlan1 up',
                ]
                for command in enable_monitor:
                    print(subprocess.getoutput(command))

    def start_kismet(self):
        """starts kismet"""
        subprocess.getoutput('/usr/bin/kismet &')

    def monitor(self):
        self.check_kismet()
        self.check_interfaces()

    def get_kismet_db(self):
        pass

    def query_kismet(self):
        pass

    def get_macs_from(self, start_time, end_time):
        pass
    
    def get_ssid_from(self, start_time, end_time):
        pass

    def fetch_from(self, start_time, end_time):
        """get data from a timeframe"""
        data = {}
        data['macs'] = self.get_macs_from(start_time, end_time)
        data['ssids'] = self.get_ssid_from(start_time, end_time)
        return data

    def rotate_lists(self):
        pass
    
    def check_logs(self):
        pass
    
    def fetch(self):
        self.past_five = self.fetch_from(self.time_now, self.time_five)
        self.five_to_ten = self.fetch_from(self.time_five, self.time_ten)
        self.ten_to_fifteen = self.fetch_from(self.time_ten, self.time_fifteen)
        self.fifteen_to_twenty = self.fetch_from(self.time_fifteen, self.time_twenty)
    
    def fetch_current(self):
        # Get last two mins
        # Check if they're in 10-20 min lists
        pass
      
if __name__ == '__main__':
    sg = SHADOWGUARD()
    sg.monitor()
    sg.get_times()
    sg.init_db()
    sg.fetch()
    
    time_count = 0
    while True:
        time_count += 1
        if time_count % 5 == 0:
            sg.fetch_current()
            sg.update_lists()
            sg.get_times()
            sg.clear_recent()
            sg.rotate_lists()
        
        time.sleep(60)
        
