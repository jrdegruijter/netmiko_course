#!/home/degruijter/new_venv/bin/python

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)
from paramiko.ssh_exception import SSHException
from concurrent.futures import ThreadPoolExecutor, wait
from getpass import getpass
import yaml
import time
import logging
import os

logging.basicConfig(
    filename="netmiko.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


def load_devices(device_file="lab_devices.yml"):
    device_dict = {}
    with open(device_file) as f:
        device_dict = yaml.safe_load(f)
    return device_dict


def netmiko_connection(device, command=None):
    try:
        net_connect = ConnectHandler(**device)
        if command is None:
            return net_connect.find_prompt()
        else:
            output = net_connect.send_command(command)
            return output
    except NetmikoAuthenticationException:
        logger.error("Authentication failed. Please check used credentials")
    except NetmikoTimeoutException as e:
        if "DNS failure" in str(e):
            logger.error("DNS failure")
        elif "TCP connection to device failed" in str(e):
            logger.error(
                "TCP connection to device failed. Are you using the correct port?"
            )
        else:
            raise
    except SSHException as e:
        if "Error reading SSH banner" in str(e):
            logger.error("SSH banner error")
        else:
            raise
    return None


if __name__ == "__main__":

    start = time.perf_counter()

    password = (
        os.getenv("NETMIKO_PASSWORD")
        if os.getenv("NETMIKO_PASSWORD")
        else getpass("Please enter a valid password:")
    )

    cmds = {
        "cisco_xe": "show ip arp",
        "arista_eos": "show ip arp",
        "juniper_junos": "show arp",
        "cisco_nxos": "show ip arp vrf management",
    }

    my_devices = load_devices()

    max_threads = 20

    pool = ThreadPoolExecutor(max_threads)

    future_list = []

    for device_name, device in my_devices.items():
        device["password"] = password
        future = pool.submit(netmiko_connection, device, cmds[device["device_type"]])
        future_list.append(future)

    wait(future_list)

    for future in future_list:
        result = future.result()
        output = result
        print("-" * 20)
        print("{}:\n\n{}".format(device_name, output))
        print("-" * 20)

    print("The script is now done")

    end = time.perf_counter()

    print("Script execution time: {:.1f}".format(end - start))
