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

# Any global variables
BUFFER = 2048


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
def chatroom (args, clients):
    # Task1: login/register the user

    # Get the socket
    sock = args.get("sock")

    # Set filename
    userinfo = "userinfo.txt"

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


    with open(userinfo, "w") as f:
        # Get the data from the file
        lines = f.readlines()                   # Example lines: ["Ann, 12345\n", "John, 54231\n"]
        nested_list = [line.strip().split(',') for line in lines]
        data_list = [data for list in nested_list for data in list]

        # See if the username is in the file
        if len(data_list == 0) or username not in data_list:
            f.write(username + ',')             # Write down the username
            sock.send(sendint(1))               # Inform user to create a password

            # Receive client's password
            try:
                password_size = sock.recv(4)
            except socket.error as e:
                print("Receive size of username error!")
                sys.exit()
            try:
                password_msg = sock.recv(receiveint(password_size))
            except socket.error as e:
                print("Receive username error!")
                sys.exit()
            password = password_msg.decode()

            f.write(password + '\n')            # write down the password

            # Inform client that the account has been created!
            msg = "Your account has been successfully created!"
            sock.send(sendint(len(msg)))
            sock.send(msg.encode())
        else:
            # Inform user to type in the password
            sock.send(sendint(-1))

            # If the password is wrong, go into the loop until client types in the correct password
            while True:
                # Receive client's password
                try:
                    password_size = sock.recv(4)
                except socket.error as e:
                    print("Receive size of username error!")
                    sys.exit()
                try:
                    password_msg = sock.recv(receiveint(password_size))
                except socket.error as e:
                    print("Receive username error!")
                    sys.exit()
                password = password_msg.decode()

                # Check the password, if not in the file, inform it to the user
                if password not in data_list:
                    sock.send(sendint(-2))
                else:
                    break

            # Inform client that the account has been logged in
            sock.send(sendint(2))

    # Add the user to the list of clients
    clients.append(username)


    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    
    # Using while loop to make sure that we can go back to "prompt user for operation" state as we want
    while True:
        print("Waiting for operations from clients...")
        # Receive client's operation
        try:
            operation_size = sock.recv(4)
        except socket.error as e:
            print("Receive size of username error!")
            sys.exit()
        try:
            operation_msg = sock.recv(receiveint(operation_size))
        except socket.error as e:
            print("Receive username error!")
            sys.exit()
        operation = operation_msg.decode()


        # Perform based on user's command
        if operation == 'BM':
            
        elif operation == "PM":
        
        elif operation == 'EX':
            sock.close()
            # Update the list of clients
            clients.remove(username)
            return




if __name__ == '__main__':
    # TODO: Validate input arguments
   
    PORT = sys.argv[1]
    # A list to record clients
    clients = []

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

        # TODO: handle any incoming connection with UDP or TCP
        sock.listen()
        try:
            conn, addr = sock.accept()
        except socket.error as e:
            print("Nothing accepts.")
        print("Connection from client established")


        # TODO: initiate a thread for the connected user
        args = {"sock" : conn}
        chat = threading.Thread(target=chatroom, args=(args, clients), daemon=True)  # Daemon = True will release memory after use
        chat.start()
        
        
                
       





