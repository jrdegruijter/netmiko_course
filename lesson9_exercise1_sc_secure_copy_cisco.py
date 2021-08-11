#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler, file_transfer
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

cmds = "copy flash:/config2.cfg system:running-config"

source_file = "config2.cfg"
dest_file = "config2.cfg"
direction = "put"
file_system = "flash:"

for device_num in range(3, 5):

    device = {
        "device_type": "cisco_ios",
        "host": "cisco{}.lasthop.io".format(device_num),
        "username": "pyclass",
        "password": password,
        "session_log": "cisco{}.log".format(device_num),
    }

    with ConnectHandler(**device) as net_connect:
        print(net_connect.find_prompt())
        transfer_dict = file_transfer(
            net_connect,
            source_file=source_file,
            dest_file=dest_file,
            file_system=file_system,
            direction=direction,
            overwrite_file=True,
        )
        print(transfer_dict)
        output = net_connect.send_command(cmds, expect_string=r"Destination filename")
        print(output)
        print(net_connect.find_prompt())

print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
