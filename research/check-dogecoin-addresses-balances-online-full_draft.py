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
import requests, re

def fetchaddress(address):
    return(requests.get('https://blockbook-dogecoin.binancechain.io/api/address/'+address).text)
regexes = {
'dogecoin':'^(D|A|9)[a-km-zA-HJ-NP-Z1-9]{33,34}$'
}

addresslist=open('./listtocheck.txt','r').read().split('\n')
regexdoge=re.compile(regexes['dogecoin'])
for address in addresslist:
    print(fetchaddress(address))
