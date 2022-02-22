# Files in the directory:

## pg1lib.py
It contains some helper functions that help us establish communication between the server and the client.
	1. getPubKey()		Get the public key of server/client's.
	2. encrypt(message, pubkey)	Encrypt the message with a public key.
	3. decrypt(cipher)		Decrypt the message by a private key.
	4. checksum(data)		Check the sum of the message received.
## udpserver.py
It contains two functions that start the server and receive messages from the client.
## udpclient.py
It contains two functions that send messages to the server.

# To run/test the code:

1. Change the hostname and port in "udpserver.py" and "udpclient.py" to your own hostname and port, and save your change.

2. Send all of these three files from local to remote using the command "scp (local address) (remote address)"
	After that, run“ls”to see if these files have been uploaded successfully.
	eg.  scp ./Desktop/IS496/udpserver.py zemingg2@student00.ischool.illinois.edu

3. Connect to two different student machines in two terminal windows with the command "ssh (remote address)"
	Determine which terminal is the server and which terminal is the client.
	eg.  ssh zemingg2@student00.ischool.illinois.edu
	        ssh zemingg2@student01.ischool.illinois.edu

4. For part 1, in the server command line window, type "python3 ./udpserver.py"
	eg.  python3 ./udpserver.py

5. Then in the client command line window, type "python3 ./udpclient.py"
	eg.  python3 ./udpclient.py

6. For part 2, in the server command line window, type "python3 ./udpserver.py [port]"
	eg.  python3 ./udpserver.py 41002

7. In the client command line window, type "python3 ./udpclient.py [hostname] [port] [test message]"
	Notice to not compile the client file in the server window! 
	Also it can accept with any other random string.
	eg.  python3 ./udpclient.py student00.ischool.illinois.edu 41002 "Howdy World!"
