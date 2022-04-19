# IS496: Computer Networks (Spring 2022)
# Programming Assignment 1 -  Starter Code
# Name and Netid of each member:

# Member 1: Justin Xiao, xulongx2
# Member 2: Jerry Guo, zemingg2
# Member 3: Tiancheng Shi, ts15


# Note: 
# This starter code is optional. Feel free to develop your own solution to Part 1. 
# The finished code for Part 1 can also be used for Part 2 of this assignment. 



# Import any necessary libraries below
import socket
import sys, struct, time
from pg1lib import *


############## Beginning of Part 1 ##############
# TODO: define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


def part1 ():
    print("********** PART 1 **********")
    # TODO: fill in the hostname and port number 
    hostname = "student01.ischool.illinois.edu"
    PORT = 41008

    # A dummy message (in bytes) to test the code
    message = b"Hello World"

    # TODO: convert the host name to the corresponding IP address
    try:
        HOST = socket.gethostbyname(hostname)
    except socket.error as e:
        print(f"Unknown host {hostname}")
    sin = (HOST, PORT)


    # TODO: create a datagram socket

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()


    # TODO: convert the message from string to byte and send it to the server
    try:
        sock.sendto(message, sin)
    except socket.error as msg:
        print("Client send error!")
        sys.exit()


    # TODO: 
    # 1. receive the acknowledgement from the server 
    # 2. convert it from network byte order to host byte order 

    try:
        data, addr = sock.recvfrom(BUFFER)
    except socket.error as msg:
        print("recvfrom() error")
        sys.exit()
    data_int = int.from_bytes(data, "big")
    data_host = socket.ntohl(data_int)

    # TODO: print the acknowledgement to the screen

    print(f"Client received {len(data)} bytes from {addr}")
    print(f"Result: {data_host}\n")    


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
    hostname = sys.argv[1]
    PORT = sys.argv[2]
    message = sys.argv[3]

    # Find the host by its name and create host's address
    try:
        HOST = socket.gethostbyname(hostname)
    except socket.error as e:
        print(f"Unknown host {hostname}")
    sin = (HOST, int(PORT))


    # Create a socket and client's public key
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()

    key = getPubKey()
   

    # send the public key to the server
    try:
        sock.sendto(key, sin)
    except socket.error as msg:
        print("Client send error!")
        sys.exit()
    

    # Receive encrypted message from the server and decrypted it
    try:
        data, addr = sock.recvfrom(BUFFER)
    except socket.error as e:
        print("Receive error!!")
        sys.exit()
    key_server = decrypt(data)


    # Convert the message from string to byte, and calculate its checksum
    # Then encrypted the byte using server's public key
    msg_byte = message.encode()
    sum = checksum(msg_byte)
    print("Checksum is: ", sum)

    to_server = encrypt(msg_byte, key_server)


    # start the Round-time counting
    start_time = time.time()


    # send the byte message to server
    try:
        sock.sendto(to_server, sin)
    except socket.error as msg:
        print("Client send message error!")
        sys.exit()

    # send the checksum to server
    sum_tosent = socket.htonl(sum)
    try:
        sock.sendto(sum_tosent.to_bytes(4, byteorder='big'), sin)
    except socket.error as msg:
        print("Client send checksum error!")
        sys.exit()
        
    print("The server has successfully received the message!")


    # Receive a confirmation number from the server
    try:
        confirm, addr = sock.recvfrom(BUFFER)
    except socket.error as e:
        print("Confirm error!!")
        sys.exit()
    data_int = int.from_bytes(confirm, "big")
    confirm_num = socket.ntohl(data_int)
    if (confirm_num == 1):
        print("The two checksums are the same!")
    else:
        print("The two checksums are different...")


    # end the counting
    end_time = time.time()
    print("RTT is: ", (end_time - start_time) * 1000000, " microseconds")


    # shuts down
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

