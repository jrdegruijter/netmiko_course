#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass

password = getpass("Please enter a valid password:")

device = {
    "device_type": "cisco_nxos",
    "host": "nxos1.lasthop.io",
    "username": "pyclass",
    "password": password,
}

net_connect = ConnectHandler(**device)

print(net_connect.find_prompt())
net_connect.disconnect()
