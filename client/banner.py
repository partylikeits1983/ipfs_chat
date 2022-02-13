import os
from colorama import Fore
import time
import sys
import json
from subprocess import Popen

import client



def banner():
    os.system("clear")
    print("")
    Popen('neofetch')
    time.sleep(2)


def infolist0():
    time.sleep(0.1)
    print(Fore.RED+" ["+Fore.WHITE+"*"+Fore.RED+"]"+Fore.CYAN+" Choose one of the options below \n")
    time.sleep(0.1)
    print(Fore.RED+" [1]"+Fore.WHITE+" Send Message\n")
    time.sleep(0.1)
    print(Fore.RED+" [2]"+Fore.WHITE+" Check Inbox\n") 
    time.sleep(0.1)
    print(Fore.RED+" [3]"+Fore.WHITE+" Generate new keys \n") 
    time.sleep(0.1)
    print(Fore.RED+" [5]"+Fore.WHITE+" Settings \n")
    time.sleep(0.1)
    print(Fore.RED+" [6]"+Fore.WHITE+" Exit . . .\n")




def SendMessage():
    os.system("clear")

    print(Fore.RED+" ["+Fore.WHITE+"*"+Fore.RED+"]"+Fore.CYAN+" input user address \n")
    time.sleep(0.1)

    client.sendMessage()







  
def Settings():
    print(Fore.WHITE+" [+]"+Fore.GREEN+" Please Enter NGROK Token  > ngrok.com\n")
    
    try:

        ngrok_key = input(Fore.RED+" ┌─["+Fore.LIGHTGREEN_EX+"FLUX-CHAT"+Fore.BLUE+"~"+Fore.WHITE+"@HOME"+Fore.GREEN+"/SETTINGS"+Fore.RED+"""]
 └──╼ """+Fore.WHITE+"$ ")  
        with open("config.json") as json_file:
            json_key = json.load(json_file)
            json_key['ngrok'] = ngrok_key

        with open("config.json","w") as json_file:
            json_key = json.dump(json_key,json_file)
        input(Fore.LIGHTRED_EX+" [*]  Back To Menu (Press Enter...) ")
    except:
        print("")
        print("\n")
        sys.exit()