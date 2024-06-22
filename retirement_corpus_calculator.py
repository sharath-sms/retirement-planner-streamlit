import streamlit as st
import numpy as np
from datetime import datetime
import plotly.express as px
from utils import *
import pandas as pd


st.set_page_config(layout="wide")

st.title("Retirement Planner & Simulator")

# Inputs in first 2 columns
col1, col2, col3 = st.columns([0.8, 4, 2.1])

current_age = int(
    col1.number_input(
        label="Current Age",
        min_value=0,
        max_value=100,
        value=35,
        step=1,
    )
)
retire_age = int(
    col1.number_input(
        label="Retirement Age",
        min_value=current_age,
        max_value=100,
        value=60,
        step=1,
    )
)
estimated_years_retirement = int(
    col1.number_input(
        label="Estimated years in Retirement",
        min_value=0,
        max_value=100,
        value=30,
        step=1,
    )
)

current_monthly_expenses = col1.number_input(
    label="Current Monthly Expenses in Rupees",
    min_value=1000,
    max_value=1000000,
    value=50000,
    step=1000,
)
other_annual_expenses = col1.number_input(
    label="Other Annual Expenses in Rupees",
    min_value=1000,
    max_value=1000000,
    value=100000,
    step=1000,
)

overestimate_expenses = col1.number_input(
    label="Overestimate_expenses for safety by %",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=0.1,
)


inflation_before_retirement = col1.number_input(
    label="Inflation before retirement",
    min_value=0.0,
    max_value=100.0,
    value=7.0,
    step=0.1,
)
inflation_after_retirement = col1.number_input(
    label="Estimated Inflation post-retirement",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
)

net_rate_return_expected = col1.number_input(
    label="Expected Average Rate of Return for Investments before Retirement",
    min_value=0.0,
    max_value=100.0,
    value=12.0,
    step=0.1,
)
net_rate_return_expected_after_retire = col1.number_input(
    label="Expected Average Rate of Return for Investments after Retirement",
    min_value=0.0,
    max_value=100.0,
    value=6.0,
    step=0.1,
)


current_investments = col1.number_input(
    label="Current Investments", min_value=0.0, max_value=1e10, value=1e6, step=1e3
)
return_current_investments = col1.number_input(
    label="Return for Current Investments",
    min_value=0.0,
    max_value=100.0,
    value=14.0,
    step=0.1,
)

annual_increase_investments = col1.number_input(
    label="Annual Increase in Investments",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=0.1,
)

year_to_retire = retire_age - current_age


current_safe_monthly_expense = round(
    (current_monthly_expenses + (other_annual_expenses / 12))
    * (1 + overestimate_expenses / 100)
)

col2.text(
    f"Current monthly expenses (overestimated by {overestimate_expenses}% for safety) = {format_to_inr(current_safe_monthly_expense)}"
)
value_of_current_investment = calc_compound_returns(
    p=current_investments, r=return_current_investments, t=year_to_retire
)

col2.text(
    f"Value of Current Investment at Retirement (assuming same returns) = {format_to_inr(value_of_current_investment)}"
)

current_expenses_at_retirement = calc_compound_returns(
    p=(current_safe_monthly_expense * 12),
    r=inflation_before_retirement,
    t=year_to_retire,
)
col2.text(
    f"Estimated Annual Expenses at the first year of retirement = {format_to_inr(current_expenses_at_retirement)}"
)


inflation_adjusted_return = (
    (
        (1 + net_rate_return_expected_after_retire / 100)
        / (1 + inflation_after_retirement / 100)
    )
    - 1
) * 100.0
col2.text(f"{inflation_adjusted_return=}")
# future_expenses_at_retirement = round(current_expenses_at_retirement/((1+inflation_adjusted_return/100)**estimated_years_retirement))
retirement_corpus_by_year = [
    (current_expenses_at_retirement / ((1 + inflation_adjusted_return / 100) ** year))
    for year in range(1, 1 + estimated_years_retirement)
]
total_retirement_corpus = round(sum(retirement_corpus_by_year))

col2.text(
    f"Total Retirement Corpus required (based on the inputs) = {format_to_inr(total_retirement_corpus)}"
)

