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
from time import time



############## Beginning of Part 1 ##############


# Convert from int to byte
def sendint(data):
    return int(data).to_bytes(4, byteorder='big', signed=True)

# Convert from byte to int
def receiveint(data):
    return int.from_bytes(data, byteorder='big', signed=True)



def part1 ():
    # TODO: fill in the hostname and port number
    hostname = "student00.ischool.illinois.edu"
    PORT = 41008

    # A dummy message (in bytes) to test the code
    message = "Hello World"

    # TODO: convert the host name to the corresponding IP address
    HOST = socket.gethostbyname(hostname)
    sin = (HOST, PORT)


    # TODO: create a datagram socket for TCP
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as e:
        print('Failed to create socket.')
        sys.exit()


    # TODO: connect to the server

    try:
        sock.connect(sin)
    except socket.error as e:
        print("Connecting to server failed!")
        sys.exit()


    # TODO: send the message to the server

    # Send the size of message first
    try:
        sock.send(sendint(len(message)))
    except socket.error as msg:
        print("Client send error!")
        sys.exit()

    # Then send the message in bytes
    try:
        sock.send(message.encode())
    except socket.error as msg:
        print("Client send error!")
        sys.exit()


    # TODO: receive the acknowledgement from the server


    try:
        data = sock.recv(4)
    except socket.error as msg:
        print("Receive error")
        sys.exit()


    # TODO: print the acknowledgement to the screen


    print(f"Acknowledgement: {receiveint(data)}\n") 


    # TODO: close the socket


    try:
        sock.close()
    except socket.error as msg:
        print("Socket close failed!")
        sys.exit()


############## End of Part 1 ##############




############## Beginning of Part 2 ##############


