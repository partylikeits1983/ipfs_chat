import socket, threading                                          #Libraries import
from subprocess import run
import hashlib


node_host = '127.0.0.1'
node_port = 5677

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((node_host, node_port)) 

serverName = input("inputServerName: ")



######## Server hash of itself at run time ##########
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
def write():
    while True:                                                 #message layout
        message = '{}:{}'.format(serverName, input(''))
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()
