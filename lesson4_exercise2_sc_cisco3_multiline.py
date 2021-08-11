#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass
import time
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

password = getpass("Please enter a valid password:")

start = time.perf_counter()

for device_num in range(3, 4):

    device = {
        "device_type": "cisco_ios",
        "host": "cisco{}.lasthop.io".format(device_num),
        "username": "pyclass",
        "password": password,
        "session_log": "cisco{}.log".format(device_num),
    }

    cmd = "copy flash:testx.txt flash:test_jdg.txt"

    with ConnectHandler(**device) as net_connect:
        output = net_connect.send_command(
            cmd,
            expect_string="Destination filename",
            strip_prompt=False,
            strip_command=False,
        )
        output += net_connect.send_command(
            "\n", expect_string="confirm", strip_prompt=False, strip_command=False
        )
        output += net_connect.send_command(
            "y", expect_string="#", strip_prompt=False, strip_command=False
        )
        print(output)


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
