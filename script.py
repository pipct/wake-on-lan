#!/usr/bin/env python
from os import listdir
from os.path import isfile, realpath
import re, subprocess, time, socket, struct, itertools, random, sys

from progressbar import enumerate_with_progress

directory = realpath('ipconfigs')
matcher = re.compile(r'Physical Address.*(([0-9A-F]{2}-){5}([0-9A-F]{2}))')
port = 9
AWESOME_FUN_MODE_ENABLED = True # Falsify for instant operation
if len(sys.argv) > 1:
    AWESOME_FUN_MODE_ENABLED = False

ip_options = ["10.50.{}.255".format(seg) for seg in [16, 20]]

def awesome_fun():
    if AWESOME_FUN_MODE_ENABLED:
        time.sleep(random.triangular(0.005, 0.01, 0.01))

def create_magic_packet(macaddress):
    """
    Create a magic packet which can be used for wake on lan using the
    mac address given as a parameter.
    Keyword arguments:
    :arg macaddress: the mac address that should be parsed into a magic
                     packet.
    """
    if len(macaddress) == 12:
        pass
    elif len(macaddress) == 17:
        sep = macaddress[2]
        macaddress = macaddress.replace(sep, '')
    else:
        raise ValueError('Incorrect MAC address format')

    # Pad the synchronization stream
    data = b'FFFFFFFFFFFF' + (macaddress * 20).encode()
    send_data = b''

    # Split up the hex values in pack
    for i in range(0, len(data), 2):
        send_data += struct.pack(b'B', int(data[i: i + 2], 16))

    awesome_fun()

    return send_data


packets = []
for f_name in enumerate_with_progress(listdir(directory), task_text="Making packets"):
    path = directory + "/" + f_name
    
    with open(path) as f:
        config = f.read()
        mac = matcher.search(config).group(1).replace('-',':')
        packet = create_magic_packet(mac)
        packets.append(packet)
        
for ip in ip_options:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect((ip, port))
    for packet in enumerate_with_progress(packets * 3, task_text="Sending packets to {}".format(ip)):
        awesome_fun()
        sock.send(packet)
    sock.close()
