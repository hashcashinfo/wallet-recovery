# Download the file "blockchair_bitcoin_addresses_and_balance_LATEST.tsv.gz" from the following source:
# "List of all funded Bitcoin addresses" available on http://addresses.loyce.club/
# After downloading, uncompress the .gz file using a tool like gzip or tar to extract the .tsv file.
# This .tsv file contains a tab-separated list of Bitcoin addresses and their balances.

import pickle
address_balances = {}  # Use a dictionary to store addresses and balances
addressbalancetsv = "blockchair_bitcoin_addresses_and_balance_LATEST.tsv"
fileoutput = "addresslist_balances_bitcoin.pickle"
count = 0
countdone = 0

# Get the total number of lines in the file
numoflines = len(open(addressbalancetsv).readlines())

# Read the TSV file line by line
with open(addressbalancetsv, 'r') as infile:
    for line in infile:
        countdone += 1
        parts = line.strip().split('\t')
        if len(parts) < 2:
            continue  # Skip invalid lines
        addr, balance = parts[0], parts[1]
        if addr[0] == '1':  # Example: Only include addresses starting with '1'
            count += 1
            address_balances[addr] = float(balance)  # Store address and balance
        # Print progress
        print(
            f"{count} addresses processed out of {numoflines} lines ({countdone / numoflines * 100:.2f}%)",
            end='\r'
        )

# Save the dictionary to a pickle file
with open(fileoutput, 'wb') as outputfile:
    pickle.dump(address_balances, outputfile)

print(f"\nTotal addresses with balances stored: {len(address_balances)}")

# Should output something like this:
# python3 convert_blockchair_addresses_to_pickle.py 
# 22380161 addresses processed out of 54702784 lines (100.00%)
# Total addresses with balances stored: 22380161
