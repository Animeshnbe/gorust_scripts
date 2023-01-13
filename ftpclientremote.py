import ftplib
import sys
import os

print("WELCOME TO MY FTP BROWSER")
# domain = 'ftp.us.debian.org' 
# ip = input("Enter an ip: ") # 
# port = int(input("Enter a port"))
# user = input("Enter username")
# pwd = input("Enter a password")
try:
    ftp = ftplib.FTP() # , user, pwd)
    ftp.connect(host='192.168.137.251',port=9999) #ip port
    ftp.login()
    print(ftp.getwelcome())
    print("Connected successfully...")
except Exception as ex:
    sys.exit("Could not connect to remote server")

while True:
    ch = int(input("\nEnter choice: \n1: LIST\n2: CWD\n3: PWD\n4: DWLD\n5: UPLD\n6: MKD\n EXIT\n\n"))

    if (ch==1):
        print("File List: ")
        files = []
        ftp.dir(files.append)
        for file in files:
            print(file)

    elif (ch==2):
        fp = input("Enter the path: ")
        try:
            ftp.cwd(fp) #changing to /pub/unix
        except Exception:
            print("Path is invalid")
    elif (ch==3):
        # wdir = ftp.sendcmd('PWD')
        # print(ftplib.parse257(wdir))
        print(ftp.pwd())
    elif (ch==4):
        file_orig = input("Enter filepath\t") #'/debian/README'
        file_copy = file_orig.split('/')[-1]

        try:
            with open(file_copy, 'w') as fp:
                res = ftp.retrlines('RETR ' + file_orig, fp.write)

                if not res.startswith('226 Transfer complete'):
                    print('Download failed')
                    if os.path.isfile(file_copy):
                        os.remove(file_copy)

        except ftplib.all_errors as e:
            print('FTP error:', e)

            if os.path.isfile(file_copy):
                os.remove(file_copy)

    elif ch==5:
        filepath = input("Enter filepath\t") #'README'
        if not os.path.isfile(filepath):
            print("Not a file")
            continue
        try:
            with open(filepath, 'rb') as fp:
                res = ftp.storlines("STOR " + filepath, fp)
                if not res.startswith('226 Transfer complete'):
                    print('Upload failed')

        except ftplib.all_errors as e:
            print('FTP error:', e)
    elif ch==6:
        try:
            dir = input("Enter directory name")
            ftp.mkd(dir)
            files = []
            ftp.retrlines('LIST', files.append)
            for f in files:
                print(f)
        except ftplib.all_errors as e:
            print('FTP error:', e)

    else:
        break
