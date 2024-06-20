import streamlit as st
import numpy as np
from datetime import datetime
import plotly.express as px

###############################################
def format_to_inr(number):
    number = float(number)
    number = round(number,2)
    is_negative = number < 0
    number = abs(number)
    s, *d = str(number).partition(".")
    r = ",".join([s[x-2:x] for x in range(-3, -len(s), -2)][::-1] + [s[-3:]])
    value = "".join([r] + d)
    if is_negative:
       value = '-' + value
    return '₹ '+ value
################################################
st.set_page_config(layout="wide")

st.title(f"Retirement on investments calculator")

# Inputs in first 2 columns
col1, col2, col3 = st.columns([1, 3, 2])

current_age = col1.number_input(
    label="Current Age",
    min_value=0.0,
    max_value=100.0,
    value=35.0,
    step=1.0,
)
retire_age = col1.number_input(
    label="Retirement Age",
    min_value=current_age,
    max_value=100.0,
    value=60.0,
    step=1.0,
)
estimated_years_retirement = col1.number_input(
    label="Estimated years in Retirement",
    min_value=0,
    max_value=100,
    value=30,
    step=1,
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

year_to_retire = (retire_age - current_age)


current_safe_monthly_expense = round((current_monthly_expenses+(other_annual_expenses/12))*(1+overestimate_expenses/100))

col2.text(
    f"Current monthly expenses (overestimated by {overestimate_expenses}% for safety) = {format_to_inr(current_safe_monthly_expense)}"
)
value_of_current_investment = round(current_investments * (1 + return_current_investments/100)**(
    retire_age - current_age
))
col2.text(
    f"Value of Current Investment at Retirement (assuming same returns) = {format_to_inr(value_of_current_investment)}"
)

current_expenses_at_retirement=round((current_safe_monthly_expense*12)*((1+inflation_before_retirement/100)**(year_to_retire)))
col2.text(
    f"Estimated Annual Expenses at the first year of retirement = {format_to_inr(current_expenses_at_retirement)}"
)



inflation_adjusted_return = (((1+net_rate_return_expected_after_retire/100)/(1+inflation_after_retirement/100))-1)*100.
col2.text(
    f"{inflation_adjusted_return=}"
)
# future_expenses_at_retirement = round(current_expenses_at_retirement/((1+inflation_adjusted_return/100)**estimated_years_retirement))
total_retirement_corpus = round(sum([(current_expenses_at_retirement/((1+inflation_adjusted_return/100)**year)) 
                                     for year in range(1,1+estimated_years_retirement)]))

col2.text(
    f"Total Retirement Corpus required (based on the inputs) = {format_to_inr(total_retirement_corpus)}"
)

remaining_corpus_to_save = round(total_retirement_corpus-value_of_current_investment)
col2.text(
    f"Corpus to be accumulated (after subtracting current investment value) = {format_to_inr(remaining_corpus_to_save)}"
)

step_up_returns_ratio = (1+annual_increase_investments/100)/(1+net_rate_return_expected/100)
yearly_corpus = (remaining_corpus_to_save/((1+net_rate_return_expected/100)**year_to_retire))*((step_up_returns_ratio-1)/(step_up_returns_ratio**year_to_retire - 1))


col2.text(
    f"Monthly investments to start now assuming yearly step-up of {annual_increase_investments}%  = {format_to_inr(yearly_corpus/12)}"
)
