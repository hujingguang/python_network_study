#!/usr/bin/python
# --*-- coding: utf8
import select
from SocketServer import StreamRequestHandler
import SocketServer
import socket

#阻塞式网络通信
def server():
    try:
        server_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server_socket.bind(('127.0.0.1',8899))
	server_socket.listen(20)
	while True:
	    conn,addr=server_socket.accept()
	    print conn,addr
	    print '-------------------'
	    data=conn.recv(1024)
	    print data
	    if not data:
		conn.close()
    except Exception as e:
	print '-----------------'
	print e
    finally:
	server_socket.close()

def server1():
    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk.bind(('0.0.0.0',8899))
    sk.listen(128)
    while True:
	conn,addr=sk.accept()
	data=conn.recv(1024)
	while data:
	    print data
	    data=conn.recv(1024)
	conn.close()

#select模型
def server_select():
    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk.bind(('0.0.0.0',8899))
    sk.listen(128)
    inputs=[sk]
    while True:
	socket_list,ws,rs=select.select(inputs,[],[])
	for s in socket_list:
	    if s is sk:
		conn,addrs=s.accept()
		print 'get connected address:'+str(addrs)
		inputs.append(conn)
	    else:
		data=s.recv(1024)
		disconnected=not data
	        if disconnected:
		    inputs.remove(s)
	        else:
		    print data

#异步IO的poll模型
def server_poll():
    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk.bind(('0.0.0.0',8899))
    sk.listen(128)
    fdmap={sk.fileno():sk}
    r=select.poll()
    r.register(sk)
    while True:
	events=r.poll()
	for fd,e in events:
	    data=''
	    if fd == sk.fileno():
		conn,addr=fdmap[fd].accept()
		r.register(conn)
		fdmap[conn.fileno()]=conn
	    elif fd & select.POLLIN:
		data=fdmap[fd].recv(1024)
		if not data:
		    r.unregister(fdmap[fd])
		    del fdmap[fd]
		else:
	            print data
		    

def server_epoll():
    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk.bind(('0.0.0.0',8899))
    sk.listen(128)
    fdmap={sk.fileno():sk}
    ep=select.epoll()
    ep.register(sk)
    while True:
	events=ep.poll()
	for fd,event in events:
	    if fd == sk.fileno():
		conn,addr=sk.accept()
		print 'get a connected '+str(addr)
		ep.register(conn)
		fdmap[conn.fileno()]=conn
	    elif fd & select.EPOLLIN:
		data=fdmap[fd].recv(1024)
		if not data:
		    ep.unregister(fd)
		    del fdmap[fd]
		else:
		    print data





#分叉模型和多线程模型实例
	
class Handler(StreamRequestHandler):
    def handle(self):
	while True:
	    data=self.request.recv(1024)
	    if not data:
		self.wfile.write('123123')
		break
	    print data
	    #self.request.send(data)
	    #self.wfile.write('helloworld')
if __name__ == '__main__':
    #server_select()
    server_epoll()
    #server_poll()
    #server()
    exit()
    #server1()
    #tcpserver=SocketServer.ThreadingTCPServer(('0.0.0.0',8899),Handler)
    tcpserver=SocketServer.ForkingTCPServer(('0.0.0.0',8899),Handler)
    tcpserver.serve_forever()
