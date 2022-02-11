from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt
from subprocess import run

import binascii

import socket, threading


from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import tinyec.ec as ec


# eventually this will be your public key
nickname = input("Choose your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
client.connect(('127.0.0.1', 5078))                             #connecting client to server


def receive():
    while True:                                                 #making valid connection
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICKNAME':
                client.send(nickname.encode('ascii'))
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


def write():
    while True:                                                 #message layout
        #message = '{}: {}'.format(nickname, input(''))
        message = '{}~ {}'.format(input("To: "), connector())     

        #print(message)

        #message = input()
        #print(message.encode('ascii'))
        client.send(message.encode('ascii'))


############ SENDING FUNCTIONS #######################

# initial user input 
def messageInput():
    message = str(input("Message: "))
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



def connector():

        # the pubKey is essentially the address of the other user
    with open("pubKey.txt", "r") as pubk:
        pubKeyHex = pubk.read()
        
    # get PUBLIC KEY POINT
    curve = registry.get_curve('brainpoolP256r1')
    
    pubKey = decompress_point(curve,pubKeyHex)

    message = messageInput()
    encryptedMsgS = encryptUserInput(message, pubKey)

    return encryptedMsgS




################################ SEND THROUGH SERVER #####################


######################## ENCRYPTION FUNCTIONS ############
from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import tinyec.ec as ec

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
    cmd = [ 'ipfs', 'get', uri ]
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
    
    #print(array)
    
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

def connector2(uri):

    file = ipfs(uri)
    cipher = dec(file)
    encryptedMsgS = decryptMessage(cipher)
    
    with open("privKey.txt", "r") as privK:
        privKeyHex = privK.read()

    privKey = int(privKeyHex,16)
    
    message = decrypt_ECC(encryptedMsgS, privKey)

    message = message.decode("ascii")
    
    print(message)
    
    return message





receive_thread = threading.Thread(target=receive)               #receiving multiple messages
receive_thread.start()
write_thread = threading.Thread(target=write)                   #sending messages 
write_thread.start()