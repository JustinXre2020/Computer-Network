# Import any necessary libraries below
import socket
import sys



# TODO: define a buffer size for the message to be read from the UDP socket
BUFFER = 2048


print("Welcome to TCP Server.")


HOST = socket.gethostbyname("student01.ischool.illinois.edu")
PORT = 41008
sin = (HOST, PORT)



try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as e:
    print('Failed to create socket.')
    sys.exit()



try:
    sock.bind(sin)
except socket.error as e:
    print('Failed to bind socket.')
    sys.exit()
opt = 1
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, opt)

print("Waiting ...")


sock.listen()
try:
    conn, addr = sock.accept()
except socket.error as e:
    print("Nothing accepts.")



# to_client = socket.htonl(1)
to_client = "This is the server, how can I help?"
try:
    # conn.send(to_client.to_bytes(4, byteorder='big'))
    bytes_sent = conn.send(to_client.encode())
except socket.error as e:
    print("Send error!")
    sys.exit()
print(f"Sent {bytes_sent} bytes")


# try:
#     sock.close()
# except socket.error as msg:
#     print("Socket close failed!")
#     sys.exit()