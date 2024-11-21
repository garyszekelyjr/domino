import socket


server = ('localhost', 4000)


def victim(server):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(b'', server)
        data, attacker = s.recvfrom(1024)
        print(f'from {attacker}:', data.decode())


victim(server)
