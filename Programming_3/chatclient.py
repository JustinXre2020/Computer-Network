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
BUFFER =  2048

# Create the server public key 
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

    # Try to receive messages
    try:
        msg = sock.recv(BUFFER)
    except socket.error as e:
        print("Receive size of operation error!")
        sys.exit()
    
    # Check if the message is an int 
    try:
        message = receiveint(msg)
        print(f"Received a message: {message}")
    except TypeError as e:
        print(f"Received a message: {msg.decode()}")




if __name__ == '__main__': 
    # TODO: Validate input arguments
    
    hostname = sys.argv[1]
    PORT = sys.argv[2]

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

    print("Connection to server established")
    
    

    # TODO: Send username to the server and login/register the user
    username = input("Please enter your username: ")
    sock.send(sendint(len(username)))
    sock.send(username.encode())

    # Receive server's response
    try:
        response_binary = sock.recv(4)
    except socket.error as e:
        print("Receive size of response error!")
        sys.exit()
    response = receiveint(response_binary)

    # Receive server's public key
    try:
        server_key = sock.recv(BUFFER)
    except socket.error as e:
        print("Receive server's public key error!")
        sys.exit()

    # Perform login/register
    if response == 1:
        print('Your username has been successfully created!')   # Prompt user to create a password
        password = input("Now please create your password: ")
        sock.send(sendint(len(password)))
        sock.send(encrypt(server_key, password))                # encrypt the password using server's pubKey

        # Receive and print server's reponse
        try:
            reponse_size = sock.recv(4)
        except socket.error as e:
            print("Receive size of server response error!")
            sys.exit()
        try:
            reponse_msg = sock.recv(receiveint(reponse_size))
        except socket.error as e:
            print("Receive server response error!")
            sys.exit()
        print(reponse_msg.decode())
    else:
        while True:
            # Type in password
            password = input("Please type in your password: ")
            sock.send(sendint(len(password)))
            sock.send(encrypt(server_key, password))

            # Receive server's response on password
            try:
                password_response = sock.recv(4)
            except socket.error as e:
                print("Receive password response error!")
                sys.exit()
            pas_response = receiveint(password_response)

            # If it is 2, that means log in successfully 
            if pas_response == 2:
                break
            else:
                print("Wrong password!")

            # Inform client that the account has been logged in
        print("You successfully log into your account!")

     # Send client's public key to server
    sock.send(key)


    # TODO: initiate a thread for receiving message
    chat = threading.Thread(target=accept_messages, daemon=True)    # Daemon = True will release memory after use
    chat.start()


    # TODO: use a loop to handle the operations (i.e., BM, PM, EX)
    while True:         
        # Prompt client to send operations
        operation = input("Please enter your operation (BM: Broadcast Messaging, PM: Private Messaging, CH: Chat History, EX: Exit): ")
        sock.send(sendint(len(operation)))
        sock.send(operation.encode())

        # Perform based on client's command
        if operation == 'BM':
            try:
                bm_ack = sock.recv(4)
            except socket.error as e:
                print("Receive message broadcasting response error!")
                sys.exit()
            bm_response = receiveint(bm_ack)

            if bm_response == 1:                                            #receive an acknowledgement from the server                             
                message_broadcasting = input("Enter the public message:")   
                sock.send(sendint(len(message_broadcasting)))               
                sock.send(message_broadcasting.encode())                    #send the message to the server
                try:
                    server_receive_ack = sock.recv(4)
                except socket.error as e:
                    print("Server receiving broadcasting message error!")
                    sys.exit()
                server_receiving_msg_response = receiveint(server_receive_ack)  
                if server_receiving_msg_response == 2:                       #verify whether the server has received the message
                    print("Public message sent.")
                    continue
            else:
                print("Cannot connect with the server.")
                continue



        elif operation == 'PM':
            try:
                client_number = sock.recv(4)
            except socket.error as e:
                print("Receive size of client number error!")
                sys.exit()                                         
            try:
                client = sock.recv(receiveint(client_number))              #receive the message that needed to be broadcast
            except socket.error as e:
                print("Receive client message error!")              
                sys.exit()
            client = client.decode().split()
            print("Peers Online: \n")
            for i in client:
                print(i+'\n')
            
            target_client = input("Peer to message: ")          #choose which client we want to send private message to
            msg = input("Enter the private mesage: ")           #the content of private message

            sock.send(sendint(len(target_client)))
            sock.send(target_client.encode())

            sock.send(sendint(len(msg)))
            sock.send(msg.encode())

            try:
                pm_ack = sock.recv(4)
            except socket.error as e:
                print("Receive message private messaging response error!")
                sys.exit()
            pm_response = receiveint(pm_ack)

            if pm_response == 1:
                print("Private message has been sent.")
            elif pm_response == 0:
                print("Target client is not online, failed to send the message.")


        
            


        elif operation == 'EX':
            sock.close()
            print("The session has ended")
            break
        elif operation == 'CH':
            file_path = os.path.join(os.getcwd(), f"{username}.txt")
            with open(file_path, "w") as f:            # write data to the file
                while True:
                    data = sock.recv(BUFFER)
                    if not data:
                        break
                    f.write(data.decode())
            
            with open(file_path, 'r') as f:             # get and print data from the file
                lines = f.readlines()                   # Example lines: ["Ann, 12345\n", "John, 54231\n"]
                for line in lines:
                    print(line)
            continue
        else:
            print("Invalid command!")