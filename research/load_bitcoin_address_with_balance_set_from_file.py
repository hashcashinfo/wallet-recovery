import pickle
addresset=pickle.load(open("addresslist.pickleset","rb"))
len(addresset)
# %timeit print("1FeexV6bAHb8ybZjqQMjJrcCrHGW9sb6uF" in addresset)
# 1.23 µs ± 22 ns per loop (mean ± std. dev. of 7 runs, 1,000,000 loops each)
