# q1
netret = [6; 2; 4]/100                  # net return
riskfreeret = 0.01                      # risk net return
corr = [8.0  -2.0  4.0;
        -2  2  -2;
        4  -2  8]/10^3

function sharpeport(corr, netret, riskfreeret)
    rf = riskfreeret
    s = corr\(netret - rf)
    o = ones(size(corr)[1], 1)
    s = s/sum(s)
end

function capmslope(s, corr, netret, riskfreeret)
    shrpret = transpose(s)*netret;
    vol = sqrt(transpose(s)*corr*s) #' volatility
    slope = (shrpret - riskfreeret)/vol;
    slope
end

## quoted in xls as excess return in percent, converted here to net
## return as a fraction
estret = [-1.52; 3.71; -1.70]/100 + riskfreeret
# estret = [-0.5186; 4.7057; -0.6986];
estcorr = [0.0056 -0.0020 0.0037;
           -0.0020 0.0022 -0.0022;
           0.0037 -0.0022 0.0074];

vol = 0.05
sest = sharpeport(estcorr, estret, riskfreeret)
estslope = capmslope(sest,estcorr, estret, riskfreeret)
est = riskfreeret + estslope*vol;
round(100*est, 2)

sharpevol = sqrt(transpose(sest)*estcorr*sest);
w = vol*sest/sharpevol;
wrf = 1 - sum(w);

trueret = wrf*riskfreeret + transpose(w)*netret;
println("q2: trueret")
round(100*trueret, 2)

actslope = capmslope(corr, netret, riskfreeret)
actret = riskfreeret + actslope*vol
round(100*actret, 2)



# q4
p = 0.5
n = 15
k = 12
s = 0
for i=k:n
    s = s + binomial(n, i)*p^i*p^(n-i)
end
round(s,4)

#q5
p = 0.5
n = 15
k = 14
s = 0
for i=k:n
    s = s + binomial(n, i)*p^i*p^(n-i)
end
t = 1 - (1-s)^100
round(t, 4)

# q6
round(2/3,2)

#q7
0.5*1 + 0.5*0.5
