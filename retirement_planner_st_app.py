####
# Copyright (c) 2024 Sharath M S
####


import streamlit as st
from datetime import datetime
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from utils import *
from calculations import *

# st.set_page_config(layout="wide")

st.set_page_config(
    page_title="Retirement Planner & Simulator",
    layout="wide",
    menu_items={
        "Get help": "https://github.com/sharath-sms/retirement-planner-streamlit/issues",
        "Report a Bug": "https://github.com/sharath-sms/retirement-planner-streamlit/issues",
        "About": """Retirement Planner & Simulator

https://github.com/sharath-sms/retirement-planner-streamlit

Copyright (c) 2024 Sharath M S

""",
    },
)
# Heading

st.title("Retirement Planner & Simulator")
st.divider()


#
# About
#


def get_info():
    # based on https://github.com/LateGenXer/finance/tree/main/rtp
    return open(os.path.join(os.path.dirname(__file__), "README.md"), "rt").read()


with st.expander("General Information..."):
    st.markdown(get_info())


st.info(
    "Disclaimer: This is not investment advice! Users are urged to consult registered financial advisors for actual planning. This tool is for DIY educational purposes only. Past performance may not be representative of future results",
    icon=None,
)


# Basic Inputs
st.header("Inputs")

col1, col2, col3 = st.columns(3)


with col1:
    # Age related
    current_age = int(
        st.number_input(
            label="Current Age",
            min_value=0,
            max_value=100,
            value=35,
            step=1,
        )
    )
    # Expenses related
    current_monthly_expenses = st.number_input(
        label="Current Monthly Expenses in Rupees",
        min_value=1000,
        max_value=1000000,
        value=50000,
        step=1000,
    )
    ## Investment related
    current_investments = st.number_input(
        label="Current Investments", min_value=0.0, max_value=1e10, value=1e6, step=1e3
    )
    # Inflation related
    inflation_before_retirement = st.number_input(
        label="Inflation before retirement",
        min_value=0.0,
        max_value=100.0,
        value=7.0,
        step=0.1,
    )

    ## Returns related
    net_rate_return_expected = st.number_input(
        label="Expected Average Rate of Return for Investments before Retirement",
        min_value=0.0,
        max_value=100.0,
        value=12.0,
        step=0.1,
    )


with col2:
    # Age related
    retire_age = int(
        st.number_input(
            label="Retirement Age",
            min_value=current_age,
            max_value=100,
            value=60,
            step=1,
        )
    )
    # Expenses related
    other_annual_expenses = st.number_input(
        label="Other Annual Expenses in Rupees",
        min_value=1000,
        max_value=1000000,
        value=100000,
        step=1000,
    )
    ## Investment related
    return_current_investments = st.number_input(
        label="Return for Current Investments",
        min_value=0.0,
        max_value=100.0,
        value=14.0,
        step=0.1,
    )
    # Inflation related
    inflation_after_retirement = st.number_input(
        label="Estimated Inflation post-retirement",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
    )
    ## Returns related
    net_rate_return_expected_after_retire = st.number_input(
        label="Expected Average Rate of Return for Investments after Retirement",
        min_value=0.0,
        max_value=100.0,
        value=6.0,
        step=0.1,
    )


with col3:
    # Age related
    estimated_years_retirement = int(
        st.number_input(
            label="Estimated years in Retirement",
            min_value=0,
            max_value=100,
            value=40,
            step=1,
        )
    )
    # Expenses related
    overestimate_expenses = st.number_input(
        label="Overestimate_expenses for safety by %",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
    )
    ## Investment related
    annual_increase_investments = st.number_input(
        label="Annual Increase in Investments",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=0.1,
    )


# Calculations
(
    current_safe_monthly_expense,
    value_of_current_investment,
    current_expenses_at_retirement,
    total_retirement_corpus,
    remaining_corpus_to_save,
    yearly_corpus,
) = calc_specific_values_on_input(
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
)
##


###########################################################################################3
st.divider()
st.header("Results obtained from the calcutations based on Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label=f"Current monthly expenses (overestimated by {overestimate_expenses}% for safety)",
        value=f"{format_to_inr(current_safe_monthly_expense)}",
    )
    st.metric(
        label=f"Value of Current Investment at Retirement (assuming same returns)",
        value=f"{format_to_inr(value_of_current_investment)}",
    )


