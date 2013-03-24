
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
