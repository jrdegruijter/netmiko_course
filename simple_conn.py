#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass

net_connect = ConnectHandler(
    device_type="invalid",
    host="cisco3.lasthop.io",
    username="pyclass",
    password=getpass(),
)
print(net_connect.find_prompt())
