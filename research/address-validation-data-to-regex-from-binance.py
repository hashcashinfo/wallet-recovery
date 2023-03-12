# pip install python-binance
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
#incomplete but i just need a useful regex
client = Client("apikey", "secret") 

coininfo = client.get_all_coins_info()
for coin in coininfo:
   for network in (coin['networkList']):
       print(coin['name'],network['addressRegex'])
