import requests,re,time,json
SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "trezorlib"})

xpublist=[]
xre=re.compile(r"([xyYzZtuUvV]pub[1-9A-HJ-NP-Za-km-z]{79,108})")
xpublist=xre.findall(open('matches.txt','r').read())
# print(xre.findall(results))
for xpub in xpublist:
    url=("https://btc1.trezor.io/api/xpub/"+xpub.split("\n")[0])
    content=(SESSION.get(url=("https://btc1.trezor.io/api/xpub/"+xpub.split("\n")[0])).content)
    if (content[:3] != b'{"p'):
        time.sleep(1)
        content=(SESSION.get(url=("https://btc1.trezor.io/api/xpub/"+xpub.split("\n")[0])).content)
    thejson=json.loads(content.decode("utf-8"))
    for k in thejson:
        if thejson['balance'] != '0':
            rejects = {'transactions','totalPages','page'}
            if k not in rejects:print(k,thejson[k])
