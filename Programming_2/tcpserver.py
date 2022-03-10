# IS496: Computer Networks (Spring 2022)
# Programming Assignment 2 - Starter Code
# Name and Netid of each member:

# Member 1: Justin Xiao - xulongx2
# Member 2: Jerry Guo - zemingg2
# Member 3: Tiancheng Shi - ts15 

# Note: 
# This starter code is optional. Feel free to develop your own solution to Part 1. 
# The finished code for Part 1 can also be used for Part 2 of this assignment. 


# Import any necessary libraries below
import socket
import sys
import os
import subprocess
from time import time


############## Beginning of Part 1 ##############


# Convert from int to byte
def sendint(data):
    return int(data).to_bytes(4, byteorder='big', signed=True)

# Convert from byte to int
def receiveint(data):
    return int.from_bytes(data, byteorder='big', signed=True)


def part1 ():
    print("********** PART 1 **********")
    # TODO: fill in the IP address of the host and the port number
    HOST = socket.gethostbyname("student00.ischool.illinois.edu")
    PORT = 41008
    sin = (HOST, PORT)

    # TODO: create a datagram socket for TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()


    # TODO: Bind the socket to address
    try:
        sock.bind(sin)
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()
    opt = 1
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, opt)

    print("Waiting ...")

    # TODO: start listening 

    sock.listen()
    

    # TODO: accept the connection and record the address of the client socket


    try:
        conn, addr = sock.accept()
    except socket.error as e:
        print("Nothing accepts.")


    # TODO: receive message from the client 

    # Receive size of message
    try:
        data = conn.recv(4)
    except socket.error as msg:
        print("Receive error")
        sys.exit()
    size = receiveint(data)

    # Receive the message
    try:
        msg = conn.recv(size)
    except socket.error as e:
        print("Receive error!")
        sys.exit()


    # TODO: print the message to the screen


    print(f"Message from client: {msg.decode()}")


    # TODO: send an acknowledgement (e.g., interger of 1) to the client


    try:
        conn.send(sendint(1))
    except socket.error as e:
        print("Send error!")
        sys.exit()


    # TODO: close the socket


    try:
        conn.close()
    except socket.error as msg:
        print("Socket close failed!")
        sys.exit()


############## End of Part 1 ##############




############## Beginning of Part 2 ##############

# main function for Part 2
def part2 ():
    print("********** PART 2 **********")  

    PORT = sys.argv[1]

    # Create a socket and start to bind 
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as msg:
        print('Failed to create socket.')
        sys.exit()

    try:
        sock.bind(("", int(PORT)))
    except socket.error as e:
        print('Failed to bind socket.')
        sys.exit()

    print(f"Waiting for connections on port {PORT}...")


    # Listen for any connections
    sock.listen()
    try:
        conn, addr = sock.accept()
    except socket.error as e:
        print("Nothing accepts.")


    print("Connection from client established")


    while True:
        print("Waiting for operations from clients...")

        # Receive client's request
        try:
            request_size = conn.recv(4)
        except socket.error as e:
            print("Receive size of operation error!")
            sys.exit()

        try:
            request = conn.recv(receiveint(request_size))
        except socket.error as e:
            print("Receive operation error!")
            sys.exit()
        operation = request.decode()


        #  Perform operations based on client's request
        if (operation[:2] == 'DN'):
            # Receive the name of file
            try:
                length_file = conn.recv(4)
            except socket.error as e:
                print("Receive length of filename error!")
                sys.exit()
            length = receiveint(length_file)

            try:
                file = conn.recv(length)
            except socket.error as e:
                print("Receive filename error!")
                sys.exit()
            filename = file.decode()


            # Check to see if the file exists in its local directory
            # If the file exists, server returns the size of the file to the client as a 32-bit integer
            # If the file does not exist, server will return a negative confirmation
            to_client = -1
            if (os.path.exists(filename)):
                to_client = os.path.getsize(filename)
                conn.send(sendint(to_client))                # send size of file         
                with open(filename, 'rb') as f:              # read file content
                    bytes_read = f.read(2048)                # read the bytes from the file
                    if not bytes_read:
                        break                                # file transmitting is done
                    conn.sendall(bytes_read)                 # send contents of the file
            else:
                conn.send(sendint(to_client)) 
                continue                                     # return to "wait for operation from client" state

        elif (operation[:2] == 'UP'):
            # Receive the name of file
            try:
                length_file = conn.recv(4)
            except socket.error as e:
                print("Receive length of filename error!")
                sys.exit()
            length = receiveint(length_file)

            try:
                file = conn.recv(length)
            except socket.error as e:
                print("Receive filename error!")
                sys.exit()
            filename = file.decode()

            msg = "The server is ready to receive the file"
            conn.send(sendint(len(msg)))
            conn.send(msg.encode())


            # Receives the file size
            try:
                size_file = conn.recv(4)
            except socket.error as e:
                print("Receive length of filename error!")
                sys.exit()
            size = receiveint(size_file)

            # Receives the file and writes it down and start counting
            start = time()
            with open(filename, "w") as f:
                data = conn.recv(size)
                if not data:    
                    break
                f.write(data.decode())

            # End the counting     
            end = time()

            # Send the time
            try:
                conn.send(sendint(len(str(end - start))))
                conn.send(str(end - start).encode())
            except socket.error:
                print("Send count time error!")
                sys.exit()
            
        elif ((operation[:2] == 'RM') & (operation[2:5] != 'DIR')):
            # Receive the name of file
            try:
                length_file = conn.recv(4)
            except socket.error as e:
                print("Receive length of filename error!")
                sys.exit()
            length = receiveint(length_file)

            try:
                file = conn.recv(length)
            except socket.error as e:
                print("Receive filename error!")
                sys.exit()
            filename = file.decode()


            # Check to see if the file exists in its local directory
            # If the file exists, server deletes the file and inform the client based on the result of deleting
            # If the file does not exist, server will return a negative confirmation and return to "wait for operation from client" state
            to_client = -1
            if (os.path.exists(filename)):
                to_client = 1
                conn.send(sendint(to_client))                # send size of file   
                try:
                    size = conn.recv(4)                      # Receive size of response
                except socket.error as e:
                    print("Receive size error!")
                    sys.exit()
                size_res = receiveint(size)      
                try:
                    res = conn.recv(size_res)
                except socket.error as e:
                    print("Receive client response error!")
                    sys.exit()
                response = res.decode()
                if response == "Yes":
                    try:
                        os.remove(filename)                  # Try deleting the file
                    except OSError as e:
                        word = "There is something wrong in deleting the file"
                        conn.send(sendint(len(word)))
                        conn.send(word.encode())             # Send failure message
                        continue
                    word = "The file has been deleted!"
                    conn.send(sendint(len(word)))                 
                    conn.send(word.encode())                 # Send success message
                    continue                                 # return to "wait for operation from client" state
                elif response == "No":
                    continue                                 # return to "wait for operation from client" state
            else:
                conn.send(sendint(to_client)) 
                continue                                     # return to "wait for operation from client" state
        
        elif (operation == 'LS'):
            # Get the list of all files and directories 
            # in the root directory
            directory = subprocess.check_output('ls -l', shell=True)
            size = len(directory)

            # Send the size of directory
            try:
                conn.send(sendint(size))
            except socket.error as e:
                print("Send size error!")

            # Send the list of directory
            try:
                conn.send(directory)
            except socket.error as e:
                print("Send directory error!")
                sys.exit()

            # return to "wait for operation from client" state
            continue

        elif (operation[:5] == 'MKDIR'):
            # Receive the name of directory
            try:
                length_dir = conn.recv(4)
            except socket.error as e:
                print("Receive length of filename error!")
                sys.exit()

            try:
                dir = conn.recv(receiveint(length_dir))
            except socket.error as e:
                print("Receive filename error!")
                sys.exit()
            directory = dir.decode()

            new_directory = os.path.join(os.getcwd(), directory)
            if os.path.isdir(new_directory):
                conn.send(sendint(-2))      # send negative confirmation
                continue
            else:
                try:
                    os.mkdir(new_directory)
                except OSError as e:
                    conn.send(sendint(-1))  # failed to create the directory
                    continue
                conn.send(sendint(1))       # the directory is successfully created
                continue


        elif (operation[:5] == 'RMDIR'):
            # Receive the name of directory
            try:
                length_dir = conn.recv(4)
            except socket.error as e:
                print("Receive length of filename error!")
                sys.exit()

            try:
                dir = conn.recv(receiveint(length_dir))
            except socket.error as e:
                print("Receive filename error!")
                sys.exit()
            directory = dir.decode()


            # Generate confirmation numbers
            target_directory = os.path.join(os.getcwd(), directory)
            if os.path.isdir(target_directory):
                if len(os.listdir(target_directory)) == 0:
                    conn.send(sendint(1))
                else:
                    conn.send(sendint(-2))
            else:
                conn.send(sendint(-1))


            # Receive client's response
            try:
                res_size = conn.recv(4)
            except socket.error as e:
                print("Receive size of client's response error!")
                sys.exit()

            try:
                res = conn.recv(receiveint(res_size))
            except socket.error as e:
                print("Receive client's response error!")
                sys.exit()
            response = res.decode()


            # Perform operations based on client's response
            if response == "Yes":
                try:
                    os.rmdir(target_directory)
                except OSError as e:
                    conn.send(sendint(-1))
                    continue
                conn.send(sendint(1))
                continue
            else:
                continue

        elif (operation[:2] == 'CD'):
            # Receive the name of directory
            try:
                length_dir = conn.recv(4)
            except socket.error as e:
                print("Receive length of filename error!")
                sys.exit()
            length = receiveint(length_dir)

            try:
                dir = conn.recv(length)
            except socket.error as e:
                print("Receive filename error!")
                sys.exit()
            directory = dir.decode()


            # Generate confirmation numbers
            target_directory = os.path.join(os.getcwd(), directory)
            if os.path.isdir(target_directory):
                try:
                    os.chdir(target_directory)
                except OSError as e:
                    conn.send(sendint(-1))
                    continue
                conn.send(sendint(1))
                continue
            else:
                conn.send(sendint(-2))
                continue

        elif (operation == 'QUIT'):
            conn.close()
            print(f"Waiting for connections on port {PORT}")

            # Listen for any connections
            try:
                conn, addr = sock.accept()
            except socket.error as e:
                print("Nothing accepts.")

            print("Connection from client established.")
            continue


############## End of Part 2 ##############



if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input. 
    # Otherwise, it will go with function part2() to handle the command line input 
    # as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()




