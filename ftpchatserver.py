from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP
from datetime import datetime as dt
import os
import threading
import time
import logging

# users = {"Stokes":0,"Warner":0,"Bavuma":0,"Kohli":0}

# mypath='inbox'

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# print(bcolors.HEADER+"Welcome to FTP Chat!"+bcolors.ENDC)
# who = input("Enter your name: ")

#SERVER ADDRESS
addr = ('127.0.0.1', 2121)

authorizer=DummyAuthorizer()
authorizer.add_anonymous('.',perm='elradfmwM')
# authorizer.add
handler=FTPHandler
handler.authorizer=authorizer
logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
# t2 = threading.Thread(target=rcv, args=(selfp,))
# t2.start()
server=FTPServer(addr,handler)
server.serve_forever()

# send()