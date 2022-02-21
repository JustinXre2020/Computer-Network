# IS496: Computer Networks (Spring 2022)
# Programming Assignment 1 -  Starter Code 
# Name and Netid of each member:

# Member 1: Justin Xiao
# Member 2: Jerry Guo
# Member 3: Tiancheng Shi


# Note: 
# This starter code is optional. Feel free to develop your own solution to Part 1. 
# The finished code for Part 1 can also be used for Part 2 of this assignment. 



# Import any necessary libraries below
import socket
import sys, struct
from pg1lib import *


############## Beginning of Part 1 ##############
# TODO: define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def part1 ():
    print("********** PART 1 **********")
    print("Welcome to UDP Server.")

    # TODO: fill in the IP address of the host and the port number
    HOST = socket.gethostbyname("student01.ischool.illinois.edu")
    PORT = 41008
    sin = (HOST, PORT)

    # TODO: create a datagram socket

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()


    # TODO: Bind the socket to address

    try:
        sock.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    print("Waiting ...")

    # TODO: receive message from the client and record the address of the client socket

    try:
        msg, addr = sock.recvfrom(BUFFER)
    except socket.error as e:
        print("Receive error!")
        sys.exit()


    # TODO: convert the message from byte to string and print it to the screen

    print(msg.decode())    
    print(f"Address is {addr}")


    # TODO: 
    # 1. convert the acknowledgement (e.g., interger of 1) from host byte order to network byte order
    # 2. send the converted acknowledgement to the client

    to_client = socket.htonl(1)
    try:
        sock.sendto(to_client.to_bytes(4, byteorder='big'), addr)
    except socket.error as e:
        print("Send error!")
        sys.exit()

    # TODO: close the socket

    try:
        sock.close()
    except socket.error as msg:
        print("Socket close failed!")
        sys.exit()




############## End of Part 1 ##############




############## Beginning of Part 2 ##############
# Note: any functions/variables for Part 2 will go here 

def part2 ():
    print("********** PART 2 **********")
    print("Welcome to UDP Server.")
    
    PORT = sys.argv[1]

    # Create a socket and start to bind 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()

    try:
        sock.bind(("", int(PORT)))
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    print("Waiting ...")


    # Create the public key and received the client's public key
    key = getPubKey()

    try:
        msg, addr = sock.recvfrom(BUFFER)
    except socket.error as e:
        print("Receive error!")
        sys.exit()
   

    # Send server's encrypted public key to client 
    to_sent = encrypt(key, msg)
    try:
        sock.sendto(to_sent, addr)
    except socket.error as e:
        print("Send error!")
        sys.exit()


    # Received and decrypted the encrypted message from client
    try:
        encrp_msg, addr = sock.recvfrom(BUFFER)
    except socket.error as e:
        print("Receive encrypt msg error!")
        sys.exit()
    msg_client = decrypt(encrp_msg)
    print("Received message: ", msg_client)


    # Received checksum(not encrypted) from the server
    try:
        checksum_, addr = sock.recvfrom(BUFFER)
    except socket.error as e:
        print("Receive checksum error!")
        sys.exit()


    # Receive and Calculate checksums 
    checksum_int = int.from_bytes(checksum_, "big")
    checksum_client = socket.ntohl(checksum_int)
    print("Received checksum: ", checksum_client)

    checksum_server = checksum(msg_client)
    print("Server's checksum: ", checksum_server)

    print("The server has successfully received the message!")

    # Compare the 2 checksums
    if (checksum_client == checksum_server):
        confirm1 = socket.htonl(1)
        try:
            sock.sendto(confirm1.to_bytes(4, byteorder='big'), addr)
        except socket.error as e:
            print("Send checksum matches error!")
            sys.exit()
    else:
        confirm0 = socket.htonl(0)
        try:
            sock.sendto(confirm0.to_bytes(4, byteorder='big'), addr)
        except socket.error as e:
            print("Send checksum matches error!")
            sys.exit()

    # Shuts down
    try:
        sock.close()
    except socket.error as msg:
        print("Socket close failed!")
        sys.exit()

    


############## End of Part 2 ##############

if __name__ == '__main__':
# Your program will go with function part1() if there is no command line input. 
# Otherwise, it will go with function part2() to handle the command line input 
# as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()




