import socket
import sys
import os
import struct

IP = "127.0.0.1"
PORT = 5050 
BUFFER_SIZE = 1024
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connected = False

def conn():
    # Connect to the server
    addr = input("Enter the address (/ for default): ").split("/")
    if len(addr)>2:
        global IP
        global PORT
        global connected
        IP,RAWPORT = addr[2].split(":")
        PORT = int(RAWPORT) if RAWPORT else PORT
        print("Sending server request... ",IP,PORT)
        try:
            s.connect((IP, PORT))
            connected = True
            print("Connected sucessfully...")
            if len(addr)>3 and addr[3]!='':
                s.send("/".join(addr[3:]).encode())
            else:
                s.send(b"/")
            status = struct.unpack("h", s.recv(2))[0]
            if not status:
                print("404 Not Found, exiting...")
                stop()
            return status
        except Exception as ex:
            print("Connection unsucessful. Server may be offline. ", ex)
            return 0
    else:
        try:
            s.connect((IP, PORT))
            connected = True
            print("Connected sucessfully...")
            s.send(b"/")
            status = struct.unpack("h", s.recv(2))[0]
            return status
        except Exception as ex:
            print("Connection unsucessful. Server may be offline. ", ex)
            return 0

def inform(msg):
    try:
        # Make upload request
        s.send(msg.encode())
        return 1
    except Exception as ex:
        print("Couldn't send server request because ",ex)
        return 0

def list_files():
    # List the files avaliable on the file server
    print("Requesting files...\n")
    if (not inform("LIST")):
        return
    try:
        no_of_files = struct.unpack("i", s.recv(4))[0]
        for i in range(int(no_of_files)):
            # Get the file name size first to reduce amount transferred over socket
            file_name_size = struct.unpack("i", s.recv(4))[0]
            file_name = s.recv(file_name_size).decode()
            file_size = struct.unpack("i", s.recv(4))[0]
            print("\t{} - {}b".format(file_name, file_size))
            # client and server are sync
            s.send(struct.pack("h", 1))

        total_directory_size = struct.unpack("i", s.recv(4))[0]
        print("\nTotal directory size: {}b".format(total_directory_size))
    except Exception as ex:
        print("Couldn't retrieve listing ",ex)
        return
    try:
        # Final check
        s.send(b"1")
        return
    except Exception:
        print("Couldn't get final server confirmation")
        return

def upload(file_path):
    # Upload a file, eg. C:/Users/ani_d/Documents/readme.txt
    print("\nUploading file: {}...".format(file_path))
    if not os.path.isfile(file_path):
        print ("Couldn't open file. Make sure the filename was entered correctly.")
        return
    if (not inform("UPLD")):
        return
    try:
        # Wait for server acknowledgement then send file details
        s.recv(BUFFER_SIZE)
        s.send(struct.pack("h", sys.getsizeof(file_path)))
        file_name = os.path.basename(file_path)
        s.send(file_name.encode())
        s.recv(BUFFER_SIZE)
        fs = os.path.getsize(file_path)
        s.send(struct.pack("i", fs))
        print("Tot tbs", fs)
    except Exception:
        print("Error sending file details")
    try:
        # Send the file in chunks defined by BUFFER_SIZE
        with open(file_path, "rb") as fh:
            l = fh.read(BUFFER_SIZE)
            print("\nSending...")
            while l:
                s.send(l)
                l = fh.read(BUFFER_SIZE)
                print("sending")
        # Get upload performance details
        upload_time = struct.unpack("f", s.recv(4))[0]
        upload_size = struct.unpack("i", s.recv(4))[0]
        print("\nSent file: {}\nTime elapsed: {}s\nFile size: {}b".format(file_name, upload_time, upload_size))
    except Exception:
        print("Error sending file")
        return
    return

