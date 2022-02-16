from ipaddress import ip_address
import socket, threading        
from random import randrange                                  #Libraries import


"""This script acts as the main server node. If a server wants to be part of the swarm, 
it sends a hash. If it is the correct hash, the server is added to the swarm.
Users initially connect to this main-node server to get pointed to
a server that will connect them to IPFS chat. """



host = '127.0.0.1'                                                      #LocalHost
port = 7899                                                             #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
serverNames = []

serverDetails = {}



def addServertoSwarm(server, host, port, users):

    if server not in serverDetails:
        serverDetails[server] = []

    serverDetails[server].append(host)
    serverDetails[server].append(port)

    # swarm server sends update of users to to main node
    serverDetails[server].append(users)

    print(serverDetails)
    print("server {} added to swarm".format(server))




def cleanData(message):
    data = message
    m = data.decode("utf-8")
    l = m.split(':')

    server = l[0]
    text = l[1]

    text = text.strip()
    print(server, text)

    return server, text



def getServer():
    print(serverDetails)
    totalServers = int(len(serverDetails))

    if totalServers > 1:
        n = totalServers - 1

        randServer = randrange(n)
        print("if")

    else: 
        print("else")
        randServer = 0
    
    swarmServers = list(serverDetails)
    
    print(swarmServers)
    server = swarmServers[randServer]
    
    ip = serverDetails[server][0]
    port = serverDetails[server][1]

    return ip, port



def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)


####### Rudementary handler
####### if client sends hash, then we assume it is a server
####### if not, we assume it is a user and pass them IP and port of a server

def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            print(message)

            server, text = cleanData(message)

            print(text)

            fileHash = "46f0eccbe13313571a0f4adfc42a80230ebb5c47"


            if text == fileHash:
                
                addServertoSwarm(server,'127.0.0.1',5555,0)


            else:
                # you need to split users and servers
                print("user")

                """print("server not added; user")

                ip, port = getServer()

                print(ip)
                print(port)

                server = "{}:{}".format(str(ip),str(port))

                msg = server.encode('ascii')

                print(msg)
                client.send(msg)"""



        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            serverName = serverNames[index]
            print('{} left!'.format(serverName))
            
            serverNames.remove(serverName)
            break


"""def receive():                                                          #accepting multiple clients
    while True:
        client, address = server.accept()

        print("Connected with {}".format(str(address)))       

        client.send('NICKNAME'.encode('ascii'))





        serverName = client.recv(1024).decode('ascii')

        serverNames.append(serverName)

        clients.append(client)

        client.send('Connected to MAIN NODE!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()"""


def receive():
    while True:
        client, address = server.accept()

        print("Connected with {}".format(str(address)))       

        client.send('PING'.encode('ascii'))

        serverName = client.recv(1024).decode('ascii')

        print(serverName)

        if serverName == "USER":

            client.send('Connected to MAIN NODE as USER!'.encode('ascii'))

            ip, port = getServer()

            print(ip)
            print(port)

            swarmServer = "{}:{}".format(str(ip),str(port))

            msg = swarmServer.encode('ascii')

            print(msg)
            client.send(msg)

            #client.close()

        else: 
            print("main node else")
            serverNames.append(serverName)
            clients.append(client)
            client.send('Connected to MAIN NODE: send hash!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()

"""    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode('ascii'))

        serverName = client.recv(1024).decode('ascii')

        if serverName == "USER":

            client.send('Connected to MAIN NODE!'.encode('ascii'))

            ip, port = getServer()

            print(ip)
            print(port)

            server = "{}:{}".format(str(ip),str(port))

            msg = server.encode('ascii')

            print(msg)
            client.send(msg)

        else: 
            serverNames.append(serverName)
            clients.append(client)
            client.send('Connected to MAIN NODE!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()"""