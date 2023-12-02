import requests

def fetchAbi(contractAddress):
    abiRequest = requests.get('http://api.etherscan.io/api?module=contract&action=getabi&address='+contractAddress+'&format=raw')
    if abiRequest.ok:
        return(json.loads(abiRequest.content))
    else:
        return(json.loads([]))
