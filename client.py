from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
from subprocess import run

import binascii

import socket, threading

nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('127.0.0.1', 5055))                             #connecting client to server

def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
            else:
                #ipfs(message)
                print(message)
                
        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            #client.close()
            break


def write():
    while True:                                                 #message layout
        #message = '{}: {}'.format(nickname, input(''))
        message = '{}: {}'.format(input("To: "), cipherText(input("Message: ")))
        #message = input()
        print(message.encode('ascii'))
        client.send(message.encode('ascii'))


# encrypting when sending
def cipherText(message):
    with open('pk_hex.txt', 'r') as file:
        pk_hex = file.read().replace('\n', '')

    data = str.encode(message)
    m = encrypt(pk_hex, data)
    bcipher = binascii.hexlify(m)
    cipher = bcipher.decode('ascii')

    return cipher


# downloading uri from IPFS
def ipfs(uri):
    cmd = [ 'ipfs', 'get', uri ]
    out = run(cmd, capture_output=True).stdout
    output = out.decode("utf-8")
    outputs = output.split(" ")
    file = outputs[3]
    file = file.rstrip()
    dec(file)
    
# decrypting message in file
def dec(file):
    with open(file, 'rb') as file:
        cipher = file.read()
    
    with open('sk_hex.txt', 'r') as file:
        secret_key = file.read().replace('\n', '')

    text = decrypt(secret_key, cipher).decode("utf-8")
    print(text)


receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()