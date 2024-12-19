import socket
import struct

from typing import Tuple
from threading import Thread


def decode(data: bytes) -> Tuple[str, int]:
    host = socket.inet_ntoa(data[:4])
    port = struct.unpack("H", data[4:])[0]
    return host, port


def send():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b"s", ("localhost", 5319))
        peer = decode(s.recv(6))
        while True:
            data = input()
            s.sendto(data.encode(), peer)


def recv():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b"r", ("localhost", 5319))
        while True:
            print(s.recv(1024).decode())


if __name__ == "__main__":
    Thread(target=send).start()
    Thread(target=recv).start()
