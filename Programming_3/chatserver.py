# IS496: Computer Networks (Spring 2022)
# Programming Assignment 3 - Starter Code
# Name and Netid of each member:
# Member 1: 
# Member 2: 
# Member 3: 


# Note: 
# This starter code is optional. Feel free to develop your own solution. 

# Import any necessary libraries below
import socket, threading, sys, os
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


"""
The thread target fuction to handle the requests by a user after a socket connection is established.
Args:
    args:  any arguments to be passed to the thread
Returns:
    None
"""
def chatroom (sockets, clients, address):
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

    userinfo_path = os.path.join(os.getcwd(), user_info)        # generate userinfo path
    mode = 'r+' if os.path.exists(userinfo_path) else 'w+'      # set mode (only read/write (r+) or create the file (w+))
                                                                # based on the existance of userinfo     

    with open(userinfo_path, mode) as f:                        # create user information file to store username and password
        # Get the data from the file
        lines = f.readlines()                   # Example lines: ["Ann, 12345\n", "John, 54231\n"]
        nested_list = [line.strip().split(',') for line in lines]
        data_list = [data for list in nested_list for data in list]

        # See if the username is in the file
        if len(data_list == 0) or username not in data_list:        # Registration process
            f.write(username + ',')             # Write down the username
            sock.send(sendint(1))               # Inform user to create a password
            sock.send(key)                      # Send server's public key to client

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
            password = decrypt(password_msg)    

            f.write(password + '\n')            # write down the password

            # Inform client that the account has been created!
            msg = "Your account has been successfully created!"
            sock.send(sendint(len(msg)))
            sock.send(msg.encode())

            # generate userinfo path
            chat_history_path = os.path.join(os.getcwd(), chat_history)        
            # create chat history file for each user
            with open(chat_history_path, mode) as f:                    
                pass   
        else:
            # Inform user to type in the password
            sock.send(sendint(-1))

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
                password = decrypt(password_msg)       

                # Check the password, if not in the file, inform it to the user
                if password not in data_list:
                    sock.send(sendint(-2))
                else:
                    break

            # Inform client that the account has been logged in
            sock.send(sendint(2))

    # Add the user to the list of clients
    clients.update({username : address})

    # Receive client's public key
    try:
        client_key = sock.recv(BUFFER)
    except socket.error as e:
        print("Receive server's public key error!")
        sys.exit()


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
            sock.send(sendint(1))                                  #send confirmation message
            try:
                msg_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of client's message error!")
                sys.exit()                                         
            try:
                msg = sock.recv(receiveint(msg_size))              #receive the message that needed to be broadcast
            except socket.error as e:
                print("Receive client message error!")              
                sys.exit()
            msg = msg.decode()
            sock.send(sendint(2))
            for i in sockets.keys():                                #loop over all the clients active
                if i != address:                                    #except the sender client itself
                    sockets.get(i).send(sendint(len(msg)))
                    sockets.get(i).send(msg.encode())               #broadcast the message
            continue



        elif operation == 'PM':
            online_clients = " ".join(clients.keys())
            sock.send(sendint(len(online_clients)))
            sock.send(online_clients.encode())
            try:
                target_client_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of client's user name length error!")
                sys.exit()                                         
            try:
                target_client = sock.recv(receiveint(target_client_size))              #receive the message that needed to be broadcast
            except socket.error as e:
                print("Receive target client's user name error!")              
                sys.exit()
            target_client = target_client.decode()
            try:
                msg_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of client's message error!")
                sys.exit()                                         
            try:
                msg = sock.recv(receiveint(msg_size))              #receive the message that needed to be privately sent
            except socket.error as e:
                print("Receive client message error!")              
                sys.exit()
            msg = msg.decode()

            if target_client in clients.keys():
                sockets.get(clients.get(target_client)).send(sendint(len(msg)))
                sockets.get(clients.get(target_client)).send(msg.encode())
                sock.send(sendint(1))
            else:
                sock.send(sendint(0))
                
            continue
            





        elif operation == 'CH':  
            with open(chat_history_path, 'rb') as f:     # read file content
                while True:
                    bytes_read = f.read(BUFFER)          # read the bytes from the file
                    if not bytes_read:
                        break                            # file transmitting is done
                    sock.sendall(bytes_read)  
            continue
        elif operation == 'EX':
            sock.close()
            # Update the list of clients and the dictionary of sockets
            print(f"{username} from {sockets.pop(address)} has logged out!")
            clients.remove(username)
            return




if __name__ == '__main__':
    # TODO: Validate input arguments
   
    PORT = sys.argv[1]
    # A list to record clients
    clients = {}
    # create a dictionary to keep track of conn sockets
    sockets = {}

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
        chat = threading.Thread(target=chatroom, args=(sockets, clients, addr), daemon=True)  # daemon = True will release memory after use
        chat.start()