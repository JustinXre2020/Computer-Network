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
from pg3lib import *

# Any global variables
BUFFER = 2048
openThread = True
key_from_server = ""
confirmation = ""
lists = ""
done_CH = False

# Create the client public key 
key = getPubKey()

# Convert from int to byte
def sendint(data):
    return int(data).to_bytes(4, byteorder='big', signed=True)


# Convert from byte to int
def receiveint(data):
    return int.from_bytes(data, byteorder='big', signed=True)


"""
The thread target fuction to handle any incoming message from the server.
Args:
    None
Returns:
    None
Hint: you can use the first character of the message to distinguish different types of message
"""

def accept_messages(): 
    while True:
        # should thread be closed
        if openThread == False:
            break

        # Try to receive messages type
        try:
            type_length = sock.recv(4)
        except socket.error as e:
            print("Receive size of operation error!", flush=True)
            sys.exit()
        try:
            types = sock.recv(receiveint(type_length))
        except socket.error as e:
            print("Receive size of operation error!", flush=True)
            sys.exit()
        types = types.decode()


        # Try to receive messages
        try:
            msg_length = sock.recv(4)
        except socket.error as e:
            print("Receive size of operation error!", flush=True)
            sys.exit()

        try:
            msg = sock.recv(receiveint(msg_length))
        except socket.error as e:
            print("Receive size of operation error!", flush=True)
            sys.exit()

        if types == 'PM' or types == 'BM':
            if types == "BM":
                print(f"\n**** Received a public message ****: {msg.decode()}", flush=True)
            else:
                msg_encrypt = decrypt(msg)
                print(f"\n**** Received a private message ****: {msg_encrypt.decode()}", flush=True)
            print("Please enter your operation (BM: Broadcast Messaging, PM: Private Messaging, CH: Chat History, EX: Exit):", flush=True)
        elif types == 'key':
            global key_from_server
            key_from_server = msg

        elif types == "LIST":
            global lists
            lists = msg.decode().split()        # a list of active clients
            print("Peers Online: \n")
            for i in lists:
                print(i + '\n')
        
        elif types == "CH":
            chat_history = msg.decode()
            if chat_history == "Done":
                global done_CH
                done_CH = True
            else:
                print(chat_history, flush=True)

        else:
            global confirmation
            confirmation = msg.decode()          # for Confirmation and CH types of message
        
    

if __name__ == '__main__': 
    # TODO: Validate input arguments
    
    hostname = sys.argv[1]
    PORT = sys.argv[2]
    username = sys.argv[3]

    # Find the host by its name and create host's address
    try:
        HOST = socket.gethostbyname(hostname)
    except socket.error as e:
        print(f"Unknown host {hostname}")
    sin = (HOST, int(PORT))


    # TODO: create a socket with UDP or TCP, and connect to the server
    # Create a socket
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()


    # Connect to the host from Command-line input
    try:
        sock.connect(sin)
    except socket.error as msg:
        print("Connection failed!")
        sys.exit()

    print("Connection to server established!")
    

    # TODO: initiate a thread for receiving message
    chat = threading.Thread(target=accept_messages, daemon=True)    # Daemon = True will release memory after use
    chat.start()

    # TODO: Send username to the server and login/register the user
    sock.send(sendint(len(username)))
    sock.send(username.encode())

    # wait until the client receives the key
    while key_from_server == "":           
        if key_from_server != "":
            break

    # Receive server's response
    # this happens in accept_messages() thread, confirmation will be changed
    # wait until receiving server's confirmation
    while confirmation == "":
        if confirmation != "":
            break

    # Perform login/register
    if confirmation == "Now please create your password!":
        # Prompt user to create a password
        print('Your username has been successfully created!')   
        
        # reinitialize confirmation
        confirmation = ""

        password = input("Now please create your password: \n")
        encrypted_password = encrypt(password.encode(), key_from_server)
        sock.send(sendint(len(encrypted_password)))
        sock.send(encrypted_password)                           # encrypt the password using server's pubKey

        # Receive and print server's reponse
        # this happens in accept_messages() thread, confirmation will be changed
        # wait until the client receives the confirmation
        while confirmation == "":           
            if confirmation != "":
                break
        print(confirmation, flush=True)

    else:
        while True:
            # reinitialize confirmation
            confirmation = ""

            # Type in password
            password = input('Now please type in your password!: \n')
            encrypted_password = encrypt(password.encode(), key_from_server)
            sock.send(sendint(len(encrypted_password)))
            sock.send(encrypted_password)

            # wait until the client receives the confirmation
            while confirmation == "":           
                if confirmation != "":
                    break

            # If it is the right message, that means log in successfully 
            if confirmation == "You successfully log into your account!":
                break
            else:
                # wrong password!!!
                print(confirmation) 

        # Inform client that the account has been logged in
        # Message printed in accept_messages() thread, confirmation will be changed
        print(confirmation, flush=True)


    # Send client's public key to server
    sock.send(sendint(len(key)))
    sock.send(key)


    # TODO: use a loop to handle the operations (i.e., BM, PM, EX)
    while True:  
        # Initialize some important values
        lists = ""    
        key_from_server = ""   
        confirmation = ""
        done_CH = False

        # Prompt client to send operations
        operation = input("Please enter your operation (BM: Broadcast Messaging, PM: Private Messaging, CH: Chat History, EX: Exit): \n")
        sock.send(sendint(len(operation)))
        sock.send(operation.encode())

        # Perform based on client's command
        if operation == 'BM':
            # wait until receiving server's confirmation
            while confirmation == "":
                if confirmation != "":
                    break
            
            if confirmation == "The server is ready to send broadcast message!":
                server_ready = confirmation                                                                      
                message_broadcasting = input("Enter the public message:  ")   
                sock.send(sendint(len(message_broadcasting)))               
                sock.send(message_broadcasting.encode())                    # send the message to the server
    
                # wait until receiving server's new confirmation
                while confirmation == server_ready:
                    if confirmation != server_ready:
                        break
                print(confirmation)
            else:
                print("Cannot connect with the server.")
            continue 
                                                                
        elif operation == 'PM':
            # receive all online clients
            # this takes place in accept_messages() thread
            # wait until the server sends all online clients
            while lists == "":           
                if lists != "":
                    break
            
            while True:
                target_client = input("Peer to message:  ")         # choose which client we want to send private message to
                if target_client in lists:
                    break                                           # If the target client not in lists, back to input
                print("Invalid client!")

            sock.send(sendint(len(target_client)))
            sock.send(target_client.encode())

            # wait until the client receives the key
            while key_from_server == "":           
                if key_from_server != "":
                    break
            print("Your private message will be encrypted!")

            msg = input("Enter the private mesage: ")           # the content of private message
            encrypt_msg = encrypt(msg.encode(), key_from_server)
            sock.send(sendint(len(encrypt_msg)))
            sock.send(encrypt_msg)

            # wait until receiving server's confirmation
            while confirmation == "":
                if confirmation != "":
                    break
            print(confirmation)

            continue

        elif operation == 'CH':
            # wait until the thread prints out chat history
            while done_CH == False:
                if done_CH == True:
                    break
            continue
            
        elif operation == 'EX':
            openThread = False
            chat.join()
            sock.close()
            print("The session has ended")
            break
        else:
            print("Invalid command!")