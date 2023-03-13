dbp= w.db_parsed
uvs=set()
for k in dbp:
    amnt=(k[:1])
    itemlen=(int.from_bytes(amnt))
    ki=(k[1:][:itemlen])
    uvs.add(ki.decode('utf-8'))
print(uvs)
# {'bestblock',
#  'bestblock_nomerkle',
#  'defaultkey',
#  'destdata',
#  'hdchain',
#  'key',
#  'keymeta',
#  'minversion',
#  'name',
#  'orderposnext',
#  'pool',
#  'purpose',
#  'tx',
#  'version'}
