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
who,op = input("Enter your name, and the operation you will perform: ").split()

def downloader(ftp,file_copy):
    try:
        with open(file_copy, 'w') as fp:
            res = ftp.retrlines('RETR ' + file_copy, fp.write)
            if not res.startswith('226 Operation success') and not res.startswith('226 Transfer complete'):
                print('Download failed')
                if os.path.isfile(file_copy):
                    os.remove(file_copy)
                return False
            else:
                return True

    except all_errors as e:
        print('FTP error:', e)

        if os.path.isfile(file_copy):
            os.remove(file_copy)
        return False

def add(msg):
    nums = msg[8:-1].split(',')
    s = 0
    for n in nums:
        s+=int(n)
    return s

def sub(msg):
    n = msg[8:-1].split(',')
    return int(n[0])-int(n[1])

def mult(msg):
    n = msg[9:-1].split(',')
    return int(n[0])*int(n[1])

def inc(msg,name,ftp):
    if len(msg)>8:
        n = msg[8:-1]
    else:
        state = name+"_join.txt"
        if downloader(ftp,state):
            with open(state, 'rb') as f:
                try:  # catch OSError in case of a one line file 
                    f.seek(-2, os.SEEK_END)
                    while f.read(1) != b'\n':
                        f.seek(-2, os.SEEK_CUR)
                except OSError:
                    f.seek(0)
                last_line = f.readline().decode()
                n = 0
        else:
            return 0
    return int(n)+1

def process(ftp,msg_file,op):
    downloader(ftp,msg_file)
    name = msg_file.split('.')[0].split('_')[0]
    global who
    # print("Opening ",mypath+"/"+msg_file)
    with open(msg_file, 'r+') as fp, open(who+"_requests_old.txt","a") as f2:
        # last_read = int(fp.readline())
        # i = 0
        for m in fp.readlines():
            # if i>=last_read:
            print("\n"+bcolors.OKGREEN+name+"> "+m+bcolors.ENDC)
            try:
                if op=="add" and (m.find("add")!=-1): # revalidate
                    s = add(m)
                elif op=="subtract" and (m.find("sub")!=-1): # revalidate
                    s = sub(m)
                elif op=="multiply" and (m.find("mult")!=-1): # revalidate
                    s = mult(m)
                elif op=="increment" and (m.find("inc")!=-1): # revalidate
                    s = inc(m,name,ftp)
                else: #invalid, ignore
                    s = "Invalid request"
            except ValueError:
                s = "Could not perform the operation, recheck the request params"
            sendback = who+"_"+str(int(time.time()))+".txt"
            with open(sendback, 'w') as fp: #raw file created to upload
                fp.write("Result: "+str(s))
            fin = open(sendback, 'rb')
            rpc = FTP()
            rpc.connect(host="127.0.0.1", port=2121)
            rpc.login()
            rpc.cwd("/"+name+"_inbox")
            _ = rpc.storbinary("STOR "+sendback, fin, 1)
            fin.close()
            os.remove(sendback)
            rpc.quit()                
            # i+=1
            f2.write(name+"> "+m+"\n")  #past record
        
        # fp.seek(0)
        # fp.write(str(i))
    os.remove(msg_file)

    if name+"_join.txt" in ftp.nlst():
        # ? APPEND b4 deleting to visualize connection
        ftp.delete(msg_file)
    else:
        ftp.rename(msg_file,name+"_join.txt") #first msg, helps to check join chat

def listen(op):
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

        # * SESSION details
        for name in nameSet-savedUsr:
            print("\n"+bcolors.WARNING+bcolors.UNDERLINE+name+" has joined the chat.\n"+bcolors.ENDC)
        for name in savedUsr-nameSet:
            print("\n"+bcolors.WARNING+bcolors.UNDERLINE+name+" has left the chat.\n"+bcolors.ENDC)
            
        for msg in newSet:
            msg_file = msg[0]
            t = threading.Thread(target=process, args=(ftp,msg_file,op)) # *PARALLEL REQUESTS
            t.start()

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
    # *BOOTSTRAPPING
    ftp.cwd('serve')
    fileName = "servers.txt"
    with open(fileName,"w") as f:
        f.write(op+' '+who+'\n')
    fin = open(fileName, 'rb')
    storeCommand = "APPE %s"%fileName;

    ftpResponse = ftp.storbinary(storeCommand, fin, 1)
    fin.close()
    # !WILL CAUSE ISSUE IF BOOTSTRAP AND ALL OTHER SERVERS ARE RUNNING IN SAME LOC
    os.remove(fileName)
    ftp.quit()
except Exception:
    print(bcolors.FAIL+"Cannot connect to FTP server here"+bcolors.ENDC)
else:
    listen(op)
    # t2.start()