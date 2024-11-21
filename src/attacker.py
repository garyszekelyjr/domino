import socket
import struct

from typing import Tuple


server = ('localhost', 4000)


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


attacker(server)
