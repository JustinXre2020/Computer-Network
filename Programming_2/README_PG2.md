

# Contributors

Jerry Guo 		    zemingg2

Justin Xiao 		  xulongx2

Tiancheng Shi 	ts15



# Files in the directory:

## tcpserver.py
```
It contains Part1, Part2 and some helper functions that help us establish communication between the server and the client.
	1. sendint(data)		Helper function, convert from int to byte.
	2. receiveint(data)		Helper function, convert from byte to int.
	3. part1()				Simple TCP application establish the connection with the client send a string to the client. 
	4. part2()				Enable some operations
		Operation Availible:
			DN:
                Decodes what it receives, and checks to see if the file exists in its local directory.
                If the file user asks exists, server returns the size of the file to the client as a 32-bit integer.
                If the file does not exist, server will return a negative confirmation (32-bit integer value -1). After that, the server should return to the "wait for operation from client" state.
                Server sends the file to client.
            UP:
                Server receives and decodes the 32-bit value.
                Server enters the loop to receive file.
                Server computes throughput results for the transfer and sends it to the client.
                Server sends the throughput results to the client. The client displays the throughput of the transfer.
			RM:
                Server receives the above information, decodes filename size and filename, and checks if the file to be deleted exists or not.
                If the file client asks exists, the server sends a positive confirmation (integer value 1) back to the client.
                If the file does not exit, the server sends a negative confirmation (integer value -1) back to the client.
                The server waits for the delete confirmation sent by the client.
                If the confirmation is "Yes", the server deletes the requested file and returns an acknowledgment to the client to indicate the success or failure of file deletion operation.
                If the confirmation is "No", the server returns to "wait for operation from client" state.
			LS:
                Server obtains listing of it's directory, including both the permission settings and the name of each file (e.g., "-rwxr-xr-x 1 netid dip 21K Aug 22 12:58 test.txt" or simply "-rwxr-xr-x test.txt" )
                Server computes the size of directory listing and sends the size to client as a 32-bit integer.
			MKDIR:
                Server receives the length of the directory name followed by the directory name which will be sent (short int) followed by the directory name, decodes directory name size and directory name, and checks if the directory to be created exists or not.
                If the directory exists, the server sends a negative confirmation (integer value -2) back to the client.
                If the directory does not exit, the server sends a positive confirmation (integer value 1) back to the client if the directory is successfully created; otherwise, the server sends a negative confirmation (integer value -1) back to the client.
			RMDIR:
                Server receives the length of the directory name followed by the directory name, decodes directory name size and directory name, and checks if the directory to be deleted exists or not.
                If the directory exists and is empty, the server sends a positive confirmation (integer value 1) back to the client.
                If the directory does not exit, the server sends a negative confirmation (integer value -1) back to the client.
                If the directory exists and is not empty, the server sends a negative confirmation (integer value -2) back to the client.
                The server waits for the delete confirmation sent by the client.
                If the confirmation is "Yes" the server deletes the requested directory and returns an acknowledgment to the client to indicate the success or failure of file deletion operation. (Directory must be empty in order for deletion to occur).
                If the confirmation is "No" the server returns to "wait for operation" state.
			CD:
                Server receives the length of the directory name followed by the directory name, decodes directory name size and directory name, and checks if the directory to be changed to exists or not.
                If the directory exists, the server sends a positive confirmation (integer value 1) back to the client if it successfully changed directories; otherwise, the server sends a negative confirmation (integer value -1) back to the client.
                If the directory does not exist, the server sends a negative confirmation (integer value -2) back to the client.
                QUIT:
					Server closes the socket and goes back to the "wait for connection" state.
```
## tcpclient.py

	It contains Part1, Part2 and some helper functions that help us establish communication between the server and the client.
		1. sendint(data)		Helper function, convert from int to byte.
		2. receiveint(data)		Helper function, convert from byte to int.
		3.part1()				Simple TCP application establish the connection with the server and send a string to the client. 
		4.part2()				Enable some operations
			DN:
	            Client sends operation (DN) to download a file from the server.
	            Client sends the length of the filename (short int) followed by the filename (character string).
	            Client receives the 32-bit file length from server.
	            Client should decode the 32-bit value.
	            If the value is -1, user should be informed that the file does not exist on the server. Client should return to "prompt user for operation" state.
	            If the value is not -1, save the value as the file size for later use.
	            Server sends the file to client.
	            Client reads "file size" bytes from server.
	            The client saves the file to disk as "filename".
	            Inform user that the transfer was successful, and return to "prompt user for operation" state. The client displays throughput results for the transfer.
	    	UP:
	            Client sends operation (UP) to upload a local file to a server.
	            Client sends the length of the filename which will be sent (short int) followed by the filename (character string).
	            Client replies with a 32-bit value which is the size of the file (in bytes).
	            Server receives and decodes the 32-bit value.
	            Client sends file to server. Server reads "file size" bytes from client and saves them to disk as "filename".
	        RM:
	            Client sends operation (RM) to delete a file from the server. Note: you can create a test file called "delete.txt" in the server directory to test the RM operation.
	            Client sends the length of the filename which will be sent (short int) followed by the filename (character string).
	            Client receives the confirmation from the server.
	            If the confirmation is negative, it should inform the user that the file does not exist on the server and return to "prompt user for operation" state.
	            If the confirmation is positive, the client further confirms if the user wants to delete the file: "Yes" to delete, "No" to ignore. The client then sends the user's confirmation (i.e., "Yes" or "No") back to the server.
	            If the user's confirmation is "Yes", the client waits for the server to send the confirmation of file deletion.
	            If the user's confirmation is "No", the client prints out "Delete abandoned by the user!" and returns to "prompt user for operation" state.
	        LS:
	            Client sends operation (LS) to list the directory at the server.
	            Client receives the size of the dictionary, and goes into a loop to read directory listing.
	            Once the listing is received, client displays the listing to user.
	            Client and server return to "prompt user for operation" and "wait for operation from client" state respectively.
	        MKDIR:
	            Client sends operation (MKDIR) to make a directory on the server.
	            Client sends the length of the directory name which will be sent (short int) followed by the directory name (character string).
	            Client receives the confirmation from the server.
	            If the confirmation is negative (-2), it prints out "The directory already exists on server" and returns to "prompt user for operation/wait for operation" state.
	            If the confirmation is negative (-1), it prints out "Error in making directory" and returns to "prompt user for operation/wait for operation" state.
	            If the confirmation is positive, the client prints out "The directory was successfully made" and returns to "prompt user for operation/wait for operation" state.
	        RMDIR:
	            Client sends operation (RMDIR) to remove a directory on the server. Note: Directory must be empty for RMDIR to work.
	            Client sends the length of the directory name which will be sent (short int) followed by the directory name (character string).
	            Client receives the confirmation from the server.
	            If the confirmation is negative (-1), it prints out "The directory does not exist on server" and returns to "prompt user for operation/wait for operation" state.
	            If the confirmation is negative (-2), it prints out "The directory is not empty" and returns to "prompt user for operation/wait for operation" state.
	            If the confirmation is positive, the client further confirms if the user wants to delete the directory: "Yes" to delete, "No" to ignore. The client then sends the user's confirmation (i.e., "Yes" or "No") back to the server.
	            If the user's confirmation is "Yes" the client waits for the server to send the confirmation of directory deletion.
	            If the user's confirmation is "No" the client prints out "Delete abandoned by the user!" and returns to prompt user for operation/wait for operation state.
	            If the acknowledgment from the server is positive, the client prints out "Directory deleted" and returns to "prompt user for operation" state.
	            If the acknowledgment is negative, the client prints out "Failed to delete directory" and returns to "prompt user for operation" state.
	        CD:
	            Client sends operation (CD) to change to a different directory on the server. Note: You can use CD followed by LS to verify that CD worked successfully.
	            Client sends the length of the directory name which will be sent (short int) followed by the directory name (character string).
	            Client receives the confirmation from the server.
	            If the confirmation is negative (-2), it prints out "The directory does not exist on server" and returns to "prompt user for operation/wait for operation" state.
	            If the confirmation is negative (-1), it prints out "Error in changing directory" and returns to "prompt user for operation/wait for operation" state.
	            If the confirmation is positive, the client prints out "Changed current directory" and returns to "prompt user for operation/wait for operation" state.
	        QUIT:
	            Client sends operation (QUIT) to exit.
	            Client closes the socket, and exits.
	            Client informs user that the session has been closed.It contains two functions that send messages to the server.
