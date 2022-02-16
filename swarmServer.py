import socket, threading                                          #Libraries import
from subprocess import run
import hashlib



node_host = '127.0.0.1'
node_port = 8977

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((node_host, node_port)) 

serverName = input("inputServerName: ")


########  CONNECT TO MAIN_NODE  ##########
BUF_SIZE = 65536 

sha1 = hashlib.sha1()

def getHash():
    with open("server.py", 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)


    fileHash = sha1.hexdigest()

    print("SHA1: {0}".format(fileHash))

    return fileHash

getHash()

def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(serverName.encode('ascii'))
            else:
                print(message)
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            client.close()
            break

#@dev just think about it, this works but can be optimized...
def write():
    while True:                                                 #message layout
        message = '{}:{}'.format(serverName, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()






############################################


import socket, threading                                          #Libraries import
from subprocess import run
import hashlib


host = '127.0.0.1'                                                #LocalHost
port = 3453                                                       #Choosing unreserved port

clients = []
usernames = []

#dictionary to link usernames to socket info
users = {}

#dictionary to link usernames to their ipfs uris 
messages = {}


##################


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)              #socket initialization
server.bind((host, port))                                               #binding host and port to socket
server.listen()


def broadcast(message):                                                 #broadcast function declaration
    for client in clients:
        client.send(message)


def broadcastUser(user, message):
    uri = message
    client = users[user][0]
    uri = uri.encode('ascii')

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



def inbox(user, uri):
    if user not in messages:
        messages[user] = []
    messages[user].append(uri)
    print(messages)
    


def handle(client):                                         
    while True:
        try:                                                            #recieving valid messages from client
            message = client.recv(1024)
            user, text = cleanData(message)
            uri = uploadIPFS(text)

            inbox(user, uri)

            broadcastUser(user, uri)

            #broadcast(message)

        except:                                                         #removing clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]

            del users[username]

            print('{} left!'.format(username))

            print(str(len(clients))+" currently connected")

            broadcast('{} left!'.format(username).encode('ascii'))
            usernames.remove(username)
            break


def receive():                                                          #accepting multiple clients
    while True:
        print("Server Started")

        client, address = server.accept()
        
        #print("Connected with {}".format(str(address))) 

        client.send('NICKNAME'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        usernames.append(username)
        clients.append(client)

        print(str(len(clients))+" currently connected") 

        users[username] = [client, address]

        print("{} is connected".format(username))
        #broadcast("{} joined!".format(nickname).encode('ascii'))

        client.send('Connected to server!'.encode('ascii'))
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

receive()