with col2:
    st.metric(
        label=f"Estimated Annual Expenses at the first year of retirement",
        value=f"{format_to_inr(current_expenses_at_retirement)}",
    )
    st.metric(
        label=f"Corpus to be accumulated (after subtracting current investment value)",
        value=f"{format_to_inr(remaining_corpus_to_save)}",
    )

with col3:
    st.metric(
        label=f"Total Retirement Corpus required (based on the inputs)",
        value=f"{format_to_inr(total_retirement_corpus)}",
    )
    st.metric(
        label=f"Monthly investments to start now assuming yearly step-up of {annual_increase_investments}%",
        value=f"{format_to_inr((yearly_corpus/12))}",
    )


#####################################################################


st.divider()
df_dict = calculate_yearly_values(
    current_age=current_age,
    retire_age=retire_age,
    estimated_years_retirement=estimated_years_retirement,
    current_investments=current_investments,
    inflation_before_retirement=inflation_before_retirement,
    inflation_after_retirement=inflation_after_retirement,
    return_current_investments=return_current_investments,
    net_rate_return_expected=net_rate_return_expected,
    net_rate_return_expected_after_retire=net_rate_return_expected_after_retire,
    annual_increase_investments=annual_increase_investments,
    current_safe_monthly_expense=current_safe_monthly_expense,
    current_expenses_at_retirement=current_expenses_at_retirement,
    total_retirement_corpus=total_retirement_corpus,
    yearly_corpus=yearly_corpus,
)

st.header("Graphical and Tabular Results Depiction")
col1, col2, col3 = st.columns([5.5, 0.5, 3])

col3.dataframe(pd.DataFrame(df_dict).set_index("age"))  # , height=2500)


age = df_dict["age"]
yearly_corpus_value = df_dict["retirement_corpus"]
amt_invested_yearly_till_retire = df_dict["investment_amount"]
full_yearly_expenses = df_dict["expenses"]

age.append(age[-1] + 1)
yearly_corpus_value.append(0)
amt_invested_yearly_till_retire.append(0)


x_axis = np.array(age)

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=x_axis[: (retire_age - current_age)],
        y=np.array(yearly_corpus_value[: (retire_age - current_age)]),
        mode="lines+markers",
        name="Accumulated Corpus",
    )
)


fig.add_trace(
    go.Scatter(
        x=x_axis[(retire_age - current_age) :],
        y=np.array(yearly_corpus_value[(retire_age - current_age) :]),
        mode="lines+markers",
        line={"color": "teal"},
        name="Remaining Retirement Corpus",
    )
)

fig.add_trace(
    go.Scatter(
        x=x_axis,
        y=np.array(full_yearly_expenses),
        mode="lines+markers",
        line={"color": "red"},
        name="Expenses",
    )
)
fig.add_trace(
    go.Scatter(
        x=x_axis,
        y=np.array(amt_invested_yearly_till_retire),
        mode="lines+markers",
        line={"color": "pink"},
        name="Amount Invested",
    )
)
fig.update_layout(
    title="Retirement Portfolio Profile",
    xaxis_title="Age",
    yaxis_title="Amount",
    legend_title="Legend Title",
)
col1.plotly_chart(fig)


#####
############################################################################################################################################
#### Simulations
st.divider()
st.header("Simulations")

col1, col_1_2, col2, col3 = st.columns([1.5, 0.5, 1, 1])

with col1:
    assumed_retirement_corpus = st.number_input(
        label="Enter the corpus amount that you can invest for retirement or think will fund your retirment",
        min_value=0.0,
        max_value=1e10,
        value=1e8,
        step=1e5,
    )
with col2:
    if total_retirement_corpus > assumed_retirement_corpus:
        st.metric(
            label=f"This is lesser than the required retirement corpus by",
            value=f"{format_to_inr(total_retirement_corpus-assumed_retirement_corpus)}",
        )
    else:
        st.write(
            "The corpus is more than sufficcient for retirement based on your expenses and other factors provided"
        )

balances_assumed_corpus, yearly_expenses_in_retirement = (
    calc_retirement_balances_n_expenses(
        initial_corpus=assumed_retirement_corpus,
        inital_expense=current_expenses_at_retirement,
        inflation=inflation_after_retirement,
        returns=net_rate_return_expected_after_retire,
        n_years_in_retire=estimated_years_retirement,
    )
)