# To run/test the code:

	1. Change the hostname and port in "tcpserver.py" and "tcpclient.py" to your own hostname and port, and save your change.
	
	2. Send all of these three files from local to remote using the command "scp (local address) (remote address)"
		After that, run“ls”to see if these files have been uploaded successfully.
		eg.  scp ./Desktop/IS496/tcpserver.py zemingg2@student00.ischool.illinois.edu
	
	3. Connect to two different student machines in two terminal windows with the command "ssh (remote address)"
		Determine which terminal is the server and which terminal is the client.
		eg.  ssh zemingg2@student00.ischool.illinois.edu
				ssh zemingg2@student01.ischool.illinois.edu
	
	4. For part 1, in the server command line window, type "python3 tcpserver.py"
		eg.  python3 tcpserver.py
	
	5. Then in the client command line window, type "python3 tcpclient.py"
		eg.  python3 tcpclient.py
	
	6. For part 2, in the server command line window, type "python3 tcpserver.py [port]"
		eg.  python3 tcpserver.py 41002
	
	7. In the client command line window, type "python3 tcpclient.py [hostname] [port]"
		Notice to not compile the client file in the server window! 
		Also it can accept with any other random string.
		eg.  python3 tcpclient.py student00.ischool.illinois.edu 41002
	
	8. Also for Part 2:
		Enter the operation you want in the client command line window, and wait the response of the server.
		It will ask you for your operation:
		"Please enter your operation:"
		Here are the formats of performing each of the operations:
			DN filename				download the file from the server
			UP filename				upload the file to the server
			RM filename				remove the file from the server
			LS 						list the directory on the server
			MKDIR directory_name	create a new directory on the server
			RMDIR directory_name	remove the directory from the server
			CD directory_name		chnage to another directory on the server 
			(if the directory_name is "..", the go back to the previous directory)
	        QUIT					client closes the socket and exit, server closes the socket and goes back to "wait for connection" state
			
			
