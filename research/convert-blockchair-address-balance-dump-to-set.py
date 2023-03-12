# https://gz.blockchair.com/dogecoin/addresses/blockchair_dogecoin_addresses_latest.tsv.gz
# takes maybe 2 seconds to load all addresses to memory
addresset=set()
for line in open('./blockchair_dogecoin_addresses_latest.tsv', 'r').read().split('\n'):
    addresset.add(line.split('\t')[0])
