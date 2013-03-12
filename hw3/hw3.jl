netret = [6; 2; 4]/100                  # net return
riskfreeret = 0.01                      # risk net return
corr = [8.0  -2.0  4.0;
        -2  2  -2;
        4  -2  8]/10^3

x = 1/3*[1; 1; 1]
## q1
transpose(x)*netret*100

## q2
sqrt(transpose(x)*corr*x)*100

## q3
function minvarport(corr)
    o = ones(size(corr)[1], 1)
    s = corr\o
    s = s/sum(s)
end
w = minvarport(corr)
transpose(w)*netret*100


function sharpeport(corr, netret, riskfreeret)
    rf = riskfreeret
    s = corr\(netret - rf)
    o = ones(size(corr)[1], 1)
    s = s/sum(s)
end

s = sharpeport(corr, netret, riskfreeret)
transpose(s)*netret*100

u = [3.15; 1.75; -6.39; -2.86; -6.75; -0.54; -6.75; -5.26]/100

c = [0.001/2 0.0013 -0.0006 -0.0007 0.0001 0.0001 -0.0004 -0.0004;
     0     0.0073/2 -0.0013  -0.0006 -0.0022 -0.001 0.0014 -0.0015;
     0     0      0.0599/2  0.0276 0.0635 0.0230 0.0330 0.0480;
     0     0       0      0.0296/2 0.0266 0.0215 0.0207 0.0299;
     0     0       0      0      0.1025/2 0.0427 0.0399 0.0660;
     0     0       0      0      0      0.0321/2 0.0199 0.032;
     0     0       0      0      0      0      0.0284/2 0.0351;
     0     0       0      0      0      0      0      0.0800/2]
c + transpose(c)

sharpeport(c, u)

c = [1 1 0; 1 4 0; 0 0 9];
u = [1;2;3]
sharpeport(c, u)

c = [0.01/2 0.0018 0.0011; 0 0.0109/2 0.0026; 0 0 0.0199/2]
c = transpose(c) + c
