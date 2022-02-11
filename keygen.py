###### KEY GEN SCRIPT ##########
from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import tinyec.ec as ec


# convert pubKey thing to hex
def compress_point(point):
    return hex(point.x) + hex(point.y % 2)[2:]


def keyGen():
    
    # obviously you can change the curve values
    curve = registry.get_curve('brainpoolP256r1')
    
    privKey = secrets.randbelow(curve.field.n)
    pubKey = privKey * curve.g
    
    return privKey, pubKey
    
    
privKey, pubKey = keyGen()


pubKeyHex = compress_point(pubKey)


with open("privKey.txt", "w") as privk:
    privk.write(str(privKey))

with open("pubKey.txt", "w") as pubk:
    pubk.write(str(pubKeyHex))