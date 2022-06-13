inport sys ,time
def scanitall(h):
    kl=set()
    strt = (time.time())
    with open(h, rb) as wallet_file:
        wallet_file.seek(0, 2)
        num_bytes = wallet_file.tell()
        print(num_bytes)
        data = wallet_file.read()
        keylist = []
        count = 0
        for i in range(num_bytes - 32):
            wallet_file.seek(i)
            key_bytes = wallet_file.read(32)
            count = count+1
            address=key_bytes.hex()
            kl.add(address)
            sys.stdout.write(str(address)+ Progress: +str(count/num_bytes*100)+(str(strt-time.time()))+r)
            sys.stdout.flush()
    return(kl)
setofuniquetotest = scanitall(f)
