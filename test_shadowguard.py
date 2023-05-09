import shadowguard
import os
import subprocess

sg = shadowguard.SHADOWGUARD()

def test_get_dbs():
    db = sg.get_kismet_db()
    print(db)

def test_monitor():
    # If you want these tests to pass in VSCode,
    # Be sure to configure passwordless sudo for ifconfig and iwconfig
    wlan = 'wlan0'
    
    sg.stop_monitor(interface=wlan)
    assert sg.monitor_enabled(interface=wlan) == False
    
    sg.start_monitor(interface=wlan)
    assert sg.monitor_enabled(interface=wlan) == True

def test_kismet():
    sg.start_kismet()
    assert sg.kismet_running() == True
    
    sg.stop_kismet()
    assert sg.kismet_running() == False

if __name__ == '__main__':
    test_get_dbs()
    test_monitor()
    test_kismet()
