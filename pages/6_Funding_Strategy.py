import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Funding Strategy",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Funding Strategy")
st.markdown("Evaluate financing options and capital structures for your resort operations")

st.markdown("---")

st.subheader("Financing Options Analysis")
st.info("Compare different financing scenarios to optimize your capital structure")

# Financing scenarios
fin_col1, fin_col2, fin_col3 = st.columns(3)

with fin_col1:
    st.markdown("**All Equity**")
    equity_pct_1 = st.slider("Equity %", 0, 100, 100, key="eq1")
    debt_pct_1 = 100 - equity_pct_1
    interest_rate_1 = st.slider("Avg Interest Rate", 0.0, 12.0, 0.0, 0.1, key="ir1")

with fin_col2:
    st.markdown("**Balanced**")
    equity_pct_2 = st.slider("Equity %", 0, 100, 60, key="eq2")
    debt_pct_2 = 100 - equity_pct_2
    interest_rate_2 = st.slider("Avg Interest Rate", 0.0, 12.0, 5.5, 0.1, key="ir2")

with fin_col3:
    st.markdown("**Debt-Heavy**")
    equity_pct_3 = st.slider("Equity %", 0, 100, 30, key="eq3")
    debt_pct_3 = 100 - equity_pct_3
    interest_rate_3 = st.slider("Avg Interest Rate", 0.0, 12.0, 6.5, 0.1, key="ir3")

st.markdown("---")

st.subheader("Capital Requirement")
capital_required = st.number_input(
    "Total Capital Required ($)",
    min_value=1000000,
    value=10000000,
    step=500000,
)

st.markdown("---")

# Calculate financing scenarios
scenarios = [
    {
        "name": "All Equity",
        "equity_pct": equity_pct_1,
        "debt_pct": debt_pct_1,
        "interest_rate": interest_rate_1,
    },
    {
        "name": "Balanced",
        "equity_pct": equity_pct_2,
        "debt_pct": debt_pct_2,
        "interest_rate": interest_rate_2,
    },
    {
        "name": "Debt-Heavy",
        "equity_pct": equity_pct_3,
        "debt_pct": debt_pct_3,
        "interest_rate": interest_rate_3,
    },
]

st.subheader("Financing Comparison")

comparison_data = []
for scenario in scenarios:
    equity_amount = capital_required * (scenario["equity_pct"] / 100)
    debt_amount = capital_required * (scenario["debt_pct"] / 100)
    annual_interest = debt_amount * (scenario["interest_rate"] / 100)
    
    comparison_data.append({
        "Scenario": scenario["name"],
        "Total Capital": capital_required,
        "Equity Required": equity_amount,
        "Debt Required": debt_amount,
        "Interest Rate": scenario["interest_rate"],
        "Annual Interest Cost": annual_interest,
        "Debt/Equity Ratio": debt_amount / equity_amount if equity_amount > 0 else 0,
    })

comparison_df = pd.DataFrame(comparison_data)

# Display comparison table
display_comp = comparison_df.copy()
for col in ["Total Capital", "Equity Required", "Debt Required", "Annual Interest Cost"]:
    display_comp[col] = display_comp[col].apply(lambda x: f"${x:,.0f}")
display_comp["Interest Rate"] = display_comp["Interest Rate"].apply(lambda x: f"{x:.1f}%")
display_comp["Debt/Equity Ratio"] = display_comp["Debt/Equity Ratio"].apply(lambda x: f"{x:.2f}x")

st.dataframe(display_comp, hide_index=True, use_container_width=True)

st.markdown("---")

# Visualizations
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("Capital Structure Comparison")
    
    capital_comp = comparison_df[["Scenario", "Equity Required", "Debt Required"]].copy()
    capital_comp_melted = capital_comp.melt(
        id_vars="Scenario",
        var_name="Type",
        value_name="Amount"
    )
    
    fig_capital = px.bar(
        capital_comp_melted,
        x="Scenario",
        y="Amount",
        color="Type",
        title="Equity vs Debt by Scenario",
        barmode="stack",
    )
    st.plotly_chart(fig_capital, use_container_width=True)

with viz_col2:
    st.subheader("Annual Interest Cost")
    
    fig_interest = px.bar(
        comparison_df,
        x="Scenario",
        y="Annual Interest Cost",
        title="Annual Interest Expense by Scenario",
        color="Scenario",
    )
    st.plotly_chart(fig_interest, use_container_width=True)

st.markdown("---")

# Debt service analysis
st.subheader("Debt Service Analysis")

loan_term = st.slider("Loan Term (Years)", 1, 30, 10)
debt_amount = capital_required * (equity_pct_2 / 100)  # Use balanced scenario
interest_rate = interest_rate_2 / 100

# Calculate annual debt service using straight amortization
annual_payment = debt_amount * (interest_rate * (1 + interest_rate) ** loan_term) / ((1 + interest_rate) ** loan_term - 1)

debt_schedule = []
remaining_balance = debt_amount

for year in range(1, loan_term + 1):
    interest_payment = remaining_balance * interest_rate
    principal_payment = annual_payment - interest_payment
    remaining_balance -= principal_payment
    
    debt_schedule.append({
        "Year": year,
        "Beginning Balance": remaining_balance + principal_payment,
        "Principal Payment": principal_payment,
        "Interest Payment": interest_payment,
        "Total Payment": annual_payment,
        "Ending Balance": max(0, remaining_balance),
    })

debt_schedule_df = pd.DataFrame(debt_schedule)

st.dataframe(
    debt_schedule_df.applymap(
        lambda x: f"${x:,.0f}" if isinstance(x, (int, float)) else x
    ),
    hide_index=True,
    use_container_width=True,
)

st.markdown("---")

# Key metrics
st.subheader("Financing Summary (Balanced Scenario)")
metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

with metric_col1:
    st.metric("Annual Interest Cost", f"${comparison_df.iloc[1]['Annual Interest Cost']:,.0f}")

with metric_col2:
    st.metric("Annual Debt Service", f"${annual_payment:,.0f}")

with metric_col3:
    st.metric("Debt/Equity Ratio", f"{comparison_df.iloc[1]['Debt/Equity Ratio']:.2f}x")

with metric_col4:
    st.metric("Debt/Total Capital", f"{equity_pct_2:.0f}%")

st.info(
    "💡 **Tip**: Use this analysis alongside your operating projections to ensure debt service "
    "coverage ratio remains healthy (typically > 1.25x)."
)
