from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from ftplib import FTP
from datetime import datetime as dt
import os
import threading
import time
import logging

savedSet = set()
savedUsr = set()
# mypath='inbox'

def rcv(por):
    mypath = por+"_inbox"
    global savedSet
    global savedUsr
    global time
    while True:
        nameSet=set()
        for file in os.listdir(mypath):
            fullpath=os.path.join(mypath, file)
            if os.path.isfile(fullpath):
                nameSet.add(file)

        retrievedSet=set()
        for name in nameSet:
            stat=os.stat(os.path.join(mypath, name))
            # size=stat.ST_SIZE
            retrievedSet.add((name,stat.st_mtime))

        newSet=retrievedSet-savedSet
        # deletedSet=savedSet-retrievedSet

        for msg in nameSet-savedUsr:
            print(msg.split('.')[0]+" has joined the chat.\n\n")
            
        for msg in newSet:
            msg_file = msg[0]
            name = msg_file.split('.')[0]
            # print("Opening ",mypath+"/"+msg_file)
            with open(mypath+"/"+msg_file, 'r+') as fp:
                last_read = int(fp.readline())
                i = 0
                for m in fp.readlines():
                    if i>=last_read:
                        print(name+"> "+m)
                    i+=1
                
                fp.seek(0)
                fp.write(str(i))
            mod = (msg_file,os.stat(os.path.join(mypath, msg_file)).st_mtime)
            retrievedSet.remove(msg)
            retrievedSet.add(mod)

        savedSet=retrievedSet
        savedUsr=nameSet
        time.sleep(1)

def send():
    who = input("Enter your name: ")
    while True:
        por = input("Enter port of receiver, 0 to exit: ")
        if (por=="0"):
            # os.remove(who+".txt")
            print("Server> Bye!")
            break

        try:
            p = int(por)
            if (p>9999 or p<1000):
                print("Please enter a valid choice!")
                continue
        except ValueError:
            print("Please enter a valid choice!")
            continue
        ftp = FTP()
        try:
            ftpResponse = ftp.connect(host="127.0.0.1", port=p)

            print(ftpResponse)
        except Exception:
            print("Cannot connect to receiver ",por)
            continue
        ftpResponse = ftp.login()
        ftpResponse = ftp.cwd("/"+por+"_inbox")
        print(ftpResponse)
        cre = True

        while True:
            try:
                ch = int(input("Enter 1 to continue sending msgs, 0 to switch: "))
            except ValueError:
                print("Please enter a valid choice!")
                continue
            if (ch!=1 and not cre):
                os.remove(who+".txt")
                ftp.rename(who+".txt",who+"_old.txt") #keep inbox
                break
            msg = input("Enter you msg> ")
            if msg=="WHO AM I":
                print("Server> "+who)
                continue
            fileName = who+".txt"
            # if cre:
            if fileName not in os.listdir('.'):
                with open(fileName, 'w') as fp: #raw file created to upload
                    fp.write("0\n")
                    fp.write(str(dt.now())+": "+msg)
            else:
                with open(fileName, 'w') as fp: #raw file created to upload
                    fp.write("\n"+str(dt.now())+": "+msg)
            fin = open(fileName, 'rb')
            cre = False
            
            # ftp.mkd(dir)
            # files = []
            # ftp.retrlines('LIST', files.append)
            # for f in files:
            #     print(f)

            # files = []
            # ftp.dir(files.append)


            storeCommand = "APPE %s"%fileName;  #Saving history
            # storeCommand = "STOR %s"%fileName;

            ftpResponse = ftp.storbinary(storeCommand, fin, 1)
            fin.close()
            print(ftpResponse)
        

selfp = input("Enter your own port: ")
addr = ('127.0.0.1', int(selfp))
try:
    os.mkdir(selfp+"_inbox")
except FileExistsError:
    pass
authorizer=DummyAuthorizer()
# authorizer.add_user('anm8','1234','C:/Users/ani_d/Documents/gorust_scripts',perm='elradfmw')
authorizer.add_anonymous('.',perm='elradfmwM')
handler=FTPHandler
handler.authorizer=authorizer
logging.basicConfig(filename='pyftpd.log', level=logging.INFO)
t1 = threading.Thread(target=send, args=())
t2 = threading.Thread(target=rcv, args=(selfp,))
t1.start()
t2.start()
server=FTPServer(addr,handler)
server.serve_forever()

# send()