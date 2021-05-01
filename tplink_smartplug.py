##Credit to https://github.com/softScheck/tplink-smartplug/blob/master/tplink_smartplug.py

import os
import socket
import json
import random
import logging
from struct import pack
from time import time, sleep
from prometheus_client import start_http_server, Summary, Gauge


def process_request():
    hosts_env_var = str(os.getenv('HS1X_HOSTS'))
    hosts = hosts_env_var.split(',')

    for val in hosts:
        hostname = val.split(':')
        ip = hostname[0]
        port = hostname[1]

        try:
            logging.info(f'Fetching data from host {ip}:{port}')
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_tcp.settimeout(int(10))
            sock_tcp.connect((str(ip), int(port)))
            sock_tcp.settimeout(None)
            sock_tcp.send(encrypt('{"emeter":{"get_realtime":{}}}'))
            data = sock_tcp.recv(2048)
            sock_tcp.close()

            decrypted = decrypt(data[4:])

            result = json.loads(decrypted)
            result = result["emeter"]["get_realtime"]

            current_ma.labels(val).set(result["current_ma"])
            voltage_mv.labels(val).set(result["voltage_mv"])
            power_mw.labels(val).set(result["power_mw"])
            total_wh.labels(val).set(result["total_wh"])

            logging.info(f'Successfully fetched data from host {ip}:{port}')
        except socket.error:
            logging.warning(f"Could not connect to host {ip}:{port}. Retrying...")
    sleep(60 - time() % 60)

# Encryption and Decryption of TP-Link Smart Home Protocol
# XOR Autokey Cipher with starting key = 171
def encrypt(string):
    key = 171
    result = pack(">I", len(string))
    for i in string:
        a = key ^ ord(i)
        key = a
        result += bytes([a])
    return result

def decrypt(string):
    key = 171
    result = ""
    for i in string:
        a = key ^ i
        key = i
        result += chr(a)
    return result

if __name__ == '__main__':
    start_http_server(9784)

    current_ma = Gauge('current_ma', 'Current being used in milliamps', ["host"])
    voltage_mv = Gauge('voltage_mv', 'Voltage being used in millivolts', ["host"])
    power_mw = Gauge('power_mw', 'Watts being used in milliwatts', ["host"])
    total_wh = Gauge('total_wh', 'Total watt-hours', ["host"])
    
    while True:
        process_request()