def download(file_name):
    # Download given file
    print("Downloading file: {}".format(file_name))
    if (not inform("DWLD")):
        return
    try:
        # Wait for server ok, then make sure file exists
        s.recv(BUFFER_SIZE)
        # Send file name length, then name
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
        # Get file size (if exists)
        file_size = struct.unpack("i", s.recv(4))[0]
        if file_size == -1:
            print("File does not exist")
            return
    except Exception as ex:
        print("Error checking file", ex)
    try:
        s.send(b"1")
        output_file = open(file_name, "wb")
        bytes_recieved = 0
        print("\nDownloading...")
        while bytes_recieved < file_size:
            # File broken into chunks and written
            l = s.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_recieved += BUFFER_SIZE
        output_file.close()
        print("Successfully downloaded {}".format(file_name))
        s.send(b"1")
        time_elapsed = struct.unpack("f", s.recv(4))[0]
        print("Time elapsed: {}s\nFile size: {}b".format(time_elapsed, file_size))
    except Exception:
        print("Error downloading file")
        return
    return

def get_wd():
    if (not inform("PWD")):
        return
    try:
        dirname = s.recv(BUFFER_SIZE)
        print("\nCurrent File path: ",dirname.decode())
    except Exception:
        print("Failed to get present directory")
        return

def change_wd(newd):
    if (not inform("CWD")):
        return
    try:
        s.send(newd.encode())
        status = struct.unpack("h", s.recv(2))[0]
        print("\nStatus: ",status)
    except Exception:
        print("Failed to change present directory")
        return

def delete_file(file_name):
    # Delete specific file from file server
    print("Deleting file: {}...".format(file_name))
    if (not inform("DELF")):
        return
    try:
        # Send filename's length, then filename
        s.send(struct.pack("h", sys.getsizeof(file_name)))
        s.send(file_name.encode())
    except Exception:
        print("Couldn't send file details")
        return
    try:
        # Get conformation that file does/doesn't exist
        exists = struct.unpack("i", s.recv(4))[0]
        if exists == -1:
            print("The file does not exist on server")
            return
    except Exception:
        print("Couldn't check file existence")
        return
    # Confirm whether to delete file
    confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
    while confirm_delete not in ["Y", "N", "YES", "NO"]:
        print("Command invalid, try again")
        confirm_delete = input("Are you sure you want to delete {}? (Y/N)\n".format(file_name)).upper()
    try:
        # Send conformation
        if confirm_delete == "Y" or confirm_delete == "YES":
            # User wants to delete file
            s.send(b"Y")
            # Wait for conformation file has been deleted
            delete_status = struct.unpack("i", s.recv(4))[0]
            if delete_status == 1:
                print("File successfully deleted")
                return
            else:
                print("File failed to be deleted")
                return
        else:
            s.send(b"N")
            print("Delete cancelled!")
            return
    except Exception:
        print("Couldn't delete file")
        return

def stop():
    if not connected:
        print("Connect to server first")
        return
    s.send(b"QUIT")
    # Wait for server go-ahead
    s.recv(BUFFER_SIZE)
    s.close()
    print("Server connection ended")

print("\n\nWelcome to my FTP client.\n\nCommand index:\nCONN           : Connect to server\
    \nLIST           : List files\nPWD           : Get present directory\
    \nCWD           : Change present directory\nUPLD file_path : Upload file\
    \nDWLD file_path : Download file\nDELF file_path : Delete file\nQUIT           : Exit")

status = 1
while status:
    # Listen for a command
    prompt = input("\nEnter a command: ")
    if prompt[:4].upper() == "CONN":
        status = conn()
    elif prompt[:4].upper() == "LIST":
        list_files()
    elif prompt[:4].upper() == "UPLD":
        upload(prompt[5:])
    elif prompt[:4].upper() == "DNLD":
        download(prompt[5:])
    elif prompt[:4].upper() == "DELF":
        delete_file(prompt[5:])
    elif prompt[:3].upper() == "PWD":
        get_wd()
    elif prompt[:3].upper() == "CWD":
        change_wd(prompt[4:])
    elif prompt[:4].upper() == "QUIT":
        stop()
        break
    else:
        print("Command not recognised; please try again")