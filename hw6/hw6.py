import random
import copy
import math
from pprint import pprint
import itertools as it
import functools as ft
import numpy as np
from scipy.optimize import fsolve, leastsq, fmin, fmin_cobyla
from numbers import Number

import pdb, sys

def info(type, value, tb):
   if hasattr(sys, 'ps1') or not sys.stderr.isatty():
      # we are in interactive mode or we don't have a tty-like
      # device, so we call the default hook
      sys.__excepthook__(type, value, tb)
   else:
      import traceback, pdb
      # we are NOT in interactive mode, print the exception...
      traceback.print_exception(type, value, tb)
      print
      # ...then start the debugger in post-mortem mode.
      pdb.pm()

sys.excepthook = info

# following function is not mine
def print_lattice(lattice, info = []):
    """
    Helper function to print lattice in a nice way."""
    levels = len(lattice[-1])
    start_date = len(lattice[0]) - 1
    dates = levels - start_date # (end_date + 1) == levels
    outlist = []
    col_widths = [0] * dates
    # Group level by level
    for j in range(levels):
        level = []
        for k in range(dates):
            try:
                point = "{:.2f}".format(lattice[k][levels - 1 - j])
                esc_width = 0 # Take care of the color escape sequence
                if info != [] and info[k][levels - 1 - j] > 0:
                    point = colored(point, 'red')
                    esc_width += 9 # len(colored('', 'red')) == 9
                level.append(point)
                col_widths[k] = max(col_widths[k], len(point) - esc_width)
            except IndexError:
                level.append('')
        outlist.append(level)

    # Prepare separator
    separator = "|-".join(['-' * w for w in col_widths])
    # Prepare format
    formats = [ ]
    for k in range(dates):
        formats.append("%%%ds" % col_widths[k])
    pattern = "  ".join(formats)
    print("\n")
    print pattern % tuple(str(start_date + time) for time in range(dates))
    print separator
    for line in outlist:
        print pattern % tuple(line)


def iterate(f, x):
    while True:
        yield x
        x = f(x)

def latticeiterate(f, init, depth=None, reverse=False):
    itr = iterate(f, init)
    if depth:
        itr = it.islice(itr, depth)
    else:
        itr = it.takewhile(lambda x: x, itr)
    out = [x for x in itr]
    if reverse:
        out.reverse()
    return out

def fupdn(x, up, dn):
    return [dn*y for y in x] + [up*x[-1]]

def felemprice(x, rl):
    def f(p,r):
        return (0.5*p)/(1+r)    # q assumed 0.5
    p = x
    r = rl[len(p) - 1]
    return [f(wl, rl) + f(wh, rh) for wl,rl,wh,rh in zip([0] + p, [0] + r, p + [0], r + [0])]

# backwards induction using risk neutral pricing
def frisknetprice(x, rl, cp=None, q=0.5):
    r = rl[len(x) - 2]
    if cp:
        c = cp[len(x) - 2]
        # pdb.set_trace()
    else:
        c = [0]*len(x)
    out = [((q*wh + (1-q)*wl)/(1+ri) + cc) for wl,wh,cc,ri in zip(x[:-1], x[1:], c, r)]
    return out

# Price defaultable bond
# Warning: coupons on not calculated correctly
def fdefaultbond(x, rl, hazrate, recrate=0.0, cp=None, q=0.5):
    r = rl[len(x) - 2]
    if cp:
        c = cp[len(x) - 2]
        # pdb.set_trace()
    else:
        c = [0]*len(x)
    hr = hazrate[len(x) - 2]
    out = [((1-hri)*(q*wh + (1-q)*wl)+hri*recrate)/(1+ri) + cc for wl,wh,cc,ri,hri in zip(x[:-1], x[1:], c, r, hr)]
    return out


def flatten(l):
    return [item for sublist in l for item in sublist] 

pl = print_lattice

def bdtlattice(a, b):
    bdt = []
    nperiod = len(a)
    for i in range(nperiod):
        period = []
        for j in range(i+1):
            period.append(a[i]*math.exp(j*b))
        bdt.append(period)
    elemp = latticeiterate(lambda x: felemprice(x, bdt), [1], nperiod+1)
    return bdt, elemp

# returns objective function for a given fixed b
def objfunc(b):
    def f(a):                   # a is a vector
        # create bdt lattice
        bdt, elemp = bdtlattice(a, b)
        bondprices = [sum(period) for period in elemp]
        spotrates = [1/(bp**(1.0/(i+1)))-1 for i,bp in enumerate(bondprices[1:])]
        return spotrates      # zero-coupon bond prices
    return f

def q1and2(b):
    # spotrates = [7.5, 7.62, 8.1, 8.45, 9.2, 9.64, 10.12, 10.45, 10.75, 11.22, 11.55, 11.92, 12.2, 12.32]
    spotrates = [3, 3.1, 3.2, 3.3, 3.4, 3.5, 3.55, 3.6, 3.65, 3.7]
    spotrates = [x/100.0 for x in spotrates]
    nperiods = len(spotrates)

    a0 = [0.05]*nperiods
    of = objfunc(b)
    ans = fsolve(lambda a: [(x-y)**2 for x, y in zip(of(a), spotrates)], a0, full_output = True)
    aopt = ans[0]
    #print aopt
    ofval = ans[1]['fvec']
    # print sum(ofval)
    shortrates, _ = bdtlattice(aopt, b)

    rf = 0.039
    strike = 0
    notional = 1e6
    couponlat = [[(r - rf)/(1+r) for r in rs] for rs in shortrates]
    swaplat = latticeiterate(lambda x: frisknetprice(x, shortrates, cp=couponlat), couponlat[-1], reverse=True)
    finoptval = [max(0, x - strike) for x in swaplat[3]]
    swaptionlat = latticeiterate(lambda x: frisknetprice(x, shortrates), finoptval, reverse=True)
    # pl(shortrates)
    # pl(couponlat)
    # pl(fwdswaplat)
    # pl(swaptionlat)
    return swaptionlat[0][0]

print("q1: %.2f" % (notional*q1and2(0.05)))
print("q2: %.2f" % (notional*q1and2(0.1)))

def q3():
    r0 = 0.05
    up = 1.1
    down = 0.9
    # q = 0.5 # assumed to be 0.5 in various parts of the code
    nperiod = 10
    r0 = 0.05
    bondprice = 100
    recrate = 0.2

    shortrates = latticeiterate(lambda x: fupdn(x, up, down), [r0], nperiod+1)
    a = 0.01
    b = 1.01
    hazrates =  [[a*(b**(j-i/2.0)) for j in range(i+1)] for i in range(nperiod+1)]
    ###elemprices = latticeiterate(lambda x: felemprice(x, shortrates), [1], nperiod+1)
    defaultlat = latticeiterate(lambda x: fdefaultbond(x, shortrates, hazrate=hazrates,
                                                       recrate=recrate),
                                [1]*(nperiods+1), reverse=True)
    return defaultlat[0][0]

print("q3: %.2f" % (bondprice*q3()))

def fdb(r, c, recrate, nperiod):
    def f(hazrate):
        hazrate = hazrate[:nperiod]
        survp = np.cumprod(1-hazrate)
        defp = np.append([1], survp[:-1])*hazrate
        ret = defp*recrate + survp*c
        ret[-1] += survp[-1]   # Return of principle in last period
        discount = 1/(1+r)**np.arange(1,nperiod+1)
        return np.dot(discount, ret)
    return f

def q4():
    r = 0.05                        # annual interest rate (with 6 month compounding)
    recrate = [0.1, 0.25, 0.5, 0.1, 0.2]
    coupon = [0.05, 0.02, 0.05, 0.05, 0.1]
    nperiod = [2*x for x in range(1,6)]
    fs = [fdb(r/2, c, rec, nper) for c,rec,nper in zip(coupon, recrate, nperiod)]

    h0 = np.linspace(0.1, 0.9, nperiod[-1])
    h0 = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99])
    h0 = 0.05*np.ones((nperiod[-1]+1,))

    bondprices = np.array([100.92, 91.56, 105.60, 98.90, 137.48])/100

    def nonneg(h):
        h = copy.deepcopy(h)
        h[h > 0] = 0
        return np.sum(h)

    def monotonic(h):
        x = h[1:] - h[:-1]
        x[x > 0] = 0
        return np.sum(x)

    hopt = fmin_cobyla(lambda hr: np.sum(([f(hr) for f in fs] - bondprices)**2), h0, [nonneg, monotonic], disp=0)
    return hopt

print("q4: %.2f" % (100*q4()[0]))

def q5():
    nperiod = 5*4                   # 5 year, quarterly CDS payments
    delta = 0.25
    recrate = 0.25                  # per annum
    hazrate = 0.01                  # 3-month hazard rate
    r = 0.05/4                      # per period
    notional = 10e6

    # Example from lecture, spread is 221.11 bps
    # nperiod = 2*4                   # 2 year, quarterly CDS payments
    # delta = 0.25
    # recrate = 0.45                  # per annum
    # hazrate = 0.01                  # 3-month hazard rate
    # r = 0.01/4                      # per period
    # notional = 1e6


    survp = (1-hazrate)**np.arange(0, nperiod+1)
    discount = 1/(1+r)**np.arange(1, nperiod+1)

    # cds par spread
    spread = (recrate - 1)*np.sum(np.diff(survp)*discount)/(0.5*delta*np.sum((survp[1:] + survp[:-1])*discount))
    print (1-recrate)*hazrate/(1-hazrate/2)*(100*100) # in bps  # why doesn't this approximation work?
    return spread
print("q5: %.2f bps" % (100*100*q5()))
