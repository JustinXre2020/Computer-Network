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
import sys, os, struct

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
def chatroom (args):
    print()
    # Task1: login/register the user
   

    # Task2: use a loop to handle the operations (i.e., BM, PM, EX)
    





if __name__ == '__main__':
    # TODO: Validate input arguments
   
    PORT = sys.argv[1]

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
        

        # Receive client's username
        try:
            username_size = conn.recv(4)
        except socket.error as e:
            print("Receive size of username error!")
            sys.exit()


        try:
            username_msg = conn.recv(receiveint(username_size))
        except socket.error as e:
            print("Receive username error!")
            sys.exit()
        username = username_msg.decode()
       





