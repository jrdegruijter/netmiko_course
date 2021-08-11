#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass

net_connect = ConnectHandler(
    device_type="cisco_nxos",
    host="nxos1.lasthop.io",
    username="pyclass",
    password=getpass(),
)
print(net_connect.find_prompt())
net_connect.disconnect()
