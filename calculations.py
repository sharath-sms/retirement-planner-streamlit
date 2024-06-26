import numpy as np
from utils import *


def calculate_yearly_values(
    current_age,
    retire_age,
    estimated_years_retirement,
    current_investments,
    inflation_before_retirement,
    inflation_after_retirement,
    return_current_investments,
    net_rate_return_expected,
    net_rate_return_expected_after_retire,
    annual_increase_investments,
    current_safe_monthly_expense,
    current_expenses_at_retirement,
    total_retirement_corpus,
    yearly_corpus,
):

    years_to_retire = round(retire_age - current_age)

    balances_in_retirement, yearly_expenses_in_retirement = (
        calc_retirement_balances_n_expenses(
            initial_corpus=total_retirement_corpus,
            inital_expense=current_expenses_at_retirement,
            inflation=inflation_after_retirement,
            returns=net_rate_return_expected_after_retire,
            n_years_in_retire=estimated_years_retirement,
        )
    )
    full_yearly_expenses = [
        calc_compound_returns(
            p=(current_safe_monthly_expense * 12),
            r=inflation_before_retirement,
            t=i,
        )
        for i in range(years_to_retire)
    ] + yearly_expenses_in_retirement

    amt_invested_yearly_till_retire = [
        round(yearly_corpus * (1 + annual_increase_investments / 100) ** i)
        for i in range(years_to_retire + 1)
    ] + [0] * (estimated_years_retirement - 1)

    yearly_sip_values = []
    yearly_sip_value = 0
    for i in range(years_to_retire):
        yearly_sip_value = (yearly_sip_value + amt_invested_yearly_till_retire[i]) * (
            1 + net_rate_return_expected / 100
        )
        yearly_sip_values.append(yearly_sip_value)

    yearly_corpus_value = [
        round(
            (
                calc_compound_returns(
                    p=current_investments, r=return_current_investments, t=i
                )
            )
            + yearly_sip_values[i]
        )
        for i in range(years_to_retire)
    ] + balances_in_retirement

    age = [i for i in range(current_age, retire_age + estimated_years_retirement)]

    return dict(
        age=age,
        expenses=full_yearly_expenses,
        investment_amount=amt_invested_yearly_till_retire,
        retirement_corpus=yearly_corpus_value,
    )


def calc_specific_values_on_input(
    current_age,
    retire_age,
    estimated_years_retirement,
    current_monthly_expenses,
    other_annual_expenses,
    overestimate_expenses,
    current_investments,
    inflation_before_retirement,
    inflation_after_retirement,
    return_current_investments,
    net_rate_return_expected,
    net_rate_return_expected_after_retire,
    annual_increase_investments,
):
    years_to_retire = round(retire_age - current_age)

    current_safe_monthly_expense = round(
        (current_monthly_expenses + (other_annual_expenses / 12))
        * (1 + overestimate_expenses / 100)
    )

    value_of_current_investment = calc_compound_returns(
        p=current_investments, r=return_current_investments, t=years_to_retire
    )

    current_expenses_at_retirement = calc_compound_returns(
        p=(current_safe_monthly_expense * 12),
        r=inflation_before_retirement,
        t=years_to_retire,
    )

    inflation_adjusted_return = (
        (
            (1 + net_rate_return_expected_after_retire / 100)
            / (1 + inflation_after_retirement / 100)
        )
        - 1
    ) * 100.0
    retirement_corpus_by_year = [
        (
            current_expenses_at_retirement
            / ((1 + inflation_adjusted_return / 100) ** year)
        )
        for year in range(1, 1 + estimated_years_retirement)
    ]
    total_retirement_corpus = round(sum(retirement_corpus_by_year))

    # The below was derived by-hand
    step_up_returns_ratio = (1 + annual_increase_investments / 100) / (
        1 + net_rate_return_expected / 100
    )

    remaining_corpus_to_save = round(
        total_retirement_corpus - value_of_current_investment
    )

    yearly_corpus = (
        remaining_corpus_to_save
        / ((1 + net_rate_return_expected / 100) ** years_to_retire)
    ) * ((step_up_returns_ratio - 1) / (step_up_returns_ratio**years_to_retire - 1))

    return (
        current_safe_monthly_expense,
        value_of_current_investment,
        current_expenses_at_retirement,
        total_retirement_corpus,
        remaining_corpus_to_save,
        yearly_corpus,
    )


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