#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass
import time
import logging
import os

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

# password = (
#    os.getenv("NETMIKO_PASSWORD")
#    if os.getenv("NETMIKO_PASSWORD")
#    else getpass("Please enter a valid password:")
# )

start = time.perf_counter()

cmd = "show ip arp"

for device_num in range(4, 5):

    device = {
        "device_type": "cisco_ios",
        "host": "cisco{}.lasthop.io".format(device_num),
        "username": "student1",
        "use_keys": True,
        "key_file": "~/.ssh/student_key",
        "allow_agent": True,
        "session_log": "cisco{}.log".format(device_num),
        "fast_cli": False,
    }

    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command(cmd)
        print(output)


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
