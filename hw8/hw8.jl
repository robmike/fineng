Pkg.add("DataFrames")
Pkg.add("Distributions")
# Pkg.add("RDatasets")
using DataFrames
# using RDdatasets
using Distributions

function logretvol(x1, expiration, nperiods)
    sqrt(nperiods/expiration)*std(log(x1[2:]./x1[1:end-1]))
end

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



function simulatehedging(prices, N, T, strike, ncontracts, rfr, vol)
    dt = T/N;
    optval = blackscholes(prices[1], strike, vol, T, rfr, 0)*ncontracts;
    stock_holdings = delta(prices[1:end-1], strike, vol, T-[0:N-1]/(N/T), rfr, 0)*ncontracts
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
end

N = 50;
T = 0.25;
ncontracts = 1e5;
rfr = 0.02;
strike = 50;
vol = 0.3;

sp = read_table("pset8.csv");            # simulated estimates of stock prices
df = read_table("pset8-1.csv");            # actual stock holdings and prices
clean_colnames!(df)

## volatility
x1 = sp[:,2];
realized_vol = round(100*logretvol(x1, T, N),2)

prices = df["Stock_Price"]
pandl = simulatehedging(prices, N, T, strike, ncontracts, rfr, vol)

for i=1:4
    realized_prices = sp[:, 1+i]
    realized_vol = 100*logretvol(realized_prices, T, N)
    pandl = pandl = simulatehedging(realized_prices, N, T, strike, ncontracts, rfr, vol)
    println()
    @printf("%i: vol = %.2f%%, p&l = %.2f\n", i, realized_vol, pandl)
end
