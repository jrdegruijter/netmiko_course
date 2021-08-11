#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler, redispatch
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
    "device_type": "cisco_ios",
    "host": "cisco3.lasthop.io",
    "username": "pyclass",
    "password": password,
    "session_log": "cisco3.log",
}

# Connect to Cisco3

print("Connecting to Cisco 3")
net_connect = ConnectHandler(**device) 
prompt = net_connect.find_prompt()
if "cisco3" not in prompt:
    raise ValueError("Expecting Cisco3 in prompt")
if "CiscoIosSSH" not in str(net_connect):
    raise ValueError("Expecting CiscoIosSSH class")
print(net_connect.find_prompt())

# Connect to Arista4
print("Connecting to Arista4")
output = net_connect.write_channel("ssh -l pyclass 10.220.88.31\n")
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
time.sleep(1)
redispatch(net_connect, device_type="arista_eos")
prompt = net_connect.find_prompt()
if "arista4" not in prompt:
    raise ValueError("Expecting Cisco3 in prompt")
if "AristaSSH" not in str(net_connect):
    raise ValueError("Expecting CiscoIosSSH class")
print(net_connect.find_prompt())

# Disconnect from Arista4
print("Disconnect from Arista4")
output += net_connect.send_command_timing("exit\n")

prompt = net_connect.find_prompt()
if "cisco3" not in prompt:
    raise ValueError("Expecting Cisco3 in prompt")

# Disconnect from Cisco3

print("Now closing SSH session completely")
output += net_connect.send_command_timing("exit\n")


print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
