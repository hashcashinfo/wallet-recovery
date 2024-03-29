# Copyright (c) 2022-* Emre Korkmaz. (https://linkedin.com/in/in-).
# Requires Pycoin, (pip install pycoin).
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
from pycoin.symbols.btc import network as btcnet
from pycoin.symbols.doge import network as dogenet
from pycoin.symbols.ltc import network as ltcnet
wf=open('/wallet.dat','rb').read()
secset=set()
btccaddrset=set()

#will make this a function
for match in re.findall(b'(\x01\x01\x04[\x10-\x20].{34})',wf):
    key=match.hex()
    numtoread=(int.from_bytes(bytes.fromhex(str(key[6:8])),'big'))
    keyexpo=bytes.fromhex(key[8:][:numtoread*2])
    secint=(int.from_bytes(keyexpo,'big'))
    secset.add(secint)
#and this
for seci in secset:
    keyp=btcnet.keys.private(is_compressed=True,secret_exponent=seci)
    btccaddrset.add(keyp.address())
#will output progress with modular option with zero third party package dependency, cross compat with py2-3

# create a dogecoin address for the secret exponent int value.
dogeaddrset=set()
def dogefromsec(compressed,seci):
    keyp=dogenet.keys.private(is_compressed=True,secret_exponent=seci)
    return(keyp.address())
    # btccaddrset.add(keyp.address())
count=0
for seci in secset:
    count=count+1
    # keyp=dogenet.keys.private(is_compressed=True,secret_exponent=seci)
    dogeaddr = dogefromsec(True,seci)
    dogeaddrset.add(dogeaddr)
    print(str(count),end="\r")
