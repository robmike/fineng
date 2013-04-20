Pkg.add("DataFrames")
# Pkg.add("RDatasets")
using DataFrames
# using RDdatasets
Pkg.add("Distributions")
using Distributions

sp = read_table("pset8.csv");            # simulated estimates of stock prices

N = 50
T = 0.25
## volatility
x1 = sp[:,2]
vol = round(100*sqrt(N/T)*std(log(x1[2:]./x1[1:end-1])),2)

df = read_table("pset8-1.csv");            # actual stock holdings and prices

function delta(price, strike, sd, expiration, riskfree_rate, coupon_rate)
    d1 = log(price/strike) + (riskfree_rate - coupon_rate + sd^2/2)*expiration
    d1 = d1./(sd*sqrt(expiration))
    println(d1)
    # d2 = d1 - sd*sqrt(expiration)
    exp(-coupon_rate*expiration).*cdf(Normal(0, 1), d1)
end

x1

clean_colnames!(df)
prices = df["Stock_Price"]
delta(prices[1:end-1], 50, 0.3, 0.25-[0:49]/200, 0.02, 0)*1e5


z = [-0.99
-3.08
-0.50
0.38
1.51
0.42
0.82
1.83
-0.46
1.75
1.23
1.06
1.29
-1.86
1.58
-3.15
-1.46
3.49
1.93
-1.65
-1.92
-1.53
3.05
-1.39
-1.40
1.19
0.89
1.58
1.48
-1.07
1.97
1.22
2.66
-1.63
-0.80
0.27
-0.80
-1.77
0.41
0.69
-2.31
-3.29
0.72
2.08
0.75
-0.41
-1.90
-0.04
4.08
1.55]
