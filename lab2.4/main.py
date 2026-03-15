from dsa.gost341012 import GostDSA

gost  = GostDSA()
private_key, public_key = gost.generate_key_pair()

sig = gost.sign(b'test', private_key)

print(gost.check(sig,b'test', public_key))

