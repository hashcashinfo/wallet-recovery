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
# https://gz.blockchair.com/dogecoin/addresses/blockchair_dogecoin_addresses_latest.tsv.gz
# takes maybe 2 seconds to load all addresses to memory
import pickle
addressset=set()
addressbalancetsv="blockchair_bitcoin_addresses_and_balance_LATEST.tsv"
fileoutput="addresslist.pickleset"
count=0
countdone=0
numoflines = len(open(addressbalancetsv).readlines())
for line in open(addressbalancetsv, 'r').read().split('\n'):
    addr=line.split('\t')[0]
    countdone=countdone+1
    if (line[0]) == '1':
        count=count+1
        addressset.add(addr)
        print(str(count),str(numoflines),str(countdone),(countdone/numoflines*100),'%% complete',end='\r')
with open(fileoutput,'wb') as outputfile: pickle.dump(addressset,outputfile)


print(len(addressset))
