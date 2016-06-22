#!/usr/bin/python
import socket
import time
def main():
    try:
	while True:
            client_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	    client_socket.connect(('127.0.0.1',8899))
	    with open('/etc/passwd','r') as f:
	        client_socket.send(''.join(f.readlines()))
	    time.sleep(1)
	    client_socket.close()
	#response=client_socket.recv(9877)
    except Exception as e:
	print e
if __name__=='__main__':
    main()

