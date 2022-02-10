from ecies.utils import generate_eth_key, generate_key
from ecies import encrypt, decrypt

eth_k = generate_eth_key()
sk_hex = eth_k.to_hex()  # hex string
pk_hex = eth_k.public_key.to_hex() 

keys = {
    "eth_k" : eth_k,
    "sk_hex" :  sk_hex,
    "pk_hex" : pk_hex
}

with open("sk_hex.txt", "w") as pk:
    pk.write(sk_hex)

with open("pk_hex.txt", "w") as pk:
    pk.write(pk_hex)

print(sk_hex)
print(pk_hex)