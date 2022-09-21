'''Extract keys from the file, keys 657461210384 is keymeta...'''
import subprocess,re
filedump = subprocess.getoutput('db_dump -p /Users/em/recovered_wallet_1528294850.dat')
