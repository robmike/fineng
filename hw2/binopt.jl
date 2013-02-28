## require("options")
## using OptionsMod

## price option using binomial approximation to Black-Scholes formula
function priceoption(duration, nperiods, init_price, strike,
                     volatility, rate, dividend, putorcall, americaneuro)

    if putorcall != "call" && putorcall != "put"
        error("putorcall must be either 'call' or 'put'")
    end
    call = putorcall == "call" ? 1 : -1
    if americaneuro != "european" && americaneuro != "american"
        error("putorcall must be either 'call' or 'put'")
    end
    iseuro = americaneuro == "european"

    dt = duration/nperiods
    # x = fill(strike, (1,2^nperiods))
    discount = exp(rate*dt)
    println(discount)
    # approx difference between discount and dividend
    drc = 1.0 + dt*(rate - dividend)
    up = exp(volatility*sqrt(dt))
    println(up)
    down = 1/up
    q = (exp((rate - dividend)*dt) - down)/(up-down) # risk neutral probabilities
    println(q)

    price = 0
    for i = 0:nperiods
        prob = q^i*(1-q)^(nperiods - i)
        coeff = binomial(nperiods, i)
        term = prob*coeff*max((init_price*(up^i)*down^(nperiods-i) - strike)*call, 0)
        price = price + term
    end
    return price/(discount^nperiods)
end

priceoption(0.25, 15, 100, 110, 0.3, 0.02, 0.01, "call", "american")
