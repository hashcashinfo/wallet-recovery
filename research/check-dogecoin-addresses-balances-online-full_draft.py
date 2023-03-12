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
