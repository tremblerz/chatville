import socket, select, string, sys
 
def prompt() :
    sys.stdout.write('<You>: ')
    sys.stdout.flush()

def exit(sock):
  print "\n Thank you for using chat application\nBye"
  sock.close()
  sys.exit()

def printUsage():
  print "1. By default your message will be sent to all clients sitting on the chat server"
  print "2. You can send a private message to a person by starting your message as \"/msg{id}{Your message}\" for example /msg2Hi will send \"hi\" to client with id 2"
  print "3. For quitting simply type \"/q\" or \"/quit\""
  prompt()
 
PORTS = 2225
PORTC = 2624


if __name__ == "__main__":
     

    broad = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    broad.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broad.bind(( '0.0.0.0' , 2624) )
    broad.sendto(b'whoisserver', 0, ("255.255.255.255", PORTS))
    broad.settimeout(10)
    print 15*"-" + "WELCOME TO CHATVILLE" + 15*"-" + "\nFinding the server"
    try:
      data , addr = broad.recvfrom(10)
    except:
      print "Can't find server ! Please ensure that server is up"
      broad.close()
      sys.exit()
    broad.close()


    if data <> "iam":
      print "Can't find a valid server !"
      sys.exit()
    host = addr[0]
    port = 5000
    print addr


#    host = sys.argv[1]
#    port = int(sys.argv[2])
#    print host,port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    name = raw_input("Please Enter your name: ")
    try :
        s.connect((host, port))
        s.send(name)
    except :
        print 'Unable to connect'
        sys.exit()

    print 'Connected to remote host. Enjoy...............................'
    name = "<" + name + ">" + ": "
    print " - type /h to see usage instructions any time :) - "
    prompt()

    while 1:
        socket_list = [sys.stdin, s]

        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data :
                    print '\nDisconnected from chat server'
                    sys.exit()
                else :
                    print ""
                    sys.stdout.write(data)
                    prompt()
             
            else :
                msg = sys.stdin.readline()
                if str.startswith(msg, "/h") or str.startswith(msg,"/help"):
                  printUsage()
                elif str.startswith(msg, "/quit") or str.startswith(msg,"/q"):
                  exit(s)
                else:
                  msg = name + msg
                  s.send(msg)
                  prompt()
