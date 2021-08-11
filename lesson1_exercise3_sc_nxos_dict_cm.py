#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass
import time

password = getpass("Please enter a valid password:")

start = time.perf_counter()

device = {
    "device_type": "cisco_nxos",
    "host": "nxos1.lasthop.io",
    "username": "pyclass",
    "password": password,
}

with ConnectHandler(**device) as net_connect:
    print(net_connect.find_prompt())

print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
