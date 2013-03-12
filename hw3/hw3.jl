netret = [6; 2; 4]/100                  # net return
riskfreeret = 0.01                      # risk net return
corr = [8.0  -2.0  4.0;
        -2  2  -2;
        4  -2  8]/10^3

x = 1/3*[1; 1; 1]
## q1
println("q1")
transpose(x)*netret*100

## q2
println("q2")
sqrt(transpose(x)*corr*x)*100

## q3
println("q3");
function minvarport(corr)
    o = ones(size(corr)[1], 1)
    s = corr\o
    s = s/sum(s)
end
w = minvarport(corr)
transpose(w)*netret*100

## q4
println("q4")
function sharpeport(corr, netret, riskfreeret)
    rf = riskfreeret
    s = corr\(netret - rf)
    o = ones(size(corr)[1], 1)
    s = s/sum(s)
end

s = sharpeport(corr, netret, riskfreeret)
shrpret = transpose(s)*netret
shrpret*100

## q5
println("q5")
vol = sqrt(s'*corr*s) #' volatility
vol*100

## q6
println("q6")
slope = (shrpret - riskfreeret)/vol     # capital market line slope

## q7
## best return for volatility of 5 percent
println("q7")
invol = 0.05
outret = riskfreeret + slope*invol
100*outret