lasting_years = sum(np.array(balances_assumed_corpus) > 0)

with col3:
    if total_retirement_corpus > assumed_retirement_corpus:

        st.metric(
            label=f"Based on the expenses, this corpus will last",
            value=f"{lasting_years} years",
        )
    else:
        st.write(
            f"The corpus is likely to last more than {estimated_years_retirement} years based on your expenses and other factors provided"
        )


tab1, tab2 = st.tabs(
    [
        "Results based on the newly entered retirement corpus ",
        "Simulation using the Bucket Strategy",
    ]
)

with tab1:

    col1, col2, col3 = st.columns([5.5, 0.5, 3])

    with col1:
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(balances_assumed_corpus),
                mode="lines+markers",
                line={"color": "teal"},
                name="Remaining Retirement corpus",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(yearly_expenses_in_retirement),
                mode="lines+markers",
                line={"color": "red"},
                name="Expenses",
            )
        )

        fig.update_layout(
            title="Retirement Profile for the Entered Corpus Amount",
            xaxis_title="Age",
            yaxis_title="Amount",
            legend_title="Legend Title",
        )
        st.plotly_chart(fig)

    with col3:

        st.dataframe(
            pd.DataFrame(
                dict(
                    age=range(retire_age, retire_age + estimated_years_retirement),
                    expenses=yearly_expenses_in_retirement,
                    retirement_corpus=np.round(balances_assumed_corpus),
                )
            ).set_index("age")
        )


