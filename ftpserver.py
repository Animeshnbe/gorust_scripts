import socket
import sys
import time
import os
import struct

print("\nWelcome to my FTP server using sockets.\n\nTo get started, connect a client.")

# Initialise socket
TCP_IP = "127.0.0.1"
TCP_PORT = 5050
BUFFER_SIZE = 1024 # Standard size
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
conn, addr = s.accept()  #blocking toe
cur = "/"
root = os.getcwd()

print("\nConnected from address: {}".format(addr))

def list_files():
    listing = os.listdir(os.getcwd())
    # Parse directory
    conn.send(struct.pack("i", len(listing)))
    total_directory_size = 0
    # Send over the file names and sizes whilst totaling the directory size
    for file in listing:
        # File name size
        conn.send(struct.pack("i", sys.getsizeof(file)))
        # File name
        conn.send(file.encode())
        # File content size
        conn.send(struct.pack("i", os.path.getsize(file)))
        total_directory_size += os.path.getsize(file)
        # Client and server sync
        conn.recv(2)
    # Sum of file sizes in directory
    conn.send(struct.pack("i", total_directory_size))
    #Final check
    conn.recv(BUFFER_SIZE)
    print("Successfully sent file listing")
    return

def upload():
    conn.send(b"1")
    # Receive file name length, then file name
    file_name_size = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_size).decode()
    # Ready for document content
    conn.send(b"1")
    # Receive file size
    file_size = struct.unpack("i", conn.recv(4))[0]
    # Initialise and start to receive file content
    start_time = time.time()
    with open(file_name, "wb") as output_file:
        bytes_recieved = 0
        print("\nReceiving...")
        while bytes_recieved < file_size:
            l = conn.recv(BUFFER_SIZE)
            output_file.write(l)
            bytes_recieved += BUFFER_SIZE
            print(bytes_recieved)
    print("\nUploaded file: {}".format(file_name))
    conn.send(struct.pack("f", time.time() - start_time))
    conn.send(struct.pack("i", file_size))
    return

def download():
    conn.send(b"1")
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    print(file_name)
    if os.path.isfile(file_name):
        # Then the file exists, and send file size
        conn.send(struct.pack("i", os.path.getsize(file_name)))
    else:
        # Then the file doesn't exist, and send error code
        print("File name",file_name," invalid")
        conn.send(struct.pack("i", -1))
        return
    # Wait for ok to send file
    conn.recv(BUFFER_SIZE)
    # Enter loop to send file
    start_time = time.time()
    print("Sending file...")
    content = open(file_name, "rb")
    # Again, break into chunks defined by BUFFER_SIZE
    l = content.read(BUFFER_SIZE)
    while l:
        conn.send(l)
        l = content.read(BUFFER_SIZE)
    content.close()
    # Get client go-ahead, then send download details
    conn.recv(BUFFER_SIZE)
    conn.send(struct.pack("f", time.time() - start_time))
    return

def delete_file():
    # Get file details
    file_name_length = struct.unpack("h", conn.recv(2))[0]
    file_name = conn.recv(file_name_length).decode()
    # Check if file exists
    if os.path.isfile(file_name):
        conn.send(struct.pack("i", 1))
    else:
        # Then the file doesn't exist
        conn.send(struct.pack("i", -1))
    # Wait for deletion conformation
    confirm_delete = conn.recv(BUFFER_SIZE).decode()
    if confirm_delete == "Y":
        try:
            # Delete file
            os.remove(file_name)
            conn.send(struct.pack("i", 1))
        except:
            # Unable to delete file
            print("Failed to delete {}".format(file_name))
            conn.send(struct.pack("i", -1))
    else:
        # User abandoned deletion
        # The server probably recieved "N", but else used as a safety catch-all
        print("Delete cancelled!")
        return

def send_dir():
    conn.send(cur.encode())

def change_dir(dname):
    try:
        os.chdir(root+"/"+dname)
        global cur
        cur = "/"+dname
        conn.send(struct.pack("h", 1))
    except Exception as ex:
        print("Couldn't change directory ",ex)
        conn.send(struct.pack("h", 0))

def stop():
    conn.send(b"1")
    # inform all connected clients and close
    os.chdir(root)
    conn.close()
    s.close()
    os.execl(sys.executable, sys.executable, *sys.argv)

init_path = conn.recv(BUFFER_SIZE).decode()
if init_path!='/':
    print("Changing to", init_path)
    change_dir(init_path)
else:
    conn.send(struct.pack("h", 1))

while True:
    # Enter into a while loop to recieve commands from client
    print("\n\nWaiting for instruction")
    data = conn.recv(BUFFER_SIZE).decode()
    print("\nRecieved instruction: {}".format(data))
    # Check the command and respond correctly
    if data == "LIST":
        list_files()
    elif data == "PWD":
        send_dir()
    elif data == "CWD":
        dname = conn.recv(BUFFER_SIZE).decode()
        change_dir(dname)
    elif data == "UPLD":
        upload()
    elif data == "DWLD":
        download()
    elif data == "DELF":
        delete_file()
    elif data == "QUIT":
        stop()
    else:
        print("Unexpected cmd... ")
        continue

    data = None