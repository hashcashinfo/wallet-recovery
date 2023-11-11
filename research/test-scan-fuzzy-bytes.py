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
# '''do whatever you wish with this but do not run this program it is just for documentation'''
# wget http://addresses.loyce.club/blockchair_bitcoin_addresses_and_balance_LATEST.tsv.gz
import bit, re, os, glob
recurse=glob.glob('/Users/em/*dat*')
# this does Not find all the posisble keys, 
# in fact any key within the curve but not at the maximum length will have padding with zeros and the start of the regex 
# (\x20) will vary, also i shouldn't match 32 bytes... 
# i have a solution but this is just the Standard way of matching keys for some reason. 
# i'll upload my better performing regex patern later.

pkeyre=re.compile(b'\x01\x04\x20([\x00-\xff]{32})') 
def returnF(filename): return(open(filename,'rb'))
# addr,balance.tsv indexed by the address column after importing in sqlite3.
addrdb=sqlite3.connect('/Users/em/Documents/btc-addr-bal-hashcash.db') 
pubkeycollection=set()

for filepath in recurse:
    try:
        results=(pkeyre.findall(returnF(filepath).read()))
        print('found',str(len(results)),'private keys @ ',filepath)
        counter=0
        for counter in range(0,len(results)):
            thiskey=getKey(results[counter])
            pubkey=(thiskey.public_key.hex())
            pubkeycollection.add(pubkey)
            counter=counter+1
    except: continue
