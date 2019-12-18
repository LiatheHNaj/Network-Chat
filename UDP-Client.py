import socket

import time
import socket
import sys

print("Welcome to HELL")
print("")
print("Initializing...")
time.sleep(1)


# Bind client socket
clientHost = socket.gethostname() # "127.0.0.1"
clientPort = 9996
s =socket.socket()
s.bind((clientHost, clientPort)) 

print("")

# Get Server data from user
host = input(str("Please enter the server address : "))
name = input(str("Please enter your name : "))
port = 9998 # Or should it be 1024 (server rcv-from port?) 
server = (host,port)

# Initialize Client as active with server
print("trying to connect to ", host , "at port", port)
time.sleep(1)

s.sendto( name.encode("ascii"), server)
print("connected..")


# connection has been established
userList = s.recv(1023)  # Set port # different from server's
users = userList.decode() # recieved user list may need to be parsed or converted to list for later comparison
print(users)

stayOnServer = True
while stayOnServer: 
    # Get user's destination and message data
    dest = str(input("Select a user to message.")).trim() # use .ignoreCase() or make users and dest UPPERCASE for comparison; 
    if dest in users: 
        break
    else: 
        print("Error - User not found in user list")
        print(users)

    keepCurrentDest = True
    while keepCurrentDest:
        msg = input("Enter your message for " + dest + ". Enter ./user to change user and ./exit to leave chat server. Enter ./wait to wait for messages.")
        
        # Check for control commands
        if msg == './user':
            keepCurrentDest = False
            break
        elif msg == './exit': 
            stayOnServer = False
            break
        elif msg == './wait': 
            print("Waiting on response ...")
            rcvMsg = s.recv(1024).decode()
            print(rcvMsg)
            break
        else: 
            # Send message -  Will eventually need user input to determine if currently wanting to send or check for recieved messages(inbox) 
            pkt = dest + ' /$MESSAGE_BREAK: ' + msg
            s.send(pkt.encode('ascii'), server)
            print("Sent!")

            # recieve messages from server
            print("Waiting on response ...")
            rcvMsg = s.recv(1024).decode()
            print(rcvMsg)

print("GoodBye!")