remaining_corpus_to_save = round(total_retirement_corpus - value_of_current_investment)
col2.text(
    f"Corpus to be accumulated (after subtracting current investment value) = {format_to_inr(remaining_corpus_to_save)}"
)

# The below was derived by-hand
step_up_returns_ratio = (1 + annual_increase_investments / 100) / (
    1 + net_rate_return_expected / 100
)
yearly_corpus = (
    remaining_corpus_to_save / ((1 + net_rate_return_expected / 100) ** year_to_retire)
) * ((step_up_returns_ratio - 1) / (step_up_returns_ratio**year_to_retire - 1))
##


full_yearly_expenses = [
    calc_compound_returns(
        p=(current_safe_monthly_expense * 12),
        r=inflation_before_retirement,
        t=i,
    )
    for i in range(year_to_retire)
] + [
    calc_compound_returns(
        p=current_expenses_at_retirement, r=inflation_after_retirement, t=i
    )
    for i in range(estimated_years_retirement)
]

amt_invested_yearly_till_retire = [
    round(yearly_corpus * (1 + annual_increase_investments/100)**i)
    for i in range(year_to_retire+1)
] + [0]*(estimated_years_retirement-1)

balances_in_retirement = []
balance_in_retirement = total_retirement_corpus

for i in range(estimated_years_retirement):
    # balance_in_retirement = balance_in_retirement-full_yearly_expenses[i+year_to_retire]
    if i>0:
        balance_in_retirement =  ((balance_in_retirement * (1 + net_rate_return_expected_after_retire/100))- full_yearly_expenses[i+year_to_retire]) 
    balances_in_retirement.append(round(balance_in_retirement))
# print(f"{balances_in_retirement=}")
yearly_sip_values=[]
yearly_sip_value = 0
for i in range(year_to_retire):
    yearly_sip_value = (yearly_sip_value+amt_invested_yearly_till_retire[i]) * (1 + net_rate_return_expected / 100)
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
    for i in range(year_to_retire)
] + balances_in_retirement


# print([((total_retirement_corpus * (1 + net_rate_return_expected_after_retire))
#         - full_yearly_expenses[i]) for i in range(year_to_retire+1, year_to_retire+estimated_years_retirement)]
# )

col2.text(
    f"Monthly investments to start now assuming yearly step-up of {annual_increase_investments}%  = {format_to_inr(yearly_corpus/12)}"
)
age = [i for i in range(current_age, retire_age + estimated_years_retirement)]
# print(len(age) , len(full_yearly_expenses), len(amt_invested_yearly_till_retire), len(yearly_corpus_value))
df_dict = dict(
    age=age,
    expenses=full_yearly_expenses,
    investment_amount=amt_invested_yearly_till_retire,
    retirement_corpus = yearly_corpus_value

)
col3.dataframe(pd.DataFrame(df_dict).set_index("age"), height=2500)

import plotly.graph_objects as go

# import numpy as np
age.append(age[-1]+1)
yearly_corpus_value.append(0)
amt_invested_yearly_till_retire.append(0)
# full_yearly_expenses.append(0)

x_axis=np.array(age)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=x_axis[:(retire_age-current_age)],
        y=np.array(yearly_corpus_value[:(retire_age-current_age)]),
        mode="lines+markers",
        name="accumulated_corpus",
    )
)


fig.add_trace(
    go.Scatter(
        x=x_axis[(retire_age-current_age):], 
        y=np.array(yearly_corpus_value[(retire_age-current_age):]), mode="lines+markers", name="remaining_retirement_corpus"
    )
)

fig.add_trace(
    go.Scatter(
        x=x_axis, 
        y=np.array(full_yearly_expenses), mode="lines+markers", name="expenses"
    )
)
fig.add_trace(
    go.Scatter(
        x=x_axis, 
        y=np.array(amt_invested_yearly_till_retire), mode="lines+markers", name="amount inve"
    )
)
fig.update_layout(
    title="Retirement Profile",
    xaxis_title="Age",
    yaxis_title="Amount",
    legend_title="Legend Title",
)
col2.plotly_chart(fig)