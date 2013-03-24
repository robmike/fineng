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

## q3
loss = [-1.1168; -1.3565; 1.3754; -1.0396; 0.5662; -0.0050; -1.9092;
1.1039; -0.2332; -0.6678; -1.3045; 0.8229; 0.9616; -0.9685; 1.0631;
-2.8888; 0.6022; 1.1204; -0.9511; 0.0810; -0.8619; 0.0685; -0.2053;
0.9565; 0.1795; -2.4565; -0.0656; -0.1942; 0.3471; -0.2564; 1.2923;
-0.3045; 0.4619; -1.8819; -1.1397; 1.9877; -0.0960; 1.0440; -0.2722;
-0.0218; 0.8140; 1.9191; 2.1450; -0.3924; 0.8846; -2.0569; -0.8699;
-0.4551; -0.5114; -0.0412; 0.2515; -0.6077; 1.8807; -0.2756; -1.2639;
-1.4916; -0.9395; 2.3707; -0.2759; -0.7360];

loss = sort(loss);

## Var
p = 0.9
n = int(ceil(length(loss)*p));
round(loss[n],2)

## q4 CVar
cvar = sum(loss[n:])/(length(loss)*(1-p));
round(cvar,2)

# q5
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
