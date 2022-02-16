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

import time

######### Connect to Main Node ############
node_host = '127.0.0.1'
node_port = 7899

main_node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      #socket initialization
main_node.connect((node_host, node_port))


def getServer(message):
    print("inside")
    data = message
    m = data.decode("utf-8")
    l = m.split(':')
    
    host = l[0]
    port = l[1]



    #print(host, port)
    return host, port


def receive():
    while True:                                                 #making valid connection
        try:
            #time.sleep(1)
            main_node.send("USER".encode('ascii'))
            data = main_node.recv(1024).decode('ascii')
            print(data)

            global host, port
            #host, port = getServer(data)

            #print("host: " + str(host))

            """if ping == 'PING':
                main_node.send("USER".encode('ascii'))
                message = main_node.recv(1024).decode('ascii')
            
                #getServer(message)

                global host, port

                host, port = getServer(message)

                #print(host)
                #print(port)

            else:
                message = main_node.recv(1024).decode('ascii')
                #print(message)



            global host, port

            host, port = getServer(message)
            #main_node.close()
            break"""


        except:                                                 #case on wrong ip/port details
            print("An error occured!")
            #ping = main_node.recv(1024).decode('ascii')
            #main_node.close()
            



receive()