with tab2:

    st.info(
        "Note: Change the defaults for various types of funds in the sidebar if you wish to",
        icon=None,
    )

    with st.sidebar:
        st.header(
            "Default Assumptions for overall Returns and Volatility (used for Simulations)"
        )

        fixed_deposit_returns = st.number_input(
            "% Return for Fixed Deposits/Instruments ",
            min_value=0.0,
            max_value=100.0,
            value=8.0,
            step=0.1,
        )

        debt_fund_returns = st.number_input(
            "% Return for Debt Instruments/Funds ",
            min_value=0.0,
            max_value=100.0,
            value=9.0,
            step=0.1,
        )
        debt_fund_volatility = st.number_input(
            "% Volatility for Debt Instruments/Funds ",
            min_value=0.0,
            max_value=100.0,
            value=3.0,
            step=0.1,
        )

        hybrid_fund_returns = st.number_input(
            "% Return for Hybrid Instruments/Funds ",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.1,
        )
        hybrid_fund_volatility = st.number_input(
            "% Volatility for Hybrid Instruments/Funds ",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.1,
        )

        large_cap_returns = st.number_input(
            "% Return for Large Cap Funds ",
            min_value=0.0,
            max_value=100.0,
            value=12.0,
            step=0.1,
        )
        large_cap_volatility = st.number_input(
            "% Volatility for Large Cap Funds",
            min_value=0.0,
            max_value=100.0,
            value=20.0,
            step=0.1,
        )

        mid_cap_returns = st.number_input(
            "% Return for Small-Mid Cap Funds ",
            min_value=0.0,
            max_value=100.0,
            value=15.0,
            step=0.1,
        )
        mid_cap_volatility = st.number_input(
            "% Volatility for Small-Mid  Cap Funds",
            min_value=0.0,
            max_value=100.0,
            value=30.0,
            step=0.1,
        )

        alloc_fixed = (
            st.number_input(
                "% Allocation for Fixed Deposits/Instruments ",
                min_value=0.0,
                max_value=100.0,
                value=50.0,
                step=0.1,
            )
            / 100
        )
        alloc_debt = (
            st.number_input(
                "% Allocation for Debt Instruments/Funds ",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.1,
            )
            / 100
        )
        alloc_hybrid = (
            st.number_input(
                "% Allocation for Hybrid Instruments/Funds ",
                min_value=0.0,
                max_value=100.0,
                value=20.0,
                step=0.1,
            )
            / 100
        )
        alloc_large_cap = (
            st.number_input(
                "% Allocation for  Large Cap Funds ",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.1,
            )
            / 100
        )
        alloc_mid_cap = (
            st.number_input(
                "% Allocation for  Small-Mid Cap Funds ",
                min_value=0.0,
                max_value=100.0,
                value=10.0,
                step=0.1,
            )
            / 100
        )

        num_simulations = int(
            st.number_input(
                "Number of times you want to run simulations",
                min_value=1,
                max_value=1000,
                value=10,
                step=1,
            )
        )
        ########## Stop of sidebar Inputs

    balances_results, expenses = bucket_strategy_simulator(
        initial_corpus=assumed_retirement_corpus,
        inital_expense=current_expenses_at_retirement,
        inflation=inflation_after_retirement,
        returns=net_rate_return_expected_after_retire,
        n_years_in_retire=estimated_years_retirement,
        fixed_deposit_returns=fixed_deposit_returns,
        debt_fund_returns=debt_fund_returns,
        debt_fund_volatility=debt_fund_volatility,
        hybrid_fund_returns=hybrid_fund_returns,
        hybrid_fund_volatility=hybrid_fund_volatility,
        large_cap_returns=large_cap_returns,
        large_cap_volatility=large_cap_volatility,
        mid_cap_returns=mid_cap_returns,
        mid_cap_volatility=mid_cap_volatility,
        alloc_fixed=alloc_fixed,
        alloc_debt=alloc_debt,
        alloc_hybrid=alloc_hybrid,
        alloc_large_cap=alloc_large_cap,
        alloc_mid_cap=alloc_mid_cap,
        num_simulations=num_simulations,
    )

    balances_results = np.array(balances_results)
    mean_retirement_balance_simulation = np.median(balances_results, axis=0)
    success_rate_bucket_strategy = (
        np.sum((balances_results[:, -1] > 0)) / num_simulations * 100
    )

    col1, col2, col3 = st.columns([5.5, 0.5, 3])

    with col1:

        st.metric(
            label=f"Success rate for the entered retirement corpus based on the bucket strategy and based on the expenses",
            value=f"{success_rate_bucket_strategy} %",
        )
        fig = go.Figure()

        # fig.add_trace(
        #     go.Scatter(
        #         x=x_axis[(retire_age - current_age) :],
        #         y=np.array(balances_assumed_corpus),
        #         mode="lines+markers",
        #         name="Retirement corpus (based on previous calculations)",
        #     )
        # )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(yearly_expenses_in_retirement),
                mode="lines+markers",
                line={"color": "red"},
                name="Expenses",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=mean_retirement_balance_simulation,
                mode="lines+markers",
                line={"color": "teal"},
                name="Mean Corpus from Bucket Strategy",
            )
        )

        fig.update_layout(
            title="Retirement Portfolio Profile Simulations based on the Bucket Strategy",
            xaxis_title="Age",
            yaxis_title="Amount",
            legend_title="Legend Title",
        )

        for i in range(num_simulations):

            fig.add_trace(
                go.Scatter(
                    x=x_axis[(retire_age - current_age) :],
                    y=np.array(balances_results[i]),
                    mode="lines",
                    opacity=0.3,
                    showlegend=False,
                )
            )

        st.plotly_chart(fig)

    with col3:
        st.metric(
            label=f"Using the bucket strategy, this corpus may likely last",
            value=f"{np.sum(mean_retirement_balance_simulation>0)} years",
        )
        st.dataframe(
            pd.DataFrame(
                dict(
                    age=range(retire_age, retire_age + estimated_years_retirement),
                    expenses=yearly_expenses_in_retirement,
                    retirement_corpus=np.round(mean_retirement_balance_simulation),
                )
            ).set_index("age")
        )


