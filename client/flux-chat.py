import os
import sys
import platform
import pip
from subprocess import getoutput
import banner



check_php = getoutput("php -v")
if "not found" in check_php:
    exit("please install php \n command > sudo apt install php")

try:
    from colorama import Fore 
    import requests
    from pyngrok import ngrok
    
except ImportError:
    print("please install library \n command > python3 -m pip install -r requirments.txt")


while True:
    banner.banner()
    banner.infolist0()
    

    try:

        input1 = input(Fore.RED+" ┌─["+Fore.LIGHTGREEN_EX+"FLUX-CHAT"+Fore.BLUE+"~"+Fore.WHITE+"@HOME"+Fore.RED+"""]
 └──╼ """+Fore.WHITE+"$ ")
        
        if input1 == "1":
            banner.SendMessage()
        
        elif input1 == "2":
            banner.banner()   
            
        
        elif input1 == "3":
            banner.banner()
            

        elif input1 == "4":
            banner.banner()
           
        
        elif input1 == "5":
            banner.banner()
            banner.Settings()

        elif input1 == "6":
            print("")
            sys.exit()

        
            
    except KeyboardInterrupt:
        print("")
        sys.exit()