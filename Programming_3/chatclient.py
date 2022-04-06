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

# Any global variables
BUFFER =  2048


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

    # Perform login/register
    if response == 1:
        # Prompt user to create a password
        print('Your username has been successfully created!')
        password = input("Now please create your password: ")
        sock.send(sendint(len(password)))
        sock.send(password.encode())

        # Receive server's reponse
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
            sock.send(password.encode())

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

    # TODO: initiate a thread for receiving message
    
    chat = threading.Thread(target=accept_messages, daemon=True)    # Daemon = True will release memory after use
    chat.start()

    # TODO: use a loop to handle the operations (i.e., BM, PM, EX)

    # Using while loop to make sure that we can go back to "prompt user for operation" state as we want
    while True:
        # Prompt client to send operations
        operation = input("Please enter your operation (BM: Broadcast Messaging, PM: Private Messaging, EX: Exit): ")
        sock.send(sendint(len(operation)))
        sock.send(operation.encode())

        # Perform based on client's command
        if operation == 'BM':
            
        elif operation == "PM":
            
        elif operation == 'EX':
            sock.close()
            print("The session has ended")
            break
        else:
            print("Invalid command!")