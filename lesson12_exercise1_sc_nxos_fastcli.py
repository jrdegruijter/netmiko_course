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
    "host": "nxos2.lasthop.io",
    "username": "pyclass",
    "password": password,
    "session_log": "nxos2.log",
    "fast_cli": False,
}

try:
    net_connect = ConnectHandler(**device)
    output = net_connect.send_command("conf t")
    print(output)
finally:
    print("The script is now done")
    end = time.perf_counter()
    print("Script execution time: {:.1f}".format(end - start))
