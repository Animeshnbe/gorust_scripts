from ftplib import FTP, all_errors
from datetime import datetime as dt
import os
import time
import sys

class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if len(sys.argv)<3:
    sys.exit("Invalid arguments")

print(bcolors.HEADER+"Welcome to FTP Chat!"+bcolors.ENDC)
who = sys.argv[1]
os.chdir(sys.argv[2])

def downloader(ftp,fpath):
    try:
        file_copy = fpath.split('/')[-1]
        with open(file_copy, 'wb') as fp:
            res = ftp.retrbinary('RETR ' + fpath, fp.write)
            if not res.startswith('226 Operation success') and not res.startswith('226 Transfer complete'):
                print('Download failed')
                if os.path.isfile(file_copy):
                    os.remove(file_copy)

    except all_errors as e:
        print('FTP error:', e)

        if os.path.isfile(file_copy):
            os.remove(file_copy)

def rcv(ftp):
    global who
    ftp.cwd('../')
    files = ftp.nlst()
    if who+"_inbox" not in files:
        ftp.mkd(who+"_inbox")
    
    ftp.cwd(who+"_inbox")
    global time
    retrievedSet = set()
    while len(retrievedSet)==0:
        files = ftp.mlsd()
        for file in files:
            if file[0].find("_join")==-1:
                retrievedSet.add((file[0],float(file[1]['modify'])))
            
        for msg in retrievedSet:
            msg_file = msg[0]
            downloader(ftp,msg_file)
            name = msg_file.split('.')[0].split('_')[0]
            # print("Opening ",mypath+"/"+msg_file)
            with open(msg_file, 'r+') as fp:
                for m in fp.readlines():
                    # if i>=last_read:
                    print("\n"+bcolors.OKGREEN+name+"> "+m+bcolors.ENDC)
                    # f2.write(m+"\n")

            os.remove(msg_file)
            ftp.delete(msg_file)

        time.sleep(1)

ftp = FTP()
# ip = input("Enter ip of server: ")
ip = "127.0.0.1"
ops = {}
try:
    _ = ftp.connect(host=ip, port=2121)
    ftpResponse = ftp.login()
    print("Success")

except Exception:
    print(bcolors.FAIL+"Cannot connect to FTP server here"+bcolors.ENDC)
else:
    while True:
        downloader(ftp,"serve/servers.txt")  #connect to SV0 to check # *REGISTRY
        print("Available servers: ")
        with open('servers.txt','r') as fp:
            for server in fp.readlines():
                line = server.split()
                ops[line[0]] = line[1]   #FOR LOOKUP
                print("For ",line[0],": ",line[1])

        op = input("Enter name of operation, 0 to exit: ")
        # TO SEND IN DIFFERENT MACHINE
        if op=="0":
            print("Server> Bye!")
            os.remove('servers.txt')
            break
        if op not in ops:
            print("Invalid operation")
            continue
        try:
            dest = ops[op]
        except Exception:
            print(bcolors.FAIL+"Cannot connect to receiver "+dest+bcolors.ENDC)
            continue
        
        cre = False
        while True:
            ftp.cwd("/"+dest+"_inbox")
            print(ftp.pwd())
            try:
                ch = int(input("Enter 1 to continue, 0 to switch: ")) #session check
            except ValueError:
                print(bcolors.FAIL+"Please enter a valid choice!"+bcolors.ENDC)
                continue

            if (ch!=1): # *SESSION DESTROY
                # ftp.rename(who+".txt",who+"_old.txt") #keep inbox
                ftp.delete(who+"_join.txt")
                ftp.cwd('../')
                break
            msg = input("Enter you msg> ")
            fileName = who+"_"+str(int(time.time()))+".txt"

            with open(fileName, 'w') as fp: #raw file created to upload
                fp.write(dest+": "+msg)
            fin = open(fileName, 'rb')


            # storeCommand = "APPE %s"%fileName;  #Saving history
            storeCommand = "STOR %s"%fileName;

            _ = ftp.storbinary(storeCommand, fin, 1)
            fin.close()
            os.remove(fileName)
            rcv(ftp)
            ftp.cwd('../')
            # print(ftpResponse)
            cre = True
    ftp.quit()