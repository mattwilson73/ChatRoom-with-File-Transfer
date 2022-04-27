#fClient

import sys
import socket
import threading
import os
import time
import struct

def log(m):
    print(name + ": " + str(m))


def f_server(p,fname):
    print('starting file recieving server')
    f_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    f_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    f_server_socket.bind(('',p))
    f_server_socket.listen(5)
    owner_socket, addr = f_server_socket.accept()
    print('accepted connection from remote client')
    xfsaver(owner_socket,fname)
    f_server_socket.close()


def f_sender(requesting_port,fname):
    requesting_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    requesting_socket.connect(('localhost',int(requesting_port)))
    print('connected to remote file server')
    #send file now
    sfsender(requesting_socket,fname)
    

def recieve_msg(s_msg):
    while True:
        try:
            msg = s_msg.recv(1024).decode()
            if msg == 'f':
                #file was requested
                #print('file is being requested')
                requesting_port = s_msg.recv(1024).decode()
                print('requesting port as: '+ requesting_port)
                fname = s_msg.recv(1024).decode()
                print('fname as: ' + fname)
                f_sender_thread = threading.Thread(target=f_sender,args=(requesting_port,fname))
                f_sender_thread.start()





            if msg == "":
                break
            else:
                print(msg)
        except Exception as e:
            print('exception hit: '+ str(e))


def control(s, p):
    while True:
        print("Enter an option ('m', 'f', 'x'): ")
        print("(M)essae (send)")
        print("(F)ile (request)")
        print("e(X)it")
        c = input()

        if c == 'm':
            print("Enter your message:")
            msg = 'm' + sys.stdin.readline().rstrip()
            s.send(msg.encode())

        if c == 'f':
            print("Who owns the file?")
            owner = sys.stdin.readline().rstrip()
            print("Which file do you want?")
            fname = sys.stdin.readline().rstrip()
            f_server_thread = threading.Thread(target=f_server,args=(p,fname))
            f_server_thread.start()
            freq = 'f' + u'\u0394' + owner + u'\u0394' + fname
            s.send(freq.encode())

        if c == 'x':
            log('exiting')
            os._exit(0)

################

def xfsaver(sock,filename):
    file_size_bytes= sock.recv( 4 )
    if file_size_bytes:
        file_size= struct.unpack( '!L', file_size_bytes[:4] )[0]
        if file_size:
            receive_file( sock, filename )
        else:
            print( 'File does not exist or is empty' )
    else:
        print( 'File does not exist or is empty' )
    sock.close()

def receive_file( sock, filename ):
	# receive the file lines returned from the server
	file= open( filename, 'wb' )
	while True:
		file_bytes= sock.recv( 1024 )
		if file_bytes:
			file.write( file_bytes )
		else:
			break
	file.close()


##############


def sfsender(sock,file_name):
    try:
        file_stat= os.stat( file_name )
        if file_stat.st_size:
            file= open( file_name, 'rb' )
            send_file( sock, file_stat.st_size, file )
        else:
            no_file( sock )
    except OSError:
        no_file( sock )
    sock.close()

def send_file( sock, file_size, file ):
	print( 'File size is ' + str(file_size) )
	file_size_bytes= struct.pack( '!L', file_size )
	# send the number of bytes in the file
	sock.send( file_size_bytes )
	# read the file and transmit its contents
	while True:
		file_bytes= file.read( 1024 )
		if file_bytes:
			sock.send( file_bytes )
		else:
			break
	file.close()

def no_file( sock ):
	zero_bytes= struct.pack( '!L', 0 )
	sock.send( zero_bytes )

#################

listen_port = int(sys.argv[2])
server_port = int(sys.argv[4])

if len(sys.argv) > 5:
    global name
    name = str(sys.argv[5])
    print("Debug Mode: Running with name " + name)
else:
    print("What is your name?")
    name = sys.stdin.readline()

    


s_msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_msg.connect(('localhost',server_port))

s_msg.send(name.encode())
time.sleep(0.5)
s_msg.send(str(listen_port).encode())

recieve_thread = threading.Thread(target=recieve_msg, args=(s_msg,))
recieve_thread.start()

control(s_msg, listen_port)



