from ftplib import FTP, all_errors
from datetime import datetime as dt
import os
import threading
import time

savedSet = set()
savedUsr = set()
stp = False

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

print(bcolors.HEADER+"Welcome to FTP Chat!"+bcolors.ENDC)
who = input("Enter your name: ")

def downloader(ftp,file_copy):
    try:
        with open(file_copy, 'w') as fp:
            res = ftp.retrlines('RETR ' + file_copy, fp.write)
            if not res.startswith('226 Operation success') and not res.startswith('226 Transfer complete'):
                print('Download failed')
                if os.path.isfile(file_copy):
                    os.remove(file_copy)

    except all_errors as e:
        print('FTP error:', e)

        if os.path.isfile(file_copy):
            os.remove(file_copy)

def add(msg):
    nums = msg[32:-1].split(',')
    s = 0
    for n in nums:
        s+=int(n)
    return s

def sub(msg):
    n = msg[32:-1].split(',')
    return int(n[0])-int(n[1])

def mult(msg):
    n = msg[33:-1].split(',')
    return int(n[0])*int(n[1])

def process(ftp,msg_file):
    downloader(ftp,msg_file)
    name = msg_file.split('.')[0].split('_')[0]
    # print("Opening ",mypath+"/"+msg_file)
    with open(msg_file, 'r+') as fp, open(name+"_old.txt","a") as f2:
        # last_read = int(fp.readline())
        # i = 0
        for m in fp.readlines():
            # if i>=last_read:
            print("\n"+bcolors.OKGREEN+name+"> "+m+bcolors.ENDC)
            if (m.find("add")!=-1): # processing message
                s = add(m)
                sendback = who+"_"+str(int(time.time()))+".txt"
                with open(sendback, 'w') as fp: #raw file created to upload
                    fp.write("\nSum: "+str(s))
                fin = open(sendback, 'rb')
                rpc = FTP()
                rpc.connect(host="127.0.0.1", port=2121)
                rpc.login()
                rpc.cwd("/"+name+"_inbox")
                _ = rpc.storbinary("STOR "+sendback, fin, 1)
                fin.close()
                os.remove(sendback)
                rpc.quit()

                print(bcolors.BOLD+"Sum "+str(s)+bcolors.ENDC)
                
            # i+=1
            f2.write(m+"\n")
        
        # fp.seek(0)
        # fp.write(str(i))
    os.remove(msg_file)

    if name+"_join.txt" in ftp.nlst():
        ftp.delete(msg_file)
    else:
        ftp.rename(msg_file,name+"_join.txt") #first msg, helps to check join chat

def rcv():
    global who
    ftp = FTP()
    # ip = input("Enter ip of receiver: ")
    ip = "127.0.0.1"
    try:
        _ = ftp.connect(host=ip, port=2121)
        _ = ftp.login()
    except Exception:
        print(bcolors.FAIL+"You may have new messages, cannot connect to FTP server!"+bcolors.ENDC)
    files = ftp.nlst()
    if who+"_inbox" not in files:
        ftp.mkd(who+"_inbox")
    
    ftp.cwd(who+"_inbox")

    global savedSet
    global savedUsr
    global time
    global stp
    while True:
        if stp:
            ftp.quit()
            break
        nameSet=set()
        retrievedSet=set()
        files = ftp.mlsd()
        for file in files:
            nameSet.add(file[0].split('_')[0])
            if file[0].find("_join")==-1:
                retrievedSet.add((file[0],float(file[1]['modify'])))

        newSet=retrievedSet-savedSet
        # deletedSet=savedSet-retrievedSet

        for name in nameSet-savedUsr:
            print("\n"+bcolors.WARNING+bcolors.UNDERLINE+name+" has joined the chat.\n"+bcolors.ENDC)
        for name in savedUsr-nameSet:
            print("\n"+bcolors.WARNING+bcolors.UNDERLINE+name+" has left the chat.\n"+bcolors.ENDC)
            
        for msg in newSet:
            msg_file = msg[0]
            t = threading.Thread(target=process, args=(ftp,msg_file))
            t.start()

            # mod = (msg_file,os.stat(os.path.join(mypath, msg_file)).st_mtime)
            # retrievedSet.remove(msg)
            # retrievedSet.add(mod)

        savedSet=retrievedSet
        savedUsr=nameSet
        time.sleep(1)


# send()

ftp = FTP()
# ip = input("Enter ip of server: ")
ip = "127.0.0.1"
try:
    _ = ftp.connect(host=ip, port=2121)
    ftpResponse = ftp.login()
    print("Success")
except Exception:
    print(bcolors.FAIL+"Cannot connect to FTP server here"+bcolors.ENDC)
else:
    t2 = threading.Thread(target=rcv, args=())
    t2.start()
    while True:
        dest = input("Enter name of receiver, 0 to exit: ")
        # TO SEND IN DIFFERENT MACHINE
        if dest=="0":
            print("Server> Bye!")
            stp = True
            break
        try:
            ftpResponse = ftp.cwd("/"+dest+"_inbox")
            print(ftpResponse)
        except Exception:
            print(bcolors.FAIL+"Cannot connect to receiver "+dest+bcolors.ENDC)
            continue
        
        cre = False
        while True:
            try:
                ch = int(input("Enter 1 to continue sending msgs, 0 to switch: "))
            except ValueError:
                print(bcolors.FAIL+"Please enter a valid choice!"+bcolors.ENDC)
                continue

            if (ch!=1):
                # ftp.rename(who+".txt",who+"_old.txt") #keep inbox
                if cre:
                    ftp.delete(who+"_join.txt")
                break
            msg = input("Enter you msg> ")
            if msg=="WHO AM I":
                print(bcolors.OKGREEN+"Server> "+who+bcolors.ENDC)
                continue
            fileName = who+"_"+str(int(time.time()))+".txt"
            # if cre:
            # files = ftp.nlst()
            # ftp.retrlines('LIST', files.append)
            with open(fileName, 'w') as fp: #raw file created to upload
                fp.write(str(dt.now())+": "+msg)
            fin = open(fileName, 'rb')


            # storeCommand = "APPE %s"%fileName;  #Saving history
            storeCommand = "STOR %s"%fileName;

            ftpResponse = ftp.storbinary(storeCommand, fin, 1)
            fin.close()
            os.remove(fileName)
            print(ftpResponse)
            cre = True
    ftp.quit()