#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass

net_connect = ConnectHandler(
    device_type="cisco_ios",
    host="cisco3.lasthop.io",
    username="pyclass",
    password=getpass(),
    session_log="cisco3.log",
)
print(net_connect.find_prompt())
