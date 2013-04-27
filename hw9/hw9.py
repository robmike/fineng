import pandas as pd
import numpy as np

pdefault = pd.read_csv('pset9.csv').values

ploss = np.zeros((len(pdefault),))
ploss[0] = 1.0;
for pdefi in pdefault:
    for j in range(i,0,-1):     # from i down to 1
        # probability of j losses in the first i credits is equal to j
        # defaults in first i-1 credits and ith credit default plus
        # j-1 defaults in first i-1 credits plus j defaults
        ploss[j] = ploss[j]*(1-pdefi) + ploss[j-1]*pdefi
    ploss[0] = ploss[0]*(1-pdefi)
    print ploss
    # import pdb
    # pdb.set_trace()

print("%.3f" % ploss[3])
