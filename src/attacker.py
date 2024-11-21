import socket
import struct
import time

from threading import Thread
from typing import Tuple


address = ('localhost', 4000)


def encode(address: Tuple[str, int]) -> bytes:
    host, port = address
    return socket.inet_aton(host) + struct.pack('H', port)


def decode(data: bytes) -> Tuple[str, int]:
    host = socket.inet_ntoa(data[:4])
    port = struct.unpack('H', data[4:])[0]
    return host, port


def attacker(server):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b'', server)
        data = s.recv(6)
        victim = decode(data)

        print('victim:', *victim)

        s.sendto(b'hello victim', victim)


def server(address):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(address)
        _, attacker = s.recvfrom(1)
        _, victim = s.recvfrom(1)
        s.sendto(encode(victim), attacker)


serve = Thread(target=server, args=(address,))
attack = Thread(target=attacker, args=(address,))

serve.start()
time.sleep(1)
attack.start()

serve.join()
attack.join()
