#!/home/degruijter/new_venv/bin/python

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
)
from paramiko.ssh_exception import SSHException
from getpass import getpass
import yaml
import time
import logging
import os

logging.basicConfig(
    filename="netmiko_class7.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)


def load_devices(device_file="lab_devices2.yml"):
    device_dict = {}
    with open(device_file) as f:
        device_dict = yaml.safe_load(f)
    return device_dict


def netmiko_connection(device):
    try:
        net_connect = ConnectHandler(**device)
        return net_connect
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

    my_devices = load_devices()

    for device_name, device in my_devices.items():
        if not device["password"]:
            device["password"] = password
        # import pdb; pdb.set_trace()
        net_connect = netmiko_connection(device)
        if net_connect is None:
            continue
        print(net_connect.find_prompt())

    print("The script is now done")

    end = time.perf_counter()

    print("Script execution time: {:.1f}".format(end - start))
