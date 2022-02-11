import socket, threading                                                #Libraries import
from subprocess import run


host = '127.0.0.1'                                                      #LocalHost
port = 5078                                                          #Choosing unreserved port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()

clients = []
nicknames = []

users = {}

def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)


### psydo code
def broadcastUser(user, message):
    print("inside bU")

    uri = message

    client = users[user][0]

    uri = uri.encode('ascii')

    print(uri)

    print(type(uri))

    try: 
        client.send(uri)
        print("sent")
    except:
        print("sad :(")

    


def cleanData(message):
    data = message
    m = data.decode("utf-8")
    l = m.split('~')

    user = l[0]
    text = l[1]
    
    text = eval(text)

    return user, text



# server side upload function
def uploadIPFS(message):
    with open("txt.txt", "wb") as txt:
        txt.write(message)
    cmd = [ 'ipfs', 'add', 'txt.txt' ]
    out = run(cmd, capture_output=True).stdout
    output = out.decode("utf-8")
    outputs = output.split(" ")
    uri = outputs[1]
    return uri



def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)

            user, text = cleanData(message)

            uri = uploadIPFS(text)

            print(uri)

            broadcastUser(user, uri)

            #broadcast(message)

        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]

            del users[nickname]

            broadcast('{} left!'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():                                                          #accepting multiple clients
    while True:
        print("server running")

        client, address = server.accept()
        
        print("Connected with {}".format(str(address)))  

        client.send('NICKNAME'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        users[nickname] = [client, address]

        print(users)

        print("Nickname is {}".format(nickname))
        #broadcast("{} joined!".format(nickname).encode('ascii'))

        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()

#kill -9 $(ps -A | grep python | awk '{print $1}')
