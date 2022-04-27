import sys
import socket
import threading
import time

def send_rec(cs):
    cname = cs.recv(1024).decode().rstrip()
    clients[cs][0] = cname
    print('got name: '+cname)
    cport = cs.recv(1024).decode().rstrip()
    print('got port: '+ cport)
    clients[cs][1] = (cport)
 
    while True:
        try:
            msg = cs.recv(1024).decode()
            if msg[0] == 'f':
                print('file is being requested by: '+ clients[cs][0])
                freq = msg.rsplit(u'\u0394')
                print(freq)
                
                fileowner = freq[1]
                fname = freq[2]
                

                for s in clients:
                    
                    
                    if clients[s][0] == fileowner:
                        print('found owner socket')
                        s.send(('f').encode())
                        time.sleep(0.1)
                        s.send((clients[cs][1]).encode())
                        time.sleep(0.1)
                        s.send(fname.encode())
                
            if msg[0] == 'm':
                for s in clients:
                    if s != cs:
                        print('sending msg from '+clients[cs][0] + " to " + clients[s][0])
                        s.send((clients[cs][0] + ": "+ msg[1:]).encode())
        except Exception as e:
            print('removing client '+clients[cs][0])
            clients.pop(cs)
            print('exception hit: '+ str(e))
            break



def listen(server):
    while True:
        cs, addr = server.accept()
        clients[cs] = ['',0]
        send_rec_thread = threading.Thread(target=send_rec,args=(cs,))
        send_rec_thread.start()








listen_port = int(sys.argv[1])

global clients
clients = {}

serversocket_msg = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #returns socket object 'serversocket'

serversocket_msg.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)

serversocket_msg.bind(('', listen_port))

serversocket_msg.listen(5)

listen(serversocket_msg)