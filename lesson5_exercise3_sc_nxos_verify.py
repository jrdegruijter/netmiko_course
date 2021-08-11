#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass
import time
import logging
import os

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

password = (
    os.getenv("NETMIKO_PASSWORD")
    if os.getenv("NETMIKO_PASSWORD")
    else getpass("Please enter a valid password:")
)

start = time.perf_counter()

device = {
    "device_type": "cisco_nxos",
    "host": "nxos1.lasthop.io",
    "username": "pyclass",
    "password": password,
    "session_log": "verylonghostnamefornxos.log",
    "fast_cli": False,
}

with ConnectHandler(**device) as net_connect:
    net_connect.global_cmd_verify=False
    output = net_connect.send_command("terminal width 80")
    output += net_connect.send_command("show ip interface brief vrf management | include management")
    print(output)

print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