#################################################################################################################################################
st.divider()
st.subheader("Simulation using Percentage Rule")
tab1, tab2 = st.tabs(
    [
        "Results based on the Percentage Rule ",
        "Simulation using the Bucket Strategy on Corpus obtained from the Percentage Rule ",
    ]
)
with tab1:

    col1, col2 = st.columns(2)

    with col1:
        #
        st.subheader("Simulations using 3% Rule ")

        retirement_corpus_3_pct_rule = 100 / 3 * current_expenses_at_retirement

        st.metric(
            label=f"Based on Expenses at the start of retirement {format_to_inr(current_expenses_at_retirement)} & based on the 3% rule, you would require ",
            value=f"{format_to_inr(round(retirement_corpus_3_pct_rule))}",
        )

        balances_3_pct_corpus, yearly_expenses_in_retirement = (
            calc_retirement_balances_n_expenses(
                initial_corpus=retirement_corpus_3_pct_rule,
                inital_expense=current_expenses_at_retirement,
                inflation=inflation_after_retirement,
                returns=net_rate_return_expected_after_retire,
                n_years_in_retire=estimated_years_retirement,
            )
        )

        lasting_years_3_pct = sum(np.array(balances_3_pct_corpus) > 0)

        if total_retirement_corpus > retirement_corpus_3_pct_rule:

            st.metric(
                label=f"Based on the expenses and 3% Withdrawal Rule, this corpus will last",
                value=f"{lasting_years_3_pct} years",
            )
        else:
            st.write(
                f"The corpus is likely to last more than {estimated_years_retirement} years based on your expenses and other factors provided"
            )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(balances_3_pct_corpus),
                mode="lines+markers",
                line={"color": "teal"},
                name="Remaining Retirement corpus",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(yearly_expenses_in_retirement),
                mode="lines+markers",
                line={"color": "red"},
                name="Expenses",
            )
        )

        fig.update_layout(
            title="Retirement Profile based on Amount Obtained from 3 % Rule",
            xaxis_title="Age",
            yaxis_title="Amount",
            legend_title="Legend Title",
        )
        st.plotly_chart(fig)

    with col2:
        #
        st.subheader("Simulations using 4% Rule ")

        retirement_corpus_4_pct_rule = 100 / 4 * current_expenses_at_retirement

        st.metric(
            label=f"Based on Expenses at the start of retirement {format_to_inr(current_expenses_at_retirement)} & based on the 4% rule, you would require ",
            value=f"{format_to_inr(round(retirement_corpus_4_pct_rule))}",
        )

        balances_4_pct_corpus, yearly_expenses_in_retirement = (
            calc_retirement_balances_n_expenses(
                initial_corpus=retirement_corpus_4_pct_rule,
                inital_expense=current_expenses_at_retirement,
                inflation=inflation_after_retirement,
                returns=net_rate_return_expected_after_retire,
                n_years_in_retire=estimated_years_retirement,
            )
        )

        lasting_years_4_pct = sum(np.array(balances_4_pct_corpus) > 0)

        if total_retirement_corpus > retirement_corpus_4_pct_rule:

            st.metric(
                label=f"Based on the expenses and 4% Withdrawal Rule, this corpus will last",
                value=f"{lasting_years_4_pct} years",
            )
        else:
            st.write(
                f"The corpus is likely to last more than {estimated_years_retirement} years based on your expenses and other factors provided"
            )

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(balances_4_pct_corpus),
                mode="lines+markers",
                line={"color": "teal"},
                name="Remaining Retirement corpus",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(yearly_expenses_in_retirement),
                mode="lines+markers",
                line={"color": "red"},
                name="Expenses",
            )
        )

        fig.update_layout(
            title="Retirement Profile based on Amount Obtained from 3 % Rule",
            xaxis_title="Age",
            yaxis_title="Amount",
            legend_title="Legend Title",
        )
        st.plotly_chart(fig)


