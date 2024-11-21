import socket

host = "172.31.41.57"
port = 5588

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(2)

def connect_peers():
    first_conn, first_addr = sock.accept()
    first_conn.send("Waiting for peer...".encode())
    second_conn, second_addr = sock.accept()
    first_conn.send("Connected to peer".encode())
    second_conn.send("Connected to peer".encode())
    return (first_conn, second_conn)

def establish_sender_receiver(first_conn, second_conn):
    while True:
        first_conn_choice = first_conn.recv(1024).decode()
        second_conn_choice = second_conn.recv(1024).decode()
        if first_conn_choice != second_conn_choice:
            if first_conn_choice == "Sender":
                first_conn.send("Success".encode())
                second_conn.send("Success".encode())
                return(first_conn, second_conn)
            else:
                first_conn.send("Success".encode())
                second_conn.send("Success".encode())
                return(second_conn, first_conn)
        else:
            first_conn.send("Failure".encode())
            second_conn.send("Failure".encode())

while True:
    first_conn, second_conn = connect_peers()
    sender, receiver = establish_sender_receiver(first_conn, second_conn)
    receiver.recv(1024)
    sender.send("Ready".encode())
    while True:
        file_name = sender.recv(1024).decode()
        receiver.send(file_name.encode())
        receiver.recv(1024)
        sender.send("Ready".encode())
        file_data = sender.recv(1024)
        file_buffer = b""
        sender.settimeout(1)
        while file_data:
            file_buffer = b"".join([file_buffer, file_data])
            try:
                file_data = sender.recv(1024)
            except socket.timeout:
                break
        sender.settimeout(None)
        receiver.send(file_buffer)
