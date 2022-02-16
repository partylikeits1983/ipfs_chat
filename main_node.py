from ipaddress import ip_address
import socket, threading        
import random                                        #Libraries import




host = '127.0.0.1'                                                      #LocalHost
port = 5677                                                             #Choosing unreserved port

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
    #text = eval(text)
    print(server, text)
    print(type(text))
    return server, text



def getServer():
    totalServers = int(len(serverDetails))
    
    randServer = random.randint(0, totalServers-1)
    
    servers = list(serverDetails)
    
    server = servers[randServer]
    
    ip = serverDetails[server][0]
    port = serverDetails[server][1]

    return ip, port



def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)


####### Rudementary handler
####### if client sends hash, then we assume it is a server
####### if not, we assume it is a user



def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            print(message)

            server, text = cleanData(message)

            print(text)

            fileHash = "9a8ab6a3bcab201bcca8693946976d6957c4f11a"


            if text == fileHash:
                print("inside")
                addServertoSwarm(server,'127.0.0.1',5555,0)



            else:
                # you need to split users and servers
                print("server cannot be added")

                ip, port = getServer()

                print(ip)
                print(port)

                server = "{}:{}".format(str(ip),str(port))

                msg = server.encode('ascii')

                print(msg)
                client.send(msg)



        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            serverName = serverNames[index]
            print('{} left!'.format(serverName))
            
            serverNames.remove(serverName)
            break


def receive():                                                          #accepting multiple clients
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))       
        client.send('NICKNAME'.encode('ascii'))
        serverName = client.recv(1024).decode('ascii')
        serverNames.append(serverName)
        clients.append(client)
        #print("Nickname is {}".format(serverName))
        #broadcast("{} joined!".format(serverName).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()