Pkg.add("DataFrames")
# Pkg.add("RDatasets")
using DataFrames
# using RDdatasets
Pkg.add("Distributions")
using Distributions

sp = read_table("pset8.csv");            # simulated estimates of stock prices
N = 50;
T = 0.25;
## volatility
x1 = sp[:,2];
vol = round(100*sqrt(N/T)*std(log(x1[2:]./x1[1:end-1])),2)

df = read_table("pset8-1.csv");            # actual stock holdings and prices

function blackscholes(price, strike, sd, expiration, riskfree_rate, coupon_rate)
    d1 = log(price/strike) + (riskfree_rate - coupon_rate + sd^2/2)*expiration;
    d1 = d1./(sd*sqrt(expiration));
    d2 = d1 - sd*sqrt(expiration)
    price.*exp(-coupon_rate*expiration).*cdf(Normal(0, 1), d1) -
    strike*exp(-riskfree_rate*expiration).*cdf(Normal(0, 1), d2)
end

function delta(price, strike, sd, expiration, riskfree_rate, coupon_rate)
    d1 = log(price/strike) + (riskfree_rate - coupon_rate + sd^2/2)*expiration;
    d1 = d1./(sd*sqrt(expiration));
    # println(d1)
    # d2 = d1 - sd*sqrt(expiration)
    exp(-coupon_rate*expiration).*cdf(Normal(0, 1), d1);
end

x1

clean_colnames!(df)

ncontracts = 1e5;
rfr = 0.02;
T = 0.25;                                # expiration
nperiods = 50;
dt = T/nperiods;
strike = 50;
prices = df["Stock_Price"]
optval = blackscholes(prices[1], strike, 0.3, 0.25, rfr, 0)*ncontracts;
stock_holdings = delta(prices[1:end-1], strike, 0.3, 0.25-[0:49]/200, rfr, 0)*ncontracts
stock_val = prices[1:end-1].*stock_holdings
cash = zeros(length(stock_val),)
portval = zeros(length(stock_val),)
cash[1] = optval - stock_val[1]         # value of hedging portfolio
portval[1] = optval
for i = 1:(length(stock_val)-1)
    portval[i+1] = cash[i]*exp(rfr*dt) + prices[i+1]*stock_holdings[i];
    cash[i+1] = portval[i+1] - prices[i+1]*stock_holdings[i+1];
end

## Note that length of prices is one longer than cash and
## stock_holdings so "end" does not refer to the same period
finalportval = cash[end]*exp(rfr*dt) + prices[end]*stock_holdings[end];
finaloptval = ncontracts*max(0, prices[end] - strike);

pandl = finalportval - finaloptval;
