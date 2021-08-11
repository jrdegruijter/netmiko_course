#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass
import time
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

password = getpass("Please enter a valid password:")

start = time.perf_counter()

for device_num in range(1, 2):

    device = {
        "device_type": "cisco_ios",
        "host": "cisco{}.lasthop.io".format(device_num),
        "username": "pyclass",
        "password": password,
        "session_log": "cisco{}.log".format(device_num),
    }

    with ConnectHandler(**device) as net_connect:
        print(net_connect.find_prompt())
        output = net_connect.send_command("disable",expect_string=r">")
        print(device["host"])
        print(net_connect.find_prompt())


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
