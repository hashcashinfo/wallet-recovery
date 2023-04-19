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

from pycoin.symbols.btc import network as btcnet
from pycoin.symbols.doge import network as dogenet
from pycoin.symbols.ltc import network as ltcnet
import requests, re
import bit, re, os
from wcmatch import glob
recurse=glob.glob('/Users/work/**/*{dat,bak}', flags=glob.BRACE)
print(recurse)
addresset=set()
for line in open('/Users/work/Desktop/blockchair_dogecoin_addresses_latest.tsv', 'r').read().split('\n'):
    addresset.add(line.split('\t')[0])

def fetchaddress(address):
    return(requests.get('https://blockbook-dogecoin.binancechain.io/api/address/'+address).text)
regexes = {
'dogecoin':'^(D|A|9)[a-km-zA-HJ-NP-Z1-9]{33,34}$'}

regexdoge=re.compile(regexes['dogecoin'])

def findbalances(walletpath):
    wf=open(walletpath,'rb').read()
    secset=set()
    btccaddrset=set()


    #will make this a function
    print("finding the secret exponents")
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
    print('counting the secret exponents')
    for seci in secset:
        count=count+1
        # keyp=dogenet.keys.private(is_compressed=True,secret_exponent=seci)
        dogeaddr = dogefromsec(True,seci)
        dogeaddrset.add(dogeaddr)
        if count <= (len(secset)-1):
            print(str(count),end="\r")
        else:
            print(str(count), 'keys processed')
            print('doge addresses found: ',len(dogeaddrset))
    for address in dogeaddrset:
        if address in addresset:
            print('found address: ', address)
            print(fetchaddress(address))

for wallet in recurse:
    findbalances(wallet)
