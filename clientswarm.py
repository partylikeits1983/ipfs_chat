from subprocess import run
import socket, threading
import binascii

from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii

import tinyec.ec as ec
from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

from time import gmtime, strftime

from colorama import Fore

import os




######### Connect to Main Node ############
node_host = '127.0.0.1'
node_port = 8977

main_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
main_node.connect((node_host, node_port))


def getServer(message):
    data = message
    m = data.decode("utf-8")
    l = m.split(':')
    
    host = l[0]
    port = l[1]

    print(host, port)
    return host, port


def receive():

    main_node.send("USER".encode('ascii'))

    while True:                                                 #making valid connection
        try:
            #main_node.send("USER".encode('ascii'))

            message = main_node.recv(1024).decode('ascii')

            if message == 'NICKNAME':
                main_node.send("USER".encode('ascii'))
                print("nick")
            else:
                global host, port

                host, port = getServer(message)
                main_node.close()
                break


        except:                                                 #case on wrong ip/port details
            #print("An error occured!")
            main_node.close()
            




receive()






################ CONNECTION SETTINGS #################

"""host = '127.0.0.1'                                                      #LocalHost
port = 7989"""

# eventually this will be your public key
"""with open("username.txt", "r") as userN:
    username = userN.read()"""


username = input("your username: ")



client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect((host, port))                             #connecting client to server


################## APPEND MESSAGES TO ARRAY ################

messages = []

############ SENDING FUNCTIONS #######################

# initial user input 
def messageInput():
    message = str(input(""))
    return message
    

def encryptUserInput(message, pubKey):
    msg = message.encode("ascii")
    
    # in the future users can choose which curve
    curve = registry.get_curve('brainpoolP256r1')
    
    encryptedMsg = encrypt_ECC(msg, pubKey)

    # put encryptedMsg in dictionary
    encryptedMsgDic = {
    'ciphertext': binascii.hexlify(encryptedMsg[0]),
    'nonce': binascii.hexlify(encryptedMsg[1]),
    'authTag': binascii.hexlify(encryptedMsg[2]),
    'x': hex(encryptedMsg[3].x),
    'y': hex(encryptedMsg[3].y)
    }
    # convert all vals in encryptedMsgDic to str
    a = str(encryptedMsgDic["ciphertext"])
    b = str(encryptedMsgDic["nonce"])
    c = str(encryptedMsgDic["authTag"])
    d = str(encryptedMsgDic["x"])
    e = str(encryptedMsgDic["y"])

    encryptedMsgDicStr = {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
        'e': e
    }
    
    # convert encryptedMsgDicStr to string with : as separation of vals
    cipherstr = ''
    for i in encryptedMsgDicStr:
        cipherstr += encryptedMsgDicStr[i] + ' : '

    #encode cipherstr and send it  
    m = cipherstr.encode("ascii")
    
    return m


def time():
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    return time



def connector():

    # the pubKey is essentially the address of the other user
    with open("pubKey.txt", "r") as pubk:
        pubKeyHex = pubk.read()
        
    # get PUBLIC KEY POINT
    curve = registry.get_curve('brainpoolP256r1')
    
    pubKey = decompress_point(curve,pubKeyHex)

    message = f"[{time()} User: {username}] {messageInput()}"



    encryptedMsgS = encryptUserInput(message, pubKey)

    return encryptedMsgS



################################ SEND THROUGH SERVER #####################


######################## ENCRYPTION FUNCTIONS #######################

def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)


def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext


def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()


def encrypt_ECC(msg, pubKey):
    curve = registry.get_curve('brainpoolP256r1')
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)


def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext


# compress x and y values to hex
def compress_point(point):
    pubKeyHex = hex(point.x) + hex(point.y)
    return pubKeyHex


# convert pubKeyHex to ec.Point
def decompress_point(curve, pubKeyHex):
    n = 0
    x = ""
    y = ""

    l = len(str(pubKeyHex))
    length = l/2
    
    for i in pubKeyHex:
        if n < length:
            x+=i
        else:
            y+=i     
        n+=1
        
    x = int(x,16)
    y = int(y,16)
    
    p = ec.Point(curve,x,y)
    
    return p



########### DOWNLOAD IPFS AND DECRYPT ##############

### download from IPFS
def ipfs(uri):
    path = "URIs/"
    cmd = [ 'ipfs', 'get', uri, f"--output={path}{uri}"]
    out = run(cmd, capture_output=True).stdout
    output = out.decode("utf-8")
    outputs = output.split(" ")
    file = outputs[3]
    file = file.rstrip()
    return file
    

# opening file
def dec(file):
    with open(file, 'rb') as file:
        cipher = file.read()
        return cipher


# rebuild data structure
def decryptMessage(m):
    d = m.decode("ascii")
    
    array = d.split(': ')
    
    #a = array[0].replace("\\", "")
    
    a = array[0].strip()
    a = eval(a)
    ciphertext = binascii.unhexlify(a)

    b = array[1].strip()
    b = eval(b)
    nonce = binascii.unhexlify(b)

    c = array[2].strip()
    c = eval(c)
    authTag = binascii.unhexlify(c)

    x = array[3].strip()
    y = array[4].strip()
    
    # convert x,y to int 
    x = int(x,16)
    y = int(y,16)
    
    curve = registry.get_curve('brainpoolP256r1')
    
    p = ec.Point(curve,x,y)
    
    array = [ciphertext, nonce, authTag, p]
    
    encryptedMsgS = tuple(array)
    
    return encryptedMsgS



# what is the best way to have a function like this?
def connector2(uri):

    file = ipfs(uri)
    cipher = dec(file)
    encryptedMsgS = decryptMessage(cipher)
    
    with open("privKey.txt", "r") as privK:
        privKeyHex = privK.read()

    privKey = int(privKeyHex,16)
    
    message = decrypt_ECC(encryptedMsgS, privKey)

    message = message.decode("ascii")
    
    #messages.append(message)

    print(message)

    #
    # print(messages)


    
    #return message



########################## MAIN HANDLER FUNCTIONS ############################
# recieve and write are both threaded

def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(username.encode('ascii'))
            else:
                #print(message)
                
                try:
                    connector2(message)
                except:
                    print("")

        except:                                                 #case on wrong ip/port details
            #print("An error occured!")
            #client.close()
            break



def sendMessage():
    global userTo
    userTo = input("User Address: ")
    write_thread = threading.Thread(target=write)                   #sending messages 
    write_thread.start()


def write():
    while True:                                                 #message layout
        #message = '{}: {}'.format(nickname, input(''))
        #message = '{}~ {}'.format(input("To: "), connector())
        message = '{}~ {}'.format(userTo, connector())    

        #print(message)

        #message = input()
        #print(message.encode('ascii'))
        client.send(message.encode('ascii'))



# starting threads
receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()


sendMessage()