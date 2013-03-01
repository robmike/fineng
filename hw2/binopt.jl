## require("options")
## using OptionsMod

## price option using binomial approximation to Black-Scholes formula
function priceoption(duration, nperiods, init_price, strike,
                     volatility, rate, dividend, putorcall, americaneuro)

    if putorcall != "call" && putorcall != "put"
        error("putorcall must be either 'call' or 'put'")
    end
    iscall = putorcall == "call"
    call = iscall ? 1 : -1
    if americaneuro != "european" && americaneuro != "american"
        error("putorcall must be either 'call' or 'put'")
    end
    isamerican = americaneuro == "american"

    dt = duration/nperiods
    # x = fill(strike, (1,2^nperiods))
    discount = exp(rate*dt)
    # approx difference between discount and dividend
    drc = 1.0 + dt*(rate - dividend)
    up = exp(volatility*sqrt(dt))
    down = 1/up
    q = (exp((rate - dividend)*dt) - down)/(up-down) # risk neutral probabilities

    price = 0
    term = zeros(2,nperiods+1)          # value of security and value of option
    for i = 0:nperiods
        prob = q^i*(1-q)^(nperiods - i)
        coeff = binomial(nperiods, i)
        term[1,i+1] = init_price*(up^i)*down^(nperiods-i) # security val
        term[2,i+1] = max((term[1,i+1] - strike)*call, 0) # option val
        price = price + prob*coeff*term[2,i+1]
    end
    if !isamerican # FIXME: If not paying dividend we can do this even for american call
        return price/discount^nperiods
    end
    ## american
    earliest = nperiods
    for i = nperiods:-1:1
        for j = 1:i
            optionval = ((1-q)*term[2,j] + q*term[2,j+1])/discount
            secval = term[1,j]*up
            term[1,j] = secval
            term[2,j] = max(optionval, (secval - strike)*call)
            if term[2,j] > optionval    # exercised
                earliest = i-1
            end
        end
        #println(term[:,1:i])
    end
    return term[2, 1], earliest
end


# test case
# priceoption(0.25, 10, 100, 100, 0.23438, 0.11941, 0.00, "put", "european") # 3.165
# priceoption(1, 3, 100, 100, 0.11719, 0.029851, 0.00, "put", "american") # 3.82

#q1
priceoption(0.25, 15, 100, 110, 0.3, 0.02, 0.01, "call", "american") # 2.6040

#q2
priceoption(0.25, 15, 100, 110, 0.3, 0.02, 0.01, "put", "american")
#priceoption(0.25, 15, 100, 110, 0.3, 0.02, 0.01, "put", "european")
