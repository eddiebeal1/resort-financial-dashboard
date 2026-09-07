import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Expense Forecast",
    page_icon="💸",
    layout="wide",
)

st.title("💸 Expense Forecast")
st.markdown("Model operating expenses with fixed and variable cost components")

# Initialize session state
if "expense_forecast" not in st.session_state:
    st.session_state.expense_forecast = None

if "demand_forecast" not in st.session_state:
    st.session_state.demand_forecast = None

# Get demand forecast data
demand_df = st.session_state.demand_forecast
if demand_df is None:
    st.warning("⚠️ Please complete the Demand Forecast first to get accurate expense projections.")
    demo_visitors = 250000
else:
    demo_visitors = int(demand_df.iloc[0]["Total Visitors"])

st.markdown("---")

st.subheader("Expense Categories Configuration")
st.info("For each expense category, enter the fixed annual amount and variable cost per visitor")

# Define all expense categories
expense_categories = [
    "Cost of Goods Sold",
    "Direct Labor",
    "Maintenance / Repairs",
    "Payroll Taxes / Benefits",
    "Electric Power / Fuel / Utilities",
    "G&A",
    "Marketing / Advertising",
    "Insurance",
    "Property / Other Taxes",
    "Miscellaneous",
    "Other Direct",
]

# Create input columns
expense_inputs = {}

for idx, category in enumerate(expense_categories):
    if idx % 2 == 0:
        col1, col2 = st.columns(2)
        current_col = col1
    else:
        current_col = col2
    
    with current_col:
        st.markdown(f"**{category}**")
        
        exp_col_a, exp_col_b = st.columns(2)
        
        with exp_col_a:
            fixed = st.number_input(
                f"{category} - Fixed Annual ($)",
                min_value=0,
                value=100000,
                step=10000,
                key=f"{category}_fixed",
            )
        
        with exp_col_b:
            variable = st.number_input(
                f"{category} - Variable ($ per visitor)",
                min_value=0.0,
                value=5.0,
                step=0.5,
                key=f"{category}_variable",
            )
        
        expense_inputs[category] = {
            "fixed": fixed,
            "variable": variable,
        }

st.markdown("---")

# Calculate expense forecast
st.subheader("Expense Forecast Results")

# Use demand forecast if available
if demand_df is not None:
    years = demand_df["Year"].values
    total_visitors = demand_df["Total Visitors"].values
else:
    # Demo data
    years = np.arange(0, 11)
    base_visitors = demo_visitors
    growth_rate = 0.035
    total_visitors = (base_visitors * (1 + growth_rate) ** years).astype(int)

# Calculate expenses by category
expense_data = []

for i, year in enumerate(years):
    year_visitors = total_visitors[i]
    year_expenses = {"Year": int(year)}
    
    for category, inputs in expense_inputs.items():
        fixed = inputs["fixed"]
        variable = inputs["variable"]
        total_expense = fixed + (variable * year_visitors)
        year_expenses[category] = total_expense
    
    year_expenses["Total Expenses"] = sum([
        year_expenses[cat] for cat in expense_categories
    ])
    
    expense_data.append(year_expenses)

expense_df = pd.DataFrame(expense_data)
st.session_state.expense_forecast = expense_df

# Display expense forecast
display_df = expense_df.copy()
for col in display_df.columns:
    if col != "Year":
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")

st.dataframe(display_df, hide_index=True, use_container_width=True)

st.markdown("---")

# Visualizations
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("Total Expense Projection")
    fig_expense = px.line(
        expense_df,
        x="Year",
        y="Total Expenses",
        title="Annual Total Expenses Projection",
        markers=True,
    )
    fig_expense.update_yaxes(title="Expenses ($)")
    fig_expense.update_xaxes(title="Year")
    st.plotly_chart(fig_expense, use_container_width=True)

