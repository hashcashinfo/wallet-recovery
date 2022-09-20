'''do whatever you wish with this but do not run this program it is just for documentation'''
import bit, re, os, glob
recurse=glob.glob('/Users/em/*dat*')
pkeyre=re.compile(b'\x01\x04\x20([\x00-\xff]{32})') # this does Not find all the posisble keys, in fact any key within the curve but not at the maximum length will have padding with zeros and the start of the regex (\x20) will vary, also i shouldn't match 32 bytes... i have a solution but this is just the Standard way of matching keys for some reason. i'll upload my better performing regex patern later.
def returnF(filename): return(open(filename,'rb'))
addrdb=sqlite3.connect('/Users/em/Documents/btc-addr-bal-hashcash.db') # addr,balance.tsv indexed by the address column after importing in sqlite3.
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
