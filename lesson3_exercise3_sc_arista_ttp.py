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
        output = net_connect.send_command("show vlan", use_ttp=True, ttp_template="show_vlan.ttp")
        # output = output["interfaces"]
        pprint(output)
        print()
        for list in output[0][0]:
            if list["vlan_id"] == "7":
                print("VLAN ID: {}".format(list["vlan_id"]))
                print("VLAN name: {}".format(list["vlan_name"]))


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
