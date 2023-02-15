from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
import logging
# import os



# print(bcolors.HEADER+"Welcome to FTP Chat!"+bcolors.ENDC)
# who = input("Enter your name: ")

#SERVER ADDRESS
addr = ('127.0.0.1', 2121)

authorizer=DummyAuthorizer()
authorizer.add_anonymous('.',perm='elradfmwM')

handler=FTPHandler
handler.authorizer=authorizer
logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
server=FTPServer(addr,handler)
server.serve_forever()

# send()