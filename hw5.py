import random
import copy
from pprint import pprint
import itertools as it

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

def latticeiterate(f, init, depth=None):
    itr = iterate(f, init)
    if depth:
        return [x for x in it.islice(itr, depth)]
    else:
        takewhile(itr)

def fupdn(x, up, dn):
    return [dn*y for y in x] + [up*x[-1]]

# takes forward values and short rates zipped
def fforeq(x, rl):
    def f(p,r):
        return (0.5*p)/(1+r)
    p = x
    r = rl[len(p) - 1]
    return [f(wl, rl) + f(wh, rh) for wl,rl,wh,rh in zip([0] + p, [0] + r, p + [0], r + [0])]

up = 1.1
down = 0.9
q = 0.5

up = 1.25
down = 0.9
q = 0.5


nperiod = 10

shortrates = latticeiterate(lambda x: fupdn(x, up, down), [6.0/100], nperiod+1)
fwdrates = latticeiterate(lambda x: fforeq(x, shortrates), [1], nperiod+1)
print_lattice(shortrates)
print_lattice(fwdrates)
