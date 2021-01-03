##Credit to https://github.com/softScheck/tplink-smartplug/blob/master/tplink_smartplug.py

import os
import socket
import json
import random
from struct import pack
from time import time, sleep
from prometheus_client import start_http_server, Summary, Gauge


def process_request():
    hosts_env_var = os.getenv('HS1X_HOSTS') or "192.168.1.156:9999,192.168.1.159:9999"
    hosts = hosts_env_var.split(',')

    current_ma = Gauge('current_ma', 'Description of gauge', ["host"])
    voltage_mv = Gauge('voltage_mv', 'Description of gauge', ["host"])
    power_mw = Gauge('power_mw', 'Description of gauge', ["host"])
    total_wh = Gauge('total_wh', 'Description of gauge', ["host"])

    for val in hosts:
        hostname = val.split(':')
        ip = hostname[0]
        port = hostname[1]
        print(f'GETTING ENERGY INFO FOR {ip} {port}')
        try:
            sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_tcp.settimeout(int(10))
            sock_tcp.connect((str(ip), int(port)))
            sock_tcp.settimeout(None)
            sock_tcp.send(encrypt('{"emeter":{"get_realtime":{}}}'))
            data = sock_tcp.recv(2048)
            sock_tcp.close()

            decrypted = decrypt(data[4:])

            result = json.loads(decrypted)
            print(result)
            result = result["emeter"]["get_realtime"]

            current_ma.labels(val).set(result["current_ma"])
            voltage_mv.labels(val).set(result["voltage_mv"])
            power_mw.labels(val).set(result["power_mw"])
            total_wh.labels(val).set(result["total_wh"])

        except socket.error:
            quit(f"Could not connect to host {ip}:{port}")
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
    # Start up the server to expose the metrics.
    start_http_server(9784)
    # Generate some requests.
    while True:
        process_request()

