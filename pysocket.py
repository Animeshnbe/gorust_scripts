import socket
import os
import struct
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP
from datetime import datetime as dt
import os
import threading
import logging

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# port = 80
# ip = socket.gethostbyname('www.google.com')

# print(ip)
# s.connect((ip,port))

# if os.path.isfile("C:/Users/ani_d/Documents/2022201027_activity1.pdf"):
#     print("YA")
# else:
#     print("Neon")
#     # Then the file doesn't exist
#     conn.send(struct.pack("i", -1))


ftp = FTP()

def read():
    fp = open("2201_inbox/Aman.txt", 'r+')
    last_read = int(fp.readline())
    print(last_read)
    i = 0
    for m in fp.readlines():
        if i>=last_read:
            print("Aman > "+m)
        i+=1
    
def send():
    print(os.getcwd())
    fileName = "Aman.txt"
    msg = input("Send now ")
    with open(fileName, 'w') as fp: #raw file created to upload
        fp.write("\n"+str(dt.now())+": "+msg)
    fin = open(fileName, 'rb')
    ftpResponse = ftp.connect(host="127.0.0.1", port=2201)
    ftpResponse = ftp.login()
    ftpResponse = ftp.cwd("/2201_inbox")

    
    storeCommand = "APPE %s"%fileName;  #Saving history
            # storeCommand = "STOR %s"%fileName;

    ftpResponse = ftp.storbinary(storeCommand, fin, 1)
    fin.close()

authorizer=DummyAuthorizer()
# authorizer.add_user('anm8','1234','C:/Users/ani_d/Documents/gorust_scripts',perm='elradfmw')
authorizer.add_anonymous('.',perm='elradfmwM')
handler=FTPHandler
handler.authorizer=authorizer
logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
t1 = threading.Thread(target=send, args=())
t2 = threading.Thread(target=read, args=())
t1.start()
t2.start()
addr = ('127.0.0.1', 2201)
server=FTPServer(addr,handler)
server.serve_forever()