# Import any necessary libraries below
import socket
import sys


# TODO: define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


HOST = sys.argv[1]
PORT = sys.argv[2]
message = sys.argv[3]


try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as msg:
    print('Failed to create socket.')
    sys.exit()


sock.connect((HOST, int(PORT)))


# try:
#     sock.send(message.encode())
# except socket.error as msg:
#     print("Client send error!")
#     sys.exit()



try:
    data = sock.recv(BUFFER)
except socket.error as msg:
    print("Receive error")
    sys.exit()
# data_int = int.from_bytes(data, "big")
# data_host = socket.ntohl(data_int)
msg = data.decode()


print(f"Result: {msg}")    



try:
    sock.close()
except socket.error as msg:
    print("Socket close failed!")
    sys.exit()
