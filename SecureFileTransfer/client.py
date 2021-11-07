import socket
import inquirer
import ntpath
import os

class Client():
    def __init__(self):
        self.host = "18.216.151.152"
        self.port = 5588
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_to_server(self):
        try_connect = True
        while try_connect:
            try:
                self.sock.connect((self.host, self.port))
                print("\033[1m" + "Success: " + "\033[0m" + "Connected to server\n")
                break
            except ConnectionRefusedError:
                self.sock.close()
                confirm = {inquirer.Confirm(
                    "try_connect",
                    message="Unable to connect to server. Try again?",
                    default=True
                )}
                try_connect = inquirer.prompt(confirm)["try_connect"]
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    def connect_to_peer(self):
        first_message = self.sock.recv(1024).decode()
        print(first_message)
        if first_message == "Waiting for peer...":
            second_message = self.sock.recv(1024).decode()
            print(second_message)
        print()

    def establish_sender_receiver(self):
        while True:
            list = [inquirer.List(
                "client_type",
                message="Select connection type",
                choices = [
                    "Sender",
                    "Receiver",
                    "Quit"
                ]
            )]
            client_type = inquirer.prompt(list)["client_type"]
            self.sock.send(client_type.encode())
            res = self.sock.recv(1024).decode()
            if res == "Success":
                return client_type
            else:
                print("Failure: Establishing sender/receiver\n")

    def send_file(self, file_path):
        try:
            file = open(file_path, "rb")
            data = file.read()
            self.sock.send(data)
            print("\033[1m" + "Success: " + "\033[0m" + "Send file\n")
            return True
        except Exception as e:
            print("\033[1m" + "Failure: " + "\033[0m" + str(e) + "\n")
            return False          

    def make_new_destination_directory(self, directory_path):
        try:
            os.mkdir(directory_path)
            os.chdir(directory_path)
            print("\033[1m" + "Success: " + "\033[0m" + "Make new destination directory\n")
            self.sock.send("Ready".encode())
            return True
        except Exception as e:
            print("\033[1m" + "Failure: " + "\033[0m" + str(e) + "\n")
            return False

    def use_existing_destination_directory(self, directory_path):
        try:
            os.chdir(directory_path)
            print("\033[1m" + "Success: " + "\033[0m" + "Use existing destination directory\n")
            self.sock.send("Ready".encode())
            return True
        except Exception as e:
            print("Failure: " + str(e) + "\n")
            return False

    def receive_file(self):
        try:
            file_name = input("Enter name for received file: ")
            file = open(file_name, "wb")
            file_data = self.sock.recv(1024)
            self.sock.settimeout(3)
            while file_data:
                file.write(file_data)
                try:
                    file_data = self.sock.recv(1024)
                except socket.timeout:
                    break
            self.sock.settimeout(None)
            print("\033[1m" + "Success: " + "\033[0m" + "Receive file\n")
            return True
        except Exception as e:
            print("\033[1m" + "Failure: " + "\033[0m" + str(e) + "\n")
            return False

if __name__ == "__main__":
    client = Client()
    client.connect_to_server()
    client.connect_to_peer()
    client_type = client.establish_sender_receiver()
    if client_type == "Sender": 
        print("Waiting for receiver...")
        client.sock.recv(1024)
        print("Receiver ready\n")
        while True:  
            list = [inquirer.List(
                "commands",
                message="Select command",
                choices = [
                    "Send file",
                    "Quit"
                ]
            )]
            command = inquirer.prompt(list)["commands"]
            if command == "Send file":
                file_path = input("Enter absolute path to file: ")
                client.send_file(file_path)
            else:
                break
    elif client_type == "Receiver":
        list = [inquirer.List(
            "commands",
            message="Select command",
            choices = [
                "Make new destination directory",
                "Use existing destination directory",
                "Quit"
            ]
        )]
        command = inquirer.prompt(list)["commands"]
        if command == "Make new destination directory":
            while True:
                directory_path = input("Enter desired absolute path (including directory name) for the new directory: ")
                res = client.make_new_destination_directory(directory_path)
                if res:
                    break
        elif command == "Use existing destination directory":
            while True:
                directory_path = input("Enter absolute path for the existing directory: ")
                res = client.use_existing_destination_directory(directory_path)
                if res:
                    break
        if command != "Quit":
            while True:
                list = [inquirer.List(
                    "commands",
                    message="Select command",
                    choices = [
                        "Receive file",
                        "Quit"
                    ]
                )]
                command = inquirer.prompt(list)["commands"]
                if command == "Receive file":
                    client.receive_file()
                else:
                    break