with viz_col2:
    st.subheader("Expense by Category (Year 1)")
    year1_data = expense_df.iloc[0]
    categories = expense_categories
    values = [year1_data[cat] for cat in categories]
    
    fig_mix = px.pie(
        names=categories,
        values=values,
        title="Expense Mix - Year 1",
    )
    st.plotly_chart(fig_mix, use_container_width=True)

st.markdown("---")

# Stacked bar chart
st.subheader("Expense Composition Over Time")

fig_stacked = go.Figure()

for category in expense_categories:
    fig_stacked.add_trace(go.Bar(
        x=expense_df["Year"],
        y=expense_df[category],
        name=category,
    ))

fig_stacked.update_layout(
    barmode='stack',
    title="Expense Composition Over Time",
    xaxis_title="Year",
    yaxis_title="Expenses ($)",
    hovermode='x unified',
)

st.plotly_chart(fig_stacked, use_container_width=True)

st.markdown("---")

# Fixed vs Variable breakdown
st.subheader("Fixed vs Variable Expense Analysis")

fixed_var_data = []
for i, year in enumerate(years):
    year_visitors = total_visitors[i]
    
    total_fixed = sum([inputs["fixed"] for inputs in expense_inputs.values()])
    total_variable = sum([inputs["variable"] * year_visitors for inputs in expense_inputs.values()])
    
    fixed_var_data.append({
        "Year": int(year),
        "Fixed Expenses": total_fixed,
        "Variable Expenses": total_variable,
    })

fixed_var_df = pd.DataFrame(fixed_var_data)

fig_fixed_var = go.Figure()

fig_fixed_var.add_trace(go.Bar(
    x=fixed_var_df["Year"],
    y=fixed_var_df["Fixed Expenses"],
    name="Fixed Expenses",
))

fig_fixed_var.add_trace(go.Bar(
    x=fixed_var_df["Year"],
    y=fixed_var_df["Variable Expenses"],
    name="Variable Expenses",
))

fig_fixed_var.update_layout(
    barmode='stack',
    title="Fixed vs Variable Expenses",
    xaxis_title="Year",
    yaxis_title="Expenses ($)",
)

st.plotly_chart(fig_fixed_var, use_container_width=True)

st.markdown("---")

# Summary metrics
st.subheader("Expense Summary")
summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

year1_expense = expense_df.iloc[0]["Total Expenses"]
year10_expense = expense_df.iloc[-1]["Total Expenses"]
total_10yr_expense = expense_df["Total Expenses"].sum()
avg_annual_expense = expense_df["Total Expenses"].mean()

with summary_col1:
    st.metric("Year 1 Expenses", f"${year1_expense/1e6:.1f}M")

with summary_col2:
    st.metric("Year 10 Expenses", f"${year10_expense/1e6:.1f}M")

with summary_col3:
    st.metric("10-Year Total", f"${total_10yr_expense/1e6:.1f}M")

with summary_col4:
    st.metric("Avg Annual", f"${avg_annual_expense/1e6:.1f}M")

# Per-visitor analysis
st.markdown("---")
st.subheader("Cost Per Visitor Analysis")

cost_per_visitor = []
for i, year in enumerate(years):
    year_visitors = total_visitors[i]
    year_expense = expense_df.iloc[i]["Total Expenses"]
    cost_per_visitor.append({
        "Year": int(year),
        "Cost Per Visitor": year_expense / year_visitors if year_visitors > 0 else 0,
    })

cpv_df = pd.DataFrame(cost_per_visitor)

fig_cpv = px.line(
    cpv_df,
    x="Year",
    y="Cost Per Visitor",
    title="Cost Per Visitor Trend",
    markers=True,
)
fig_cpv.update_yaxes(title="Cost Per Visitor ($)")
fig_cpv.update_xaxes(title="Year")

st.plotly_chart(fig_cpv, use_container_width=True)

st.success("✅ Expense forecast saved to session! Use in Scenario Builder and financial analysis.")
