import subprocess
import time
import os
import glob

class SHADOWGUARD():
    def __init__(self, interfaces=['wlan0']):
        self.interfaces = interfaces
        self.init_logs()
        self.init_lists()

    def monitor_enabled(self, interface):
        """Checks if interface is in monitor mode"""
        command = f'iwconfig {interface}'
        iw_output = subprocess.getoutput(command)
        monitor_enabled = "Mode:Monitor" in iw_output        

        return monitor_enabled    

    def start_monitor(self, interface):
        """Tries to enable monitor mode on the specified interface"""
        command = f'sudo ifconfig {interface} down'
        command += f'&& sudo iwconfig {interface} mode monitor'
        command += f'&& sudo ifconfig {interface} up'
        return subprocess.getoutput(command)

    def stop_monitor(self, interface):
        """Tries to disable monitor mode on the specified interface"""
        command = f'sudo ifconfig {interface} down'
        command += f'&& sudo iwconfig {interface} mode managed'
        command += f'&& sudo ifconfig {interface} up'
        return subprocess.getoutput(command)

    def kismet_running(self):
        """Check if kismet is running"""
        processes = subprocess.getoutput('ps aux | grep "kismet --daemonize" | grep -v grep')
        
        # grep counts as a process, so kismet + grep = 2 or more processes
        print(processes)
        print(len(processes))
        kismet_running = len(processes) >= 1
        return kismet_running
        
    def start_kismet(self):
        """starts kismet"""
        subprocess.Popen(['/usr/bin/kismet', '--daemonize'])
        time.sleep(5)

    def stop_kismet(self):
        """stops kismet"""
        while self.kismet_running():
            pids = subprocess.getoutput('ps aux | grep "kismet --daemonize" | grep -v grep | cut -d " " -f 7')
            pid = pids
            if '\n' in pids:
                pid = pids.splitlines()[0]
            subprocess.getoutput(f'kill -9 {pid}')

    def monitor(self):
        """Checks kismet and monitor mode, start if stopped"""
        for interface in self.interfaces:
            if not self.monitor_enabled(interface):
                self.start_monitor(interface)
        
        if not self.kismet_running():
            self.start_kismet()

    def get_kismet_db(self):
        """Get the most recent kismet db file"""
        kismet_dbs = glob.glob('*.kismet')
        latest_file = max(kismet_dbs, key=os.path.getctime)

        return latest_file

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
   
    def init_logs(self):
       pass
      
    def init_lists(self):
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
        
