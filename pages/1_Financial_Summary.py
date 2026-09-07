import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Financial Summary",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Financial Summary")
st.markdown("Overview of key financial metrics and performance indicators")

# Initialize session state for data
if "demand_data" not in st.session_state:
    st.session_state.demand_data = None
if "revenue_data" not in st.session_state:
    st.session_state.revenue_data = None
if "expense_data" not in st.session_state:
    st.session_state.expense_data = None

st.markdown("---")

# Display current metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Projected Annual Visitors",
        "250,000",
        "+5.2%",
        delta_color="normal"
    )

with col2:
    st.metric(
        "Total Revenue",
        "$25.0M",
        "+12.3%",
        delta_color="normal"
    )

with col3:
    st.metric(
        "Operating Expenses",
        "$18.2M",
        "+8.1%",
        delta_color="inverse"
    )

with col4:
    st.metric(
        "EBITDA",
        "$6.8M",
        "+18.5%",
        delta_color="normal"
    )

st.markdown("---")

# Revenue breakdown
st.subheader("Revenue Mix")
revenue_categories = {
    "Ticket Sales": 12500000,
    "F&B": 4200000,
    "Retail": 2800000,
    "Rentals": 2100000,
    "Ski School": 1800000,
    "Summer Activities": 1200000,
    "Snowplay & Winter Ops": 400000,
    "Other Revenue": 200000,
}

rev_col1, rev_col2 = st.columns(2)

with rev_col1:
    rev_df = pd.DataFrame(
        list(revenue_categories.items()),
        columns=["Category", "Amount"]
    )
    st.bar_chart(rev_df.set_index("Category"))

with rev_col2:
    st.dataframe(
        rev_df.assign(
            Percent=lambda x: (x["Amount"] / x["Amount"].sum() * 100).round(1).astype(str) + "%"
        ),
        hide_index=True,
        use_container_width=True,
    )

st.markdown("---")

# Expense breakdown
st.subheader("Expense Categories")
expense_categories = {
    "Direct Labor": 4500000,
    "Payroll Taxes / Benefits": 1350000,
    "Cost of Goods Sold": 3200000,
    "Electric Power / Fuel / Utilities": 1800000,
    "Maintenance / Repairs": 1200000,
    "G&A": 1100000,
    "Insurance": 900000,
    "Marketing / Advertising": 600000,
    "Property / Other Taxes": 450000,
    "Miscellaneous": 250000,
    "Other Direct": 150000,
}

exp_col1, exp_col2 = st.columns(2)

with exp_col1:
    exp_df = pd.DataFrame(
        list(expense_categories.items()),
        columns=["Category", "Amount"]
    )
    st.bar_chart(exp_df.set_index("Category"))

with exp_col2:
    st.dataframe(
        exp_df.assign(
            Percent=lambda x: (x["Amount"] / x["Amount"].sum() * 100).round(1).astype(str) + "%"
        ),
        hide_index=True,
        use_container_width=True,
    )

st.markdown("---")

# Key ratios
st.subheader("Key Financial Ratios")
ratio_col1, ratio_col2, ratio_col3, ratio_col4 = st.columns(4)

with ratio_col1:
    st.metric("EBITDA Margin", "27.2%")

with ratio_col2:
    st.metric("Operating Margin", "18.5%")

with ratio_col3:
    st.metric("Revenue per Visitor", "$100.00")

with ratio_col4:
    st.metric("Cost per Visitor", "$72.80")

st.markdown("---")

# Summary table
st.subheader("Financial Summary (12-Month Projection)")
summary_data = {
    "Metric": [
        "Total Revenue",
        "Cost of Goods Sold",
        "Gross Profit",
        "Gross Margin %",
        "Operating Expenses",
        "EBITDA",
        "EBITDA Margin %",
        "Taxes & Other",
        "Net Income",
        "Net Margin %",
    ],
    "Amount": [
        "$25,200,000",
        "$3,200,000",
        "$22,000,000",
        "87.3%",
        "$15,400,000",
        "$6,600,000",
        "26.2%",
        "$1,320,000",
        "$5,280,000",
        "20.9%",
    ],
}

summary_df = pd.DataFrame(summary_data)
st.dataframe(summary_df, hide_index=True, use_container_width=True)

st.info(
    "💡 **Note**: These are placeholder values. Update the Demand Forecast, Revenue Forecast, "
    "and Expense Forecast pages to see live calculations reflected here."
)
