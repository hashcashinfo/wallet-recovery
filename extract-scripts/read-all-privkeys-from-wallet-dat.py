'''Return the correct number of keys in the wallet file, checks how many bytes to read. dirty code but works'''


import re
from pycoin.symbols.ltc import network as ltcnet
wf=open('./wallet.dat','rv').read()
for match in re.findall(b'(\x01\x01\x04[\x1e-\x20].{34})',wf):
    key=match.hex()
    numtoread=(int.from_bytes(bytes.fromhex(str(key[6:8])),'big'))
    keyexpo=bytes.fromhex(key[8:][:numtoread*2])
    secint=(int.from_bytes(keyexpo,'big'))
    keyp=ltcnet.keys.private(is_compressed=True,secret_exponent=secint)
    print(keyp.address())