with tab2:

    col1, col2 = st.columns(2)

    with col1:
        bucket_results_3pct, expenses = bucket_strategy_simulator(
            initial_corpus=retirement_corpus_3_pct_rule,
            inital_expense=current_expenses_at_retirement,
            inflation=inflation_after_retirement,
            returns=net_rate_return_expected_after_retire,
            n_years_in_retire=estimated_years_retirement,
            fixed_deposit_returns=fixed_deposit_returns,
            debt_fund_returns=debt_fund_returns,
            debt_fund_volatility=debt_fund_volatility,
            hybrid_fund_returns=hybrid_fund_returns,
            hybrid_fund_volatility=hybrid_fund_volatility,
            large_cap_returns=large_cap_returns,
            large_cap_volatility=large_cap_volatility,
            mid_cap_returns=mid_cap_returns,
            mid_cap_volatility=mid_cap_volatility,
            alloc_fixed=alloc_fixed,
            alloc_debt=alloc_debt,
            alloc_hybrid=alloc_hybrid,
            alloc_large_cap=alloc_large_cap,
            alloc_mid_cap=alloc_mid_cap,
            num_simulations=num_simulations,
        )

        bucket_results_3pct = np.array(bucket_results_3pct)
        mean_retirement_balance_simulation_3pct = np.median(bucket_results_3pct, axis=0)
        success_rate_bucket_strategy_3pct = (
            np.sum((bucket_results_3pct[:, -1] > 0)) / num_simulations * 100
        )

        st.metric(
            label=f"Success rate for the corpus obtained from 3% rule based on the bucket strategy and based on the expenses",
            value=f"{success_rate_bucket_strategy_3pct} %",
        )
        fig = go.Figure()

        # fig.add_trace(
        #     go.Scatter(
        #         x=x_axis[(retire_age - current_age) :],
        #         y=np.array(balances_assumed_corpus),
        #         mode="lines+markers",
        #         name="Retirement corpus (based on previous calculations)",
        #     )
        # )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(yearly_expenses_in_retirement),
                mode="lines+markers",
                line={"color": "red"},
                name="Expenses",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=mean_retirement_balance_simulation_3pct,
                mode="lines+markers",
                line={"color": "teal"},
                name="Mean Corpus from Bucket Strategy",
            )
        )

        fig.update_layout(
            title="Retirement Portfolio Profile Simulations based on the Bucket Strategy for 3% Rule",
            xaxis_title="Age",
            yaxis_title="Amount",
            legend_title="Legend Title",
        )

        for i in range(num_simulations):

            fig.add_trace(
                go.Scatter(
                    x=x_axis[(retire_age - current_age) :],
                    y=np.array(bucket_results_3pct[i]),
                    mode="lines",
                    opacity=0.3,
                    showlegend=False,
                )
            )

        st.plotly_chart(fig)

    with col2:
        bucket_results_4pct, expenses = bucket_strategy_simulator(
            initial_corpus=retirement_corpus_4_pct_rule,
            inital_expense=current_expenses_at_retirement,
            inflation=inflation_after_retirement,
            returns=net_rate_return_expected_after_retire,
            n_years_in_retire=estimated_years_retirement,
            fixed_deposit_returns=fixed_deposit_returns,
            debt_fund_returns=debt_fund_returns,
            debt_fund_volatility=debt_fund_volatility,
            hybrid_fund_returns=hybrid_fund_returns,
            hybrid_fund_volatility=hybrid_fund_volatility,
            large_cap_returns=large_cap_returns,
            large_cap_volatility=large_cap_volatility,
            mid_cap_returns=mid_cap_returns,
            mid_cap_volatility=mid_cap_volatility,
            alloc_fixed=alloc_fixed,
            alloc_debt=alloc_debt,
            alloc_hybrid=alloc_hybrid,
            alloc_large_cap=alloc_large_cap,
            alloc_mid_cap=alloc_mid_cap,
            num_simulations=num_simulations,
        )

        bucket_results_4pct = np.array(bucket_results_4pct)
        mean_retirement_balance_simulation_4pct = np.median(bucket_results_4pct, axis=0)
        success_rate_bucket_strategy_4pct = (
            np.sum((bucket_results_4pct[:, -1] > 0)) / num_simulations * 100
        )

        st.metric(
            label=f"Success rate for the corpus obtained from 4% rule based on the bucket strategy and based on the expenses",
            value=f"{success_rate_bucket_strategy_4pct} %",
        )
        fig = go.Figure()

        # fig.add_trace(
        #     go.Scatter(
        #         x=x_axis[(retire_age - current_age) :],
        #         y=np.array(balances_assumed_corpus),
        #         mode="lines+markers",
        #         name="Retirement corpus (based on previous calculations)",
        #     )
        # )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=np.array(yearly_expenses_in_retirement),
                mode="lines+markers",
                line={"color": "red"},
                name="Expenses",
            )
        )

        fig.add_trace(
            go.Scatter(
                x=x_axis[(retire_age - current_age) :],
                y=mean_retirement_balance_simulation_4pct,
                mode="lines+markers",
                line={"color": "teal"},
                name="Mean Corpus from Bucket Strategy",
            )
        )

        fig.update_layout(
            title="Retirement Portfolio Profile Simulations based on the Bucket Strategy for 4% Rule",
            xaxis_title="Age",
            yaxis_title="Amount",
            legend_title="Legend Title",
        )

        for i in range(num_simulations):

            fig.add_trace(
                go.Scatter(
                    x=x_axis[(retire_age - current_age) :],
                    y=np.array(bucket_results_4pct[i]),
                    mode="lines",
                    opacity=0.3,
                    showlegend=False,
                )
            )

        st.plotly_chart(fig)
