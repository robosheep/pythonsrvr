#!/usr/bin/python3

from socket import *
import _thread
import subprocess,sys,shlex

# Buffer size to print
BUFF = 1024

# IP to listen on
HOST = '0.0.0.0'# must be input parameter @TODO

# port number
PORT = 9999 # must be input parameter @TODO

# Host and Port var
ADDR = (HOST, PORT)

# Using IPv4
s = socket(AF_INET, SOCK_STREAM)

# SOL_SOCKET Data to receive
# SO_REUSEADDR
s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

# Bind to the IP and port
s.bind(ADDR)

# Number of backlog connections to accept
# before refusing connections.
s.listen(1)

def handler(clientsock,addr):
    while 1:
        data = clientsock.recv(BUFF)
        if not data: 
          break

        data = data.decode('UTF-8')

	# Command list
        #t_cmds = ["ps -ef", "netstat -apn --inet","last -10"]
        #t_cmds = [ ]
        data = data.replace("\n","")
        results = subprocess.check_output(data, stderr=subprocess.STDOUT, shell=True)
        print(str(clientsock.sendall(results)))


	# type 'close' on client console to close connection from the server side
        if "close" == data.rstrip(): 
          break 

    clientsock.close()
    print(addr, "- closed connection") #log on console

# Top level code execution.
if __name__=='__main__':
	# While loop to wait for connections.
	while 1:
	    print('waiting for connection... listening on port', PORT)
	
	    # Accepts connections
	    # clientsock is an object to send/recv messages
	    # address is the address of the remote connection.
	    clientsock, addr = s.accept()
	    print('...connected from:', addr)
	    _thread.start_new_thread(handler, (clientsock, addr))
