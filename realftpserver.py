##pip install pyftpdlib

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

addr= ('127.0.0.1', 21)
authorizer=DummyAuthorizer()
authorizer.add_user('anm8','1234','C:\Users\ani_d\Documents\gorust_scripts',perm='elradfmw')
authorizer.add_anonymous('.')
handler=FTPHandler
handler.authorizer=authorizer
server=FTPServer(addr,handler)
server.serve_forever()
