import socket
import struct

from typing import Tuple


address = ('localhost', 4000)


def encode(address: Tuple[str, int]) -> bytes:
    host, port = address
    return socket.inet_aton(host) + struct.pack('H', port)


def server(address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.bind(address)
            while True:
                _, attacker = s.recvfrom(1)
                _, victim = s.recvfrom(1)
                s.sendto(encode(victim), attacker)
        except KeyboardInterrupt:
            pass


server(address)
