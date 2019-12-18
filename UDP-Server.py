import socket

# Initialize Server Socket 
serverSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind Server Socket to host
serverHost = socket.gethostname() # "127.0.0.1"
serverPort = 9998
serverSock.bind((serverHost, serverPort))

# User list - Dictionary {userName: IP-Address}
users = {}

# IP list - {IP: username}
IPs = {}

# Message log
msg_log = {}

# Keep Server Process running prepared to print client requests
print("Server Online... Waiting for connections: \n")
while True:    
    clientData, clientAddr = serverSock.recvfrom(1024)
    # Try to check for Client IP in user list
    try: 
        if clientAddr in users:
            # Client UDP Data must be delimited to determine message receiver 
            try: 
                message = "From " + IPs[clientAddr] + ': ' + clientData.split(" /$MESSAGE_BREAK: ")[1]
                
                # Get IP address from user list
                destination = users[clientData.split(" /$MESSAGE_BREAK: ")[0]]  
                
                # Separate Address and port by ':' delimiter
                rcv_addr, rcv_port = destination.split(':')[0], destination.split(':')[1]
                
            except Exception as e: 
                print("Formatting Error: " + str(e))
                break
            
            # Send message to receiving IP address and port
            serverSock.sendto(message.encode, (rcv_addr, rcv_port))

        # Just in case check for user does not throw an exception to initialize unknown user  
        else: raise Exception

    # Initialize user if not in user list 
    except Exception as e:
        # Add client to user list using given user name 
        users[clientData] = clientAddr

        # Add Username to IP list
        IPs[clientAddr] = clientData

        # Send list of connected users to newly initialized user 
        serverSock.sendto(
            str(users).encode, 
            (clientAddr.split(':')[0], clientAddr.split(':')[1]) 
            ) 