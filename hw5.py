import random
import copy
from pprint import pprint
import itertools as it
import functools as ft

import pdb, sys

# debug shit (from stackexchange)
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

# takes forward values and short rates zipped
def felemprice(x, rl):
    def f(p,r):
        return (0.5*p)/(1+r)    # q assumed 0.5
    p = x
    r = rl[len(p) - 1]
    return [f(wl, rl) + f(wh, rh) for wl,rl,wh,rh in zip([0] + p, [0] + r, p + [0], r + [0])]

# backwards induction using risk neutral pricing
def frisknetprice(x, rl, q=0.5):
    r = rl[len(x) - 2]
    return [(q*wl + (1-q)*wh)/(1+ri) for wl,wh,ri in zip(x[:-1], x[1:], r)]

pl = print_lattice

up = 1.1
down = 0.9
# q = 0.5 # assumed to be 0.5 in various parts of the code
nperiod = 10
r0 = 0.05
bondprice = 100

# up = 1.25
# down = 0.9
# r0 = 0.06
# nperiod = 6
# bondprice = 110
# q = 0.5

shortrates = latticeiterate(lambda x: fupdn(x, up, down), [r0], nperiod+1)
elemprices = latticeiterate(lambda x: felemprice(x, shortrates), [1], nperiod+1)
print_lattice(shortrates)
print_lattice(elemprices)

# q1
print("\n")
print("q1")
print("%.2f" % (sum(elemprices[10])*bondprice)) # 61.62

# q2
print("\n")
print("q2")

bond4lat = latticeiterate(lambda x: frisknetprice(x, shortrates), (4+1)*[bondprice])[::-1]
bond10lat = latticeiterate(lambda x: frisknetprice(x, shortrates), (nperiod+1)*[bondprice])[::-1]
# for zero-coupon fwdplat and bond10lat are the same for the periods they overlap
fwdlat = latticeiterate(lambda x: frisknetprice(x, shortrates), bond10lat[4])[::-1]
# print_lattice(fwdlat)
# print_lattice(bond4lat)
# print_lattice(bond10lat)
# print("%.2f" % (100*fwdlat[0][0]/bond4lat[0][0]))           # this works but
print("%.2f" % (100*sum(elemprices[-1])/sum(elemprices[4])))  # this is easier
# sum(elemprices[-1]) coincides with risk-neutral expected value of
# forward at time zero because it is equal to risk-neutral expected
# value of bond10lat[4] (backwards induction is the same)

# q3

print("\n")
print("q2")
# not the best way to do this
zeroshortrates = latticeiterate(lambda x: [0]*(len(x)+1), [0], nperiod + 1)
futlat = latticeiterate(lambda x: frisknetprice(x, zeroshortrates), bond10lat[4], reverse=True)
pl(futlat)
