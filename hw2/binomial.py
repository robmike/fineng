
from __future__ import division
from math import exp, sqrt
from copy import deepcopy
 
def calibrate_from_blackscholes(maturity, periods, interest_rate, volatility, dividend_yield):
    """Calibrates binomial model from Black-Scholes parameters. Returns appropriate values in tuple
       (up_value, risk_neutral_q, period_interest_rate)"""
     
    period_interest_rate = exp(interest_rate * (maturity / periods))
    up_value = exp(volatility * sqrt(maturity / periods))
    down_value = 1 / up_value
    risk_neutral_q = (exp((interest_rate - dividend_yield) * (maturity / periods)) - down_value) / (up_value - down_value)
 
    return (up_value, risk_neutral_q, period_interest_rate)
 
def generate_stock_price_lattice(initial_price, up_value, down_value, periods):
    lattice = [[initial_price]]
    for n in range(periods):
        current_level = []
        for p in lattice[n]:
            current_level.append(p * down_value)
        current_level.append(lattice[n][-1] * up_value)
        lattice.append(current_level)
    return lattice
 
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
    print pattern % tuple(str(start_date + time) for time in range(dates))
    print separator
    for line in outlist:
        print pattern % tuple(line)


def print_lattice_old(lattice):
    """Helper function to print lattice in a nice way."""
    n = len(lattice)
    outlist = []
    for i in range(n):
        level = []
        for k in range(n):
            try:
                level.append(str(round(lattice[k][n-1-i],2)))
            except IndexError:
                level.append('')
        outlist.append(level)
    for line in outlist:
        print "\t".join(line)
 
 
 
def binomial_tree_run(base_lattice, risk_neutral_q, valuation_function, params):
    """Accepts valuation_function in form f(base_price, risk_neutral_q, params, connected_nodes = ())
       Valuation function must return two values: price, and additional information (as float) eg. early execution for puts.
       Returns two lattices price lattice after binomial run and additional information lattice."""
    n = len(base_lattice)
 
    final = []
    for price in base_lattice[-1]:
        final.append(valuation_function(price, risk_neutral_q, params)[0])
    result_lattice = [final]
    info_lattice = [[0 for i in range(len(base_lattice[-1]))]]
 
    for i in range(1,n):
        level = []
        info_level = []
        for k in range(len(base_lattice[n - i - 1])):
            result = valuation_function(base_lattice[n - i - 1][k], risk_neutral_q, params, (result_lattice[i - 1][k], result_lattice[i - 1][k + 1]))
            level.append(result[0])
            info_level.append(result[1])
        result_lattice.append(level)
        info_lattice.append(info_level)
 
    result_lattice.reverse()
    info_lattice.reverse()
     
    return result_lattice, info_lattice
 
def european_call(base_price, risk_neutral_q, params, connected_nodes = ()):
    if connected_nodes == ():
        value = max(0, base_price - params['strike'])
    else:
        value = ((1 - risk_neutral_q) * connected_nodes[0] + risk_neutral_q * connected_nodes[1]) * (1 / params['rate'])
    return (value, 0)
 
def european_put(base_price, risk_neutral_q, params, connected_nodes = ()):
    if connected_nodes == ():
        value = max(0, params['strike'] - base_price)
    else:
        value = ((1 - risk_neutral_q) * connected_nodes[0] + risk_neutral_q * connected_nodes[1]) * (1 / params['rate'])
    return (value, 0)
 
def american_call(base_price, risk_neutral_q, params, connected_nodes = ()):
    if connected_nodes == ():
        value = max(0, base_price - params['strike'])
        info = 0
    else:
        opt_value = ((1 - risk_neutral_q) * connected_nodes[0] + risk_neutral_q * connected_nodes[1]) * (1 / params['rate'])
        exc_value = max(0, base_price - params['strike'])
        if opt_value > exc_value:
            value = opt_value
            info = 0
        else:
            value = exc_value
            info = 1
    return (value, info)
 
def american_put(base_price, risk_neutral_q, params, connected_nodes = ()):
    if connected_nodes == ():
        value = max(0, params['strike'] - base_price)
        info = 0
    else:
        opt_value = ((1 - risk_neutral_q) * connected_nodes[0] + risk_neutral_q * connected_nodes[1]) * (1 / params['rate'])
        exc_value = max(0, params['strike'] - base_price)
        if opt_value > exc_value:
            value = opt_value
            info = 0
        else:
            value = exc_value
            info = 1
    return (value, info)
 
 
def futures(base_price, risk_neutral_q, params, connected_nodes = ()):
    if connected_nodes == ():
        value = base_price
    else:
        value = (1 - risk_neutral_q) * connected_nodes[0] + risk_neutral_q * connected_nodes[1]
    return (value, 0)
 
 
def tests():
    """Some tests from example excel spreadsheet."""
    x = calibrate_from_blackscholes(.25, 15, 0.02, 0.3, 0.01)
    # assert round(x[0], 5) == 1.04574
    # assert round(x[1], 5) == 0.49441
    # assert round(x[2], 5) == 1.00100
 
    y = calibrate_from_blackscholes(.25, 10, 0.11941, 0.23438, 0)
    assert round(y[0], 5) == 1.03775
    assert round(y[1], 5) == 0.53106
    assert round(y[2], 5) == 1.00299
 
    # #big one
    # l = generate_stock_price_lattice(100, y[0], 1/y[0], 10)
    # c = binomial_tree_run(l, y[1], european_call, {'strike': 100, 'rate': y[2]})
    # print_lattice(c[0])
 
    # #put test
    # pl = generate_stock_price_lattice(100, 1.07, 1/1.07, 3)
    # pc = binomial_tree_run(pl, 0.557, american_put, {'strike': 100, 'rate': 1.01})
    # print_lattice(pc[0])
    # print_lattice(pc[1])
 
    #futures test
    fl = generate_stock_price_lattice(100, x[0], 1/x[0], 15)
    fp = binomial_tree_run(fl, x[1], futures, {})
    print_lattice(fl)
    print_lattice(fp[0])
 
    # #option on futures
    # fo = binomial_tree_run(fp[0], x[1], european_put, {'strike': 100, 'rate': x[2]})
    # print_lattice(fo[0])
 
    #example for option on future that matures earlier than said futures
    fearly = binomial_tree_run(fp[0][0:11], x[1], american_call, {'strike': 110, 'rate': x[2]})
    print_lattice(fearly[0])
    print("---\n")
    print_lattice(fearly[1])
    print("---\n")
    print([i for i,z in enumerate(fearly[1]) if 1.0 in z])
 
    pl = generate_stock_price_lattice(100, x[0], 1/x[0], 15)
    pc = binomial_tree_run(pl, x[1], european_put, {'strike': 100, 'rate': x[2]})
    cc = binomial_tree_run(pl, x[1], european_call, {'strike': 100, 'rate': x[2]})

    # Since they are european options we only care about final value, not entire lattice
    chooser_lattice = deepcopy(pc[0][0:11])
    n = 10
    chooser_lattice[n] = [max(i,j) for i,j in zip(pc[0][n], cc[0][n])]

    fchooser = binomial_tree_run(chooser_lattice, x[1], european_call, {'strike': 0, 'rate': x[2]})
    print_lattice(pc[0])
    print_lattice(cc[0])
    print_lattice(fchooser[0])
 
def problem_set():
    pass
 
if __name__ == '__main__':
    tests()
    problem_set()

