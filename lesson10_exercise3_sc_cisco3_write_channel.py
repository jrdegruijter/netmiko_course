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

    with ConnectHandler(**device) as net_connect:
        print(net_connect.find_prompt())
        output = net_connect.write_channel("telnet 10.220.88.22\n")
        print(output)
        time.sleep(1)
        output = net_connect.read_channel()
        print(output)
        time.sleep(1)
        output = net_connect.write_channel("pyclass\n")
        print(output)
        time.sleep(1)
        output = net_connect.read_channel()
        print(output)
        time.sleep(1)
        output = net_connect.write_channel("{}\n".format(password))
        print(output)
        time.sleep(1)
        output = net_connect.read_channel()
        print(output)
        time.sleep(2)
        output = net_connect.write_channel("exit\n")

print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
