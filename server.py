import socket, select,re


def getSocket( idd):
  return CONNECTION_LIST[idd]


def broadcast_data (sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock :
            try :
                socket.send(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)


def single_client (sock , message , idd):
  socket = getSocket ( idd )
  if socket :
    socket.send(message)
  else:
    print "chudap"


if __name__ == "__main__":
     
    CONNECTION_LIST = []
    RECV_BUFFER = 4096 
    PORT = 5000
    PORTC = 2225
 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    listen.bind(("0.0.0.0" , PORTC))
    #listen.listen(10)

    CONNECTION_LIST.append(server_socket)
    CONNECTION_LIST.append(listen) 
    print "Chat server started on port " + str(PORT)
 
    idd = 1
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                #name = sockfd.recv(RECV_BUFFER)
                print "connected from ip %s, id assigned is %d" % (addr[0] , idd)
                broadcast_data(sockfd, "client with IP %s has entered with id = %d\n" % (addr[0] , idd))
                idd += 1
            elif sock == listen:
                print "debugging"
                data,addr = listen.recvfrom(RECV_BUFFER)
                print "Received server probe request from [%s:%s]"%addr
                listen.sendto("iam" , addr)#(addr[0] , 2624))
                listen.close()
                CONNECTION_LIST.remove(listen)
                listen = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                listen.bind(("0.0.0.0" , PORTC))
                CONNECTION_LIST.append(listen)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if re.findall(r'.*/msg\d+' , data):
                      #print "got single client message request" + data

                      name = "private message from " + re.findall('([^:]+): /msg(\d+)([^"]+)'  , data)[0][0] + ": "
                      #print name

                      eid = int(re.findall('([^:]+): /msg(\d+)([^"]+)'  , data)[0][1])
                      #print eid

                      data = re.findall('([^:]+): /msg(\d+)([^"]+)'  , data)[0][2]
                      #print data

                      data = name + data

                      #print "single client message sent with id = %d" %eid

                      single_client( sock , data , int(eid))
                    elif data:
                        broadcast_data(sock, data)                
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
