# Copyright (c) 2022-* Emre Korkmaz. 
# You can find me on linkedin.com via this link (https://linkedin.com/in/in-).
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

# Let's import only what we need, no third party scripts for maximum compatibility and less chance of security risks.

import re,sys,os
kmre=re.compile(b'\x07keymeta!([\x02|\x03][\x00-\xFF].{32})')
secre=re.compile(b'(\x01\x01\x04[\x10-\x20].{34})')

def extractPrivKeys(filebinary):
    # Below is a Set to store Unique items, in this case this is the potential 'private keys'.
    secset=set()
    # Let's do a search using the regex pattern i made, this patern also finds keys that are smaller than 32 bytes
    # this finds more keys than most tools i have used such as pywallet.
    # but when dumping old wallet's i noticed some wallet's can have 
    for match in secre.findall(filebinary):
        key=match.hex()
        numtoread=(int.from_bytes(bytes.fromhex(str(key[6:8])),'big'))
        keyexpo=bytes.fromhex(key[8:][:numtoread*2])
        secint=(int.from_bytes(keyexpo,'big'))
        secset.add(secint)
    # Below we return the Set of potential 'private keys'
    return(secset)

def extractKeyMetas(filebinary):
    # Below is a Set to store Unique items, in this case this is the potential 'public keys'.
    kmetaset=set()
    # Let's do a search using the regex pattern i made, this patern also finds keys that begin with keymeta.
    for match in kmre.findall(filebinary):
        key=match.hex()
        kmetaset.add(secint)
    # Below we return the Set of potential 'private keys'
    return(kmetaset)


wallet_filename = sys.argv[1]
prog = os.path.basename(sys.argv[0])
print('checking ',wallet_filename)
if len(sys.argv) != 2 or sys.argv[1].startswith("-"):
    print("usage:", prog, "wallet file", file=sys.stderr)
    sys.exit(2)

walletbinary=open(wallet_filename,'rb').read()
keymetas=extractKeyMetas(walletbinary)
secrets=extractPrivKeys(walletbinary)
print('there are potentially ',len(keymetas),' Keymetas and ', len(secrets),' Private Keys in this wallet')
