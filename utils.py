import numpy as np


### Helper function to calculate returns using CI ###
def calc_compound_returns(p, r, t, n=1):
    r = r / 100 if r > 1.0 else r
    value = p * ((1 + r / n) ** (n * t))
    return round(value)


##############################################


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


def calc_balances_in_retirement(initial_balance, expenses, time_period, rate_of_return):
    balances_in_retirement = [initial_balance]
    for i in range(time_period):
        # balance_in_retirement = balance_in_retirement-full_yearly_expenses[i+years_to_retire]
        if i > 0:
            balance_in_retirement = (
                balance_in_retirement * (1 + rate_of_return / 100)
            ) - expenses[i]
        balances_in_retirement.append(round(balance_in_retirement))
    return balances_in_retirement


def calc_retirement_balances_n_expenses(
    initial_corpus,
    inital_expense,
    inflation,
    returns,
    n_years_in_retire,
    ignore_first_year_expense=True,
):
    yearly_expenses = []
    yearly_balances = []


    inflation = inflation / 100 if inflation > 1.0 else inflation

    balances_in_retirement = initial_corpus

    for i in range(n_years_in_retire):

        if isinstance(returns,np.ndarray):
            corpus_returns = returns[i]
            corpus_returns = corpus_returns / 100 if corpus_returns > 1.0 else corpus_returns
        else:
            returns = returns / 100 if returns > 1.0 else returns
            corpus_returns = returns


        inflation_adjusted_expenses = calc_compound_returns(
            p=inital_expense, r=inflation, t=i
        )


        balances_in_retirement = (
            balances_in_retirement * ((1 + corpus_returns)) - inflation_adjusted_expenses
        )
        if i == 0 and ignore_first_year_expense:
            balances_in_retirement = initial_corpus

        if balances_in_retirement <= 0:
            yearly_balances.append(0)
        else:
            yearly_balances.append(balances_in_retirement)
        yearly_expenses.append(inflation_adjusted_expenses)

    return yearly_balances, yearly_expenses


def bucket_strategy_simulator(
    initial_corpus,
    inital_expense,
    inflation,
    returns,
    n_years_in_retire,
    fixed_deposit_returns,
    debt_fund_returns,
    debt_fund_volatility,
    hybrid_fund_returns,
    hybrid_fund_volatility,
    large_cap_returns,
    large_cap_volatility,
    mid_cap_returns,
    mid_cap_volatility,
    alloc_fixed,
    alloc_debt,
    alloc_hybrid,
    alloc_large_cap,
    alloc_mid_cap,
    num_simulations=1,
    ignore_first_year_expense=True
):

    balances_results = []

    for _ in range(num_simulations):

        rand_returns_debt_fund = np.random.normal(
            debt_fund_returns, debt_fund_volatility, n_years_in_retire
        )

        rand_returns_hybrid_fund = np.random.normal(
            hybrid_fund_returns, hybrid_fund_volatility, n_years_in_retire
        )

        rand_returns_large_cap_fund = np.random.normal(
            large_cap_returns, large_cap_volatility, n_years_in_retire
        )

        rand_returns_mid_cap_fund = np.random.normal(
            mid_cap_returns, mid_cap_volatility, n_years_in_retire
        )
        # inflation_rates = np.random.normal(inflation, 0.1, n_years_in_retire)
   
        yearly_expenses = []
        yearly_balances = []


        inflation = inflation / 100 if inflation > 1.0 else inflation
        fixed_deposit_returns = fixed_deposit_returns / 100 if fixed_deposit_returns > 1.0 else fixed_deposit_returns
        rand_returns_debt_fund = rand_returns_debt_fund / 100 
        rand_returns_hybrid_fund = rand_returns_hybrid_fund / 100
        rand_returns_large_cap_fund = rand_returns_large_cap_fund / 100 
        rand_returns_mid_cap_fund = rand_returns_mid_cap_fund / 100 
        print(f"{rand_returns_mid_cap_fund=}")

        
        balances_in_retirement = initial_corpus
        for i in range(n_years_in_retire):

            balances_fixed = alloc_fixed*balances_in_retirement
            balances_debt = alloc_debt*balances_in_retirement
            balances_hybrid = alloc_hybrid*balances_in_retirement
            balances_large_cap = alloc_large_cap*balances_in_retirement
            balances_mid_cap = alloc_mid_cap*balances_in_retirement

            inflation_adjusted_expenses = calc_compound_returns(
                p=inital_expense, r=inflation, t=i
            )


            balances_fixed = (balances_fixed * (1 + fixed_deposit_returns)) 
            balances_debt = (balances_debt * (1 + rand_returns_debt_fund[i])) 
            balances_hybrid = (balances_hybrid * (1 + rand_returns_hybrid_fund[i])) 
            balances_large_cap = (balances_large_cap * (1 + rand_returns_large_cap_fund[i])) 
            balances_mid_cap = (balances_mid_cap * (1 + rand_returns_mid_cap_fund[i])) 
                
            balances_in_retirement = balances_fixed+ balances_debt+  balances_hybrid+balances_large_cap +balances_mid_cap - inflation_adjusted_expenses
            
            if i == 0 and ignore_first_year_expense:
                balances_in_retirement = initial_corpus
                
            if balances_in_retirement <= 0:
                yearly_balances.append(0)
            else:
                yearly_balances.append(balances_in_retirement)
            yearly_expenses.append(inflation_adjusted_expenses)




        balances_results.append(yearly_balances)

    return balances_results, yearly_expenses
