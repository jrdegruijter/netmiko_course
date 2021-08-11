#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler, NetmikoAuthenticationException
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

try:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("show ip arp vrf management")
    print(output)
except NetmikoAuthenticationException:
    print("Authentication failed")


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
