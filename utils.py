def calc_compound_returns(p, r, t, n=1):
    r = r / 100 if r > 1.0 else r
    value = p * ((1 + r / n) ** (n * t))
    return round(value)


### Helper function to format Indian system ###
def format_to_inr(number):
    number = float(number)
    number = round(number, 2)
    is_negative = number < 0
    number = abs(number)
    s, *d = str(number).partition(".")
    r = ",".join([s[x - 2 : x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    value = "".join([r] + d)
    if is_negative:
        value = "-" + value
    return "₹ " + value


################################################
