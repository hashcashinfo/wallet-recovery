 python ./pywallet.py --datadir=/home/ubuntu/bitcoinbackups/ --wallet=wallet.dat --passphrase=t3mp3st --dumpwallet > dump
Traceback (most recent call last):
  File "./pywallet.py", line 5004, in <module>
    db_env = create_env(db_dir)
  File "./pywallet.py", line 1269, in create_env
    r = db_env.open(db_dir, (DB_CREATE|DB_INIT_LOCK|DB_INIT_LOG|DB_INIT_MPOOL|DB_INIT_TXN|DB_THREAD|DB_RECOVER))
bsddb.db.DBRunRecoveryError: (-30974, 'DB_RUNRECOVERY: Fatal error, run database recovery -- /home/ubuntu/bitcoinbackups/: Operation not permitted')


Means probably you just need to make the file readable and move wallet.dat into it's own folder, also don't run the pywallet in the same terminal directory.
