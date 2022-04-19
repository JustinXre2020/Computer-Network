# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and Netid of each member:
# Member 1: 
# Member 2: 
# Member 3: 


# Note: 
# This starter code is optional. Feel free to develop your own solution. 

# Import any necessary libraries below
import socket
import threading 
import sys
import os
from datetime import datetime
from pg3lib import *

# Any global variables
BUFFER = 2048

# Create the server public key 
key = getPubKey()

# Convert from int to byte
def sendint(data):
    return int(data).to_bytes(4, byteorder='big', signed=True)

# Convert from byte to int
def receiveint(data):
    return int.from_bytes(data, byteorder='big', signed=True)

# Get key based on value from a dictionary
def get_key(val, my_dict):
    for key, value in my_dict.items():
         if val == value:
             return key
    return "Unknown client"


# send the messages to client
def sendtoClient(sock, type, message):
    sock.send(sendint(len(type)))
    sock.send(type.encode())
    sock.send(sendint(len(message)))
    
    # these three have binary messages
    if type == "key" or type == "BM" or type == "PM":       
        sock.send(message)
    else:
        sock.send(message.encode())
    

"""
The thread target fuction to handle the requests by a user after a socket connection is established.
Args:
    args:  any arguments to be passed to the thread
Returns:
    None
"""
def chatroom (sockets, clients, address, client_keys):
    # Task1: login/register the user

    # Get the socket
    sock = sockets.get(address)

    # Receive client's username
    try:
        username_size = sock.recv(4)
    except socket.error as e:
        print("Receive size of username error!")
        sys.exit()

    try:
        username_msg = sock.recv(receiveint(username_size))
    except socket.error as e:
        print("Receive username error!")
        sys.exit()
    username = username_msg.decode()

    # Set up files for future_use
    user_info = "userinfo.txt"
    chat_history = f"{username}.txt"

    # Send server's public key to client
    sendtoClient(sock, "key", key)

    userinfo_path = os.path.join(os.getcwd(), user_info)            # generate userinfo path
    chat_history_path = os.path.join(os.getcwd(), chat_history)     # generate chat history path

    # use "r+" rather than "a+" because we need to 
    # read first and then write data down on the file
    mode = 'r+' if os.path.exists(userinfo_path) else 'w+'          # set mode (only read/write (r+) or create the file (w+))
                                                                    # based on the existance of userinfo     

    with open(userinfo_path, mode) as f:                            # create user information file to store username and password
        # Get the data from the file
        lines = f.readlines()                                       # Example lines: ["Ann, 12345\n", "John, 54231\n"]
        nested_list = [line.strip().split(',') for line in lines]
        data_list = [data for list in nested_list for data in list]

        # See if the username is in the file
        if len(data_list) == 0 or username not in data_list:        # Registration process
            f.write(username + ',')                                 # Write down the username
            
            # Inform user to type in the password
            sendtoClient(sock, "Confirmation", "Now please create your password!")

            # Receive client's password
            try:
                password_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of created password error!")
                sys.exit()
            try:
                password_msg = sock.recv(receiveint(password_size))
            except socket.error as e:
                print("Receive client's created password error!")
                sys.exit()

            # decrypt the client's password
            password = decrypt(password_msg).decode()
            # password = password_msg.decode()   

            f.write(password + '\n')            # write down the password

            # Inform client that the account has been created!
            sendtoClient(sock, "Confirmation", "Your account has been successfully created!")
   
        else:
            # Inform user to type in the password
            sendtoClient(sock, "Confirmation", "Now please type in your password!")                                    

            # If the password is wrong, go into the loop until client types in the correct password
            while True:
                # Receive client's password
                try:
                    password_size = sock.recv(4)
                except socket.error as e:
                    print("Receive size of password error!")
                    sys.exit()
                try:
                    password_msg = sock.recv(receiveint(password_size))
                except socket.error as e:
                    print("Receive password error!")
                    sys.exit()

                # decrypt the client's password
                password = decrypt(password_msg).decode()    

                # Check the password, if not in the file, inform it to the user
                if password not in data_list:
                    sendtoClient(sock, "Confirmation", "Wrong password!")   
                else:
                    # Inform client that the account has been logged in
                    sendtoClient(sock, "Confirmation", "You successfully log into your account!")    
                    break

        
    # Add the user to the list of clients
    clients.update({username : address})

    # Receive client's public key
    try:
        key_size = sock.recv(4)
    except socket.error as e:
        print("Receive size of key size error!")
        sys.exit()
    try:
        client_key = sock.recv(receiveint(key_size))
    except socket.error as e:
        print("Receive server's public key error!")
        sys.exit()
    client_keys.update({username : client_key})


    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    while True:
        print("Waiting for operations from clients...")
        # Receive client's operation
        try:
            operation_size = sock.recv(4)
        except socket.error as e:
            print("Receive size of client operation error!")
            sys.exit()
        try:
            operation_msg = sock.recv(receiveint(operation_size))
        except socket.error as e:
            print("Receive client operation error!")
            sys.exit()
        operation = operation_msg.decode()


        # Perform based on user's command
        if operation == 'BM':
            # send confirmation message
            sendtoClient(sock, "Confirmation", "The server is ready to send broadcast message!")      

            try:
                msg_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of client's message error!")
                sys.exit()                                         
            try:
                msg = sock.recv(receiveint(msg_size))              # receive the message that needed to be broadcast
            except socket.error as e:
                print("Receive client message error!")              
                sys.exit()
        
            for addr in sockets.keys():                               # loop over all the client sockets
                if addr != address:                                   # send the message except the sender himself                  
                    sendtoClient(sockets.get(addr), "BM", msg)        # broadcast the message

                    # use "a+" rather than "r+" because we only need to 
                    # write data down on the file
                    mode_sender = 'a+' if os.path.exists(chat_history_path) else 'w+'          # set mode (only append (a+) or create the file (w+))
                    with open(chat_history_path, mode_sender) as f:             # record the chat message for the sender
                        f.write(f"At {datetime.now()}, {get_key(address, clients)} sends {get_key(addr, clients)} a BM message: {msg.decode()} \n")

                    receiver_chat_history = f"{get_key(addr, clients)}.txt"
                    mode_receiver = 'a+' if os.path.exists(receiver_chat_history) else 'w+' 
                    with open(receiver_chat_history, mode_receiver) as f:       # record the chat message for the receiver
                        f.write(f"At {datetime.now()}, {get_key(addr, clients)} receives a BM message from {get_key(address, clients)}: {msg.decode()} \n")
            
            # send confirmation to the client
            sendtoClient(sock, "Confirmation", "Public message sent!")                   
            continue

        elif operation == 'PM':
            # remove the current user
            other_clients = [item for item in clients.keys() if item != username]
                        
            online_clients = " ".join(other_clients)                                    # from the list of users 
            sendtoClient(sock, "LIST", online_clients)                                  # send the list as a string                                        

            try:
                target_client_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of client's user name length error!")
                sys.exit()                                         
            try:
                target_client = sock.recv(receiveint(target_client_size))               # receive the message that needed to be broadcast
            except socket.error as e:
                print("Receive target client's user name error!")              
                sys.exit()
            target_client = target_client.decode()

            target_key = client_keys.get(target_client)
            sendtoClient(sock, "key", target_key)                                       # send the public key of the target client


            try:
                msg_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of client's message error!")
                sys.exit()                                         
            try:
                msg_encrypted = sock.recv(receiveint(msg_size))                         # receive the message that needed to be privately sent
            except socket.error as e:
                print("Receive client message error!")              
                sys.exit()

            if target_client in clients.keys():
                target_client_sock = sockets.get(clients.get(target_client))            # find the specific socket
                sendtoClient(target_client_sock, "PM", msg_encrypted)

                sendtoClient(sock, "Confirmation", "Private message has been sent.")
            else:
                sendtoClient(sock, "Confirmation", "Target client is not online, failed to send the message!")
                continue                
            continue
            
        elif operation == 'CH': 
            if os.path.exists(chat_history_path): 
                # use "r+" rather than "a+" because we only need to 
                # read the date on the file
                with open(chat_history_path, "r+") as f:     # read chat history
                    data = f.readlines()                     # read as a list of strings
                    for i in data:    
                        # print(i)
                        sendtoClient(sock, "CH", i) 
            sendtoClient(sock, "CH", "Done") 
            continue

        elif operation == 'EX':
            sock.close()
            # Update the list of clients and the dictionary of sockets
            sockets.pop(address)
            print(f"{username} from {clients.pop(username)} has logged out!")
            return




if __name__ == '__main__':
    # TODO: Validate input arguments
   
    PORT = sys.argv[1]

    # A list to record clients
    clients = {}

    # create a dictionary to keep track of conn sockets
    sockets = {}

    # Create a dict to hold public keys from clients
    client_pub_keys = {}

    # TODO: create a socket in UDP or TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()
    
    # TODO: Bind the socket to address
    try:
        sock.bind(('', int(PORT)))
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()
    

    while True:
        print(f"Waiting for connections on port {PORT}...")

        # TODO: handle any incoming connection with TCP
        sock.listen()
        try:
            conn, addr = sock.accept()
        except socket.error as e:
            print("Nothing accepts.")
        print("Connection from client established")


        # TODO: initiate a thread for the connected user
        sockets.update({addr : conn})
        chat = threading.Thread(target=chatroom, args=(sockets, clients, addr, client_pub_keys), daemon=True)  # daemon = True will release memory after use
        chat.start()