t = 12;
## q1
principal = 400000;
r = 0.05/t;
n = 30*t;

function payment(r, n)
    r*(1+r)^n/((1+r)^n-1);
end

round(principal*payment(r,n), 2)


println("q2");
round(payment, 2)

#q2
notional = 400
r = 0.06/12;
n = 20*12;
c = 0.05/12;
t = [0:n];
cpr = 100*(0.06*t/30);
cpr[cpr.>1.0] = 1;
smm = 1 - (1-cpr).^(1/12);
monthly_payment = notional*payment(r, n);
