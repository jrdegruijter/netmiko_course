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
        "device_type": "cisco_nxos",
        "host": "nxos{}.lasthop.io".format(device_num),
        "username": "pyclass",
        "password": password,
        "session_log": "nxos{}.log".format(device_num),
    }

    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command("show lldp neighbors detail", use_genie=True)
        #output = output["interfaces"]        
        print(output)
        #print()
        #for vlan_dict in output:
        #    print()
        #    print("Local interface: {}".format(vlan_dict["port_id"]))
        #    print("Remote neighbor name: {}".format(vlan_dict["neighbors"]))
        #    print("Remote interface name {}".format(vlan_dict["port_description"]))
        #    print("Management IP: {}".format(vlan_dict["management_address_v4"]))


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
