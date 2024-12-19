import socket
import struct

from typing import Tuple


def encode(address: Tuple[str, int]) -> bytes:
    host, port = address
    return socket.inet_aton(host) + struct.pack("H", port)


if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind(("0.0.0.0", 5319))

        sends = []
        receives = []

        for _ in range(4):
            data, address = s.recvfrom(1)
            if data == b"s":
                sends.append(address)
            else:
                receives.append(address)

        peer_1_send, peer_2_send = sends
        peer_1_recv, peer_2_recv = receives

        if peer_1_send[0] == peer_1_recv[0] and peer_2_send[0] == peer_2_recv[0]:
            s.sendto(encode(peer_2_recv), peer_1_send)
            s.sendto(encode(peer_1_recv), peer_2_send)
