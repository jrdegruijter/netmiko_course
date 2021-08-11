#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass
import time
import logging
from pprint import pprint

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

password = getpass("Please enter a valid password:")

start = time.perf_counter()

for device_num in range(1, 2):

    device = {
        "device_type": "arista_eos",
        "host": "arista{}.lasthop.io".format(device_num),
        "username": "pyclass",
        "password": password,
        "session_log": "arista{}.log".format(device_num),
    }

    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command_timing("show vlan", use_textfsm=True)
        print()
        pprint(output)
        print()
        for vlan_dict in output:
            if vlan_dict["vlan_id"] == "7":
                print()
                print("VLAN ID: {}".format(vlan_dict["vlan_id"]))
                print("VLAN name: {}".format(vlan_dict["name"]))

print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
