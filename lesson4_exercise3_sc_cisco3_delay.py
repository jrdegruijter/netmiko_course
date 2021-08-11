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

for device_num in range(3, 4):

    device = {
        "device_type": "cisco_ios",
        "host": "cisco{}.lasthop.io".format(device_num),
        "username": "pyclass",
        "password": password,
        "session_log": "cisco{}.log".format(device_num),
        "fast_cli": False,
        "global_delay_factor":4,
    }

    with ConnectHandler(**device) as net_connect:
        print(net_connect.find_prompt())


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
