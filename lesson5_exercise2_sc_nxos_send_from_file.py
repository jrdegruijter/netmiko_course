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

for device_num in range(1, 3):

    device = {
        "device_type": "cisco_nxos",
        "host": "nxos{}.lasthop.io".format(device_num),
        "username": "pyclass",
        "password": password,
        "session_log": "nxos{}.log".format(device_num),
        "fast_cli": False,
    }

    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_config_from_file(config_file="config.cfg")
        # command("show run", delay_factor=5, max_loops=1000)
        print(output)


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
