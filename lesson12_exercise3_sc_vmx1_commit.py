#!/home/degruijter/new_venv/bin/python

from netmiko import ConnectHandler
from getpass import getpass
import time
import logging

logging.basicConfig(filename="test.log", level=logging.DEBUG)
logger = logging.getLogger("netmiko")

password = getpass("Please enter a valid password:")

start = time.perf_counter()

cfg_commands = [
    "set system syslog archive size 110k files 3",
    "set system time-zone America/New_York",
]

device = {
    "device_type": "juniper_junos",
    "host": "vmx1.lasthop.io",
    "username": "pyclass",
    "password": password,
    "session_log": "vmx1.log",
}

print("Sending commands to vmx1")

net_connect = ConnectHandler(**device)

output = net_connect.send_config_set(cfg_commands)

print("Next step is to commit commands, this can take some time!")

output = net_connect.commit(comment="commit by JdG netmiko script", and_quit=True)

output = net_connect.send_command("show system commit")
output = output.strip()
commits = output.splitlines()
last_commit = commits[:2]
last_commit = "\n".join(last_commit)

# import pdb; pdb.set_trace()

print(last_commit)

print("The script is now done")

end = time.perf_counter()

print("Script execution time: {:.1f}".format(end - start))
