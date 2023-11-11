# Copyright (c) 2022-* Emre Korkmaz. (https://linkedin.com/in/in-).
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
