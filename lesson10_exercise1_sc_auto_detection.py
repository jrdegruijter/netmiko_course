#!/home/degruijter/new_venv/bin/python

from netmiko import (
    ConnectHandler,
    NetmikoAuthenticationException,
    NetmikoTimeoutException,
    SSHDetect,
)
from paramiko.ssh_exception import SSHException
from concurrent.futures import ThreadPoolExecutor, as_completed
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


def load_devices(device_file="my_hosts.txt"):
    device_dict = {}
    with open(device_file) as f:
        for line in f:
            device_dict[str(line).split('.')[0]] = {
                "host": line,
                "device_type": "autodetect",
                "username": "pyclass",
            }
    return device_dict


def netmiko_connection(device):
    try:
        guesser = SSHDetect(**device)
        output = device["host"]
        output += guesser.autodetect()
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

    my_devices = load_devices()

    max_threads = 20

    pool = ThreadPoolExecutor(max_threads)

    future_list = []

    for device_name, device in my_devices.items():
        device["password"] = password
        future = pool.submit(netmiko_connection, device)
        future_list.append(future)

    for future in as_completed(future_list):
        result = future.result()
        print("-" * 20)
        print("{}".format(result))
        print("-" * 20)

    print("The script is now done")

    end = time.perf_counter()

    print("Script execution time: {:.1f}".format(end - start))
