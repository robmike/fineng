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

# expected number of losses
exploss = np.sum(ploss*np.arange(0,len(ploss)))
print("expected num losses: %.2f" % exploss)

# Variance
print("var: %.2f" % np.sum(ploss*(np.arange(0,len(ploss)) - exploss)**2))

# expected 0-2 tranche losses
trloss = 2*(1 - ploss[0] - ploss[1]) # 2 or more losses cases
trloss += 1*ploss[1]
print('0-2 tranche loss: %.2f' % trloss)

# range end points are inclusive
def exp_tranche_loss(beg, end):
    n = end - beg + 1
    trloss2 = n*(1 - np.sum(ploss[:end])) # 4 or more losses cases
    trloss2 += sum((np.arange(1,n))*ploss[beg:end])
    return trloss2

print("3-4 tranche loss: %.2f" % exp_tranche_loss(3,4))
print("5-20 tranche loss: %.2f" % exp_tranche_loss(5,20))
