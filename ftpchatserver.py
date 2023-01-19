from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
# import os

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

# def add_user():
#     while True:
#         os.stat('.creds')
    # with open('.creds','r') as cred:
    #     for uc in cred.readlines():
    #         un, pwd = uc.split()
    #         authorizer.add_user(un,pwd,perm='elradfmwM')

authorizer=DummyAuthorizer()
authorizer.add_anonymous('.',perm='elradfmwM')

handler=FTPHandler
handler.authorizer=authorizer
logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
server=FTPServer(addr,handler)
server.serve_forever()

# send()