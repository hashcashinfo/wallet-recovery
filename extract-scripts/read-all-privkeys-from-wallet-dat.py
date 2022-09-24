'''Return the correct number of keys in the wallet file, checks how many bytes to read. dirty code but works'''


import re
wf=open('./wallet.dat','rv').read()
for match in re.findall(b'(\x01\x01\x04[\x1e-\x20].{34})',wf):
    key=match.hex()
    numtoread=(int.from_bytes(bytes.fromhex(str(key[6:8])),'big'))
    print(key[8:][:numtoread*2])