# main function for Part 2
def part2 ():
    print("********** PART 2 **********")


    hostname = sys.argv[1]
    PORT = sys.argv[2]


    # Find the host by its name and create host's address
    try:
        HOST = socket.gethostbyname(hostname)
    except socket.error as e:
        print(f"Unknown host {hostname}")
    sin = (HOST, int(PORT))


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


    # Using while loop to make sure that we can go back to "prompt user for operation" state as we want
    while True:
        # User input to perform operations
        operation = input("Please enter your operation: ")
        sock.send(sendint(len(operation)))
        sock.send(operation.encode())

        if (operation[:2] == 'DN'):
            # Send length of file
            filename = operation[2:].strip()
            try:
                sock.send(sendint(len(filename)))
            except socket.error as msg:
                print("Send length of file error!")
                sys.exit()

            # Send filename
            try:
                sock.send(filename.encode())
            except socket.error as msg:
                print("Send filename error!")
                sys.exit()


            # Receive the 32-bit file size from server if file exists
            try:
                data = sock.recv(4)
            except socket.error as msg:
                print("Receive error")
                sys.exit()
            confirm_num = receiveint(data)


            # Client receives the 32-bit file length from server.
            # If it is -1, return to "prompt user for operation" state;
            # If not, save the file size
            if confirm_num != -1:
                size_file = confirm_num
            else:
                print(f"{filename} does not exist on the server!")
                continue


            # Receives the file and writes it down, also start counting
            start = time()
            with open(filename, "w") as f:
                data = sock.recv(size_file)
                if not data:
                    break
                f.write(data.decode())


            # end the counting
            end = time()


            # Print the result
            print(f"{size_file} bytes transferred in {end - start} seconds: {size_file / (end - start) * 0.000001} Megabytes/sec")
          

            # Return to "prompt client for operation" state
            continue


        elif (operation[:2] == 'UP'):
            # Send length of file
            filename = operation[2:].strip()
            try:
                sock.send(sendint(len(filename)))
            except socket.error as msg:
                print("Send length of file error!")
                sys.exit()
            

            # Send filename
            try:
                sock.send(filename.encode())
            except socket.error as msg:
                print("Send filename error!")
                sys.exit()


            # Receive ready message from server
            try:
                size_ready = sock.recv(4)
            except socket.error as msg:
                print("Receive error")
                sys.exit()

            try:
                msg = sock.recv(receiveint(size_ready))
            except socket.error as msg:
                print("Receive error")
                sys.exit()
            print(msg.decode())


            # Reply with the file size
            size = os.path.getsize(filename)
            try:
                sock.send(sendint(size))
            except socket.error as msg:
                print("Send length of file error!")
                sys.exit()


            # Send the file
            if os.path.exists(filename): 
                with open(filename, 'rb') as f:          # read file content
                    bytes_read = f.read(size)            # read the bytes from the file
                    if not bytes_read:
                        break                            # file transmitting is done
                    sock.sendall(bytes_read)             # send contents of the file
            else:
                print("There is no such file at your side!")
                continue


            # receive the counting time
            try:
                t = sock.recv(4)
            except socket.error as e:
                print("Receive count time error!")
                sys.exit()

            try:
                count_time = sock.recv(receiveint(t))
            except socket.error as e:
                print("Receive count time error!")
                sys.exit()
            time_ = float(count_time.decode())

            # Print the result
            print(f"{size} bytes transferred in {time_} seconds: {size / (time_) * 0.000001} Megabytes/sec")

        elif ((operation[:2] == 'RM') & (operation[2:5] != 'DIR')):
            # Send length of file
            filename = operation[2:].strip()
            try:
                sock.send(sendint(len(filename)))
            except socket.error as msg:
                print("Send length of file error!")
                sys.exit()


            # Send filename
            try:
                sock.send(filename.encode())
            except socket.error as msg:
                print("Send filename error!")
                sys.exit()


            # Receive confirmation number
            try:
                num = sock.recv(4)
            except socket.error as e:
                print("Receive confirmation number error!")
                sys.exit()
            confirm_num = receiveint(num)


            # If it is -1, inform the client and return to "prompt user for operation" state 
            # if it is 1, confirms if the user wants to delete the file and then sends it to the server    
            if confirm_num == -1:
                print(f"{filename} does not exist on the server!")
                continue
            else:
                client_ope = input("Do you want to delete it? ")
                sock.send(sendint(len(client_ope)))
                sock.send(client_ope.encode())
                if client_ope == "Yes":
                    
                    try:
                        size = sock.recv(4)                         # Receive size of acknowledgement
                    except socket.error as e:
                        print("Receive size error!")
                        sys.exit()
                    size_ack = receiveint(size)
                    try:
                        res = sock.recv(size_ack)
                    except socket.error as e:
                        print("Receive Server response error!")
                        sys.exit()
                    print(f"Server response: {res.decode()}")       # Print out server's response to then return to "prompt user for operation" state
                    continue
                else:
                    print("Delete abandoned by the user!")
                    continue

        elif (operation == 'LS'):
            # Receive the size
            try:
                data = sock.recv(1024)
            except socket.error as e:
                print("Receive size error!")
                sys.exit()
            size = receiveint(data)

            # Receive the directory listing
            try:
                dir = sock.recv(abs(size))
            except socket.error as e:
                print("Receive list of directory error!")
                sys.exit()
            
            # Display the list
            print(dir.decode())

            # Return to "prompt user for operation" state
            continue

        elif (operation[:5] == 'MKDIR'):
            # Send length of file
            directory = operation[5:].strip()
            try:
                sock.send(sendint(len(directory)))
            except socket.error as msg:
                print("Send length of file error!")
                sys.exit()


            # Send directory
            try:
                sock.send(directory.encode())
            except socket.error as msg:
                print("Send directory error!")
                sys.exit()

            
            # Receive confirmation number
            try:
                num = sock.recv(4)
            except socket.error as e:
                print("Receive confirmation nunmber error!")
                sys.exit()
            confirm_num = receiveint(num)


            # Perform operations based on the result of confirmation number
            if confirm_num == -2:
                print("The directory already exists on server")
                continue
            elif confirm_num == -1:
                print("Error in making directory")
                continue
            else:
                print("The directory was successfully made")
                continue

        elif (operation[:5] == 'RMDIR'):
            # Send length of file
            directory = operation[5:].strip()
            try:
                sock.send(sendint(len(directory)))
            except socket.error as msg:
                print("Send length of file error!")
                sys.exit()


            # Send directory
            try:
                sock.send(directory.encode())
            except socket.error as msg:
                print("Send directory error!")
                sys.exit()


            # Receive confirmation number
            try:
                num = sock.recv(4)
            except socket.error as e:
                print("Receive confirmation number error!")
                sys.exit()
            confirm_num = receiveint(num)


            # Perform operations based on the result of confirmation number
            if confirm_num == -2:
                print("The directory is not empty")
                continue
            elif confirm_num == -1:
                print("The directory does not exist on server")
                continue
            else:
                # when confirmation number is 1
                operation = input("Do you want to delete the directory? ")
                sock.send(sendint(len(operation)))
                sock.send(operation.encode())
                if operation == "Yes":
                    # Receives the acknowledgment
                    try:
                        delete_acknow = sock.recv(4)                        
                    except socket.error as e:
                        print("Receive delete acknowledgement error!")
                        sys.exit()
                    acknowledgement = receiveint(delete_acknow)

                    # Perform based on the acknowledgement
                    if acknowledgement > 0:
                        print("Directory deleted")
                        continue
                    elif acknowledgement < 0:
                        print("Failed to delete directory")
                        continue
                else:
                    print("Delete abandoned by the user!")
                    continue
                

        elif (operation[:2] == 'CD'):
            # Send length of file
            directory = operation[2:].strip()
            try:
                sock.send(sendint(len(directory)))
            except socket.error as msg:
                print("Send length of file error!")
                sys.exit()


            # Send filename
            try:
                sock.send(directory.encode())
            except socket.error as msg:
                print("Send filename error!")
                sys.exit()


            # Receive confirmation number
            try:
                num = sock.recv(4)
            except socket.error as e:
                print("Receive confirmation number error!")
                sys.exit()
            confirm_num = receiveint(num)
            

            # Perform operations based on the result of confirmation number
            if confirm_num == -2:
                print("The directory does not exist on server")
                continue
            elif confirm_num == -1:
                print("Error in changing directory")
                continue
            else:
                print("Changed current directory")
                continue

        elif (operation == 'QUIT'):
            sock.close()
            print("The session has been closed")
            break


############## End of Part 2 ##############


if __name__ == '__main__':
    # Your program will go with function part1() if there is no command line input. 
    # Otherwise, it will go with function part2() to handle the command line input 
    # as specified in the assignment instruction. 
    if len(sys.argv) == 1:
        part1()
    else:
        part2()

   