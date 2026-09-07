import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Scenario Builder",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Scenario Builder")
st.markdown("Compare multiple financial scenarios side-by-side")

# Initialize session state
if "scenarios_data" not in st.session_state:
    st.session_state.scenarios_data = {}

st.markdown("---")

st.subheader("Create Custom Scenarios")

# Base scenario inputs
base_col1, base_col2, base_col3, base_col4 = st.columns(4)

with base_col1:
    base_visitors = st.number_input(
        "Base Year Visitors",
        min_value=50000,
        max_value=1000000,
        value=250000,
        step=10000,
    )

with base_col2:
    base_growth = st.slider(
        "Base Growth Rate (%)",
        min_value=-10.0,
        max_value=20.0,
        value=3.5,
        step=0.1,
    )

with base_col3:
    base_revenue_per_visitor = st.number_input(
        "Revenue Per Visitor",
        min_value=20.00,
        max_value=200.00,
        value=100.00,
        step=5.00,
    )

with base_col4:
    base_cost_per_visitor = st.number_input(
        "Cost Per Visitor",
        min_value=10.00,
        max_value=100.00,
        value=30.00,
        step=2.00,
    )

st.markdown("---")

st.subheader("Scenario Definitions")

# Define three distinct scenarios
scenarios_config = {
    "Conservative": {
        "visitor_adjustment": -0.10,  # -10% from base
        "growth_adjustment": -0.02,   # -2% growth
        "revenue_adjustment": -0.05,   # -5% revenue per visitor
        "cost_adjustment": 0.05,       # +5% cost per visitor
        "description": "Lower demand, reduced spending"
    },
    "Base Case": {
        "visitor_adjustment": 0.0,
        "growth_adjustment": 0.0,
        "revenue_adjustment": 0.0,
        "cost_adjustment": 0.0,
        "description": "Expected performance"
    },
    "Optimistic": {
        "visitor_adjustment": 0.15,    # +15% from base
        "growth_adjustment": 0.03,     # +3% growth
        "revenue_adjustment": 0.08,    # +8% revenue per visitor
        "cost_adjustment": -0.03,      # -3% cost per visitor
        "description": "Strong demand, increased spending"
    },
}

# Calculate scenarios
scenarios_results = {}

for scenario_name, adjustments in scenarios_config.items():
    visitors = base_visitors * (1 + adjustments["visitor_adjustment"])
    growth = base_growth + (adjustments["growth_adjustment"] * 100)
    revenue_pv = base_revenue_per_visitor * (1 + adjustments["revenue_adjustment"])
    cost_pv = base_cost_per_visitor * (1 + adjustments["cost_adjustment"])
    
    # Project 10 years
    years = np.arange(0, 11)
    annual_visitors = visitors * (1 + growth/100) ** years
    annual_revenue = annual_visitors * revenue_pv
    annual_costs = annual_visitors * cost_pv
    annual_ebitda = annual_revenue - annual_costs
    
    scenarios_results[scenario_name] = pd.DataFrame({
        "Year": years,
        "Visitors": annual_visitors.astype(int),
        "Revenue": annual_revenue,
        "Costs": annual_costs,
        "EBITDA": annual_ebitda,
        "EBITDA Margin": (annual_ebitda / annual_revenue * 100).round(1),
    })

st.session_state.scenarios_data = scenarios_results

st.markdown("---")

# Display scenario comparison
st.subheader("Scenario Summary Metrics")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.markdown("### Conservative Scenario")
    st.write(f"📉 {scenarios_config['Conservative']['description']}")
    cons_data = scenarios_results["Conservative"]
    st.metric("Year 1 Visitors", f"{cons_data.iloc[0]['Visitors']:,}")
    st.metric("Year 10 EBITDA", f"${cons_data.iloc[-1]['EBITDA']:,.0f}")
    st.metric("10-Yr Total EBITDA", f"${cons_data['EBITDA'].sum():,.0f}")

with summary_col2:
    st.markdown("### Base Case Scenario")
    st.write(f"📊 {scenarios_config['Base Case']['description']}")
    base_data = scenarios_results["Base Case"]
    st.metric("Year 1 Visitors", f"{base_data.iloc[0]['Visitors']:,}")
    st.metric("Year 10 EBITDA", f"${base_data.iloc[-1]['EBITDA']:,.0f}")
    st.metric("10-Yr Total EBITDA", f"${base_data['EBITDA'].sum():,.0f}")

with summary_col3:
    st.markdown("### Optimistic Scenario")
    st.write(f"📈 {scenarios_config['Optimistic']['description']}")
    opt_data = scenarios_results["Optimistic"]
    st.metric("Year 1 Visitors", f"{opt_data.iloc[0]['Visitors']:,}")
    st.metric("Year 10 EBITDA", f"${opt_data.iloc[-1]['EBITDA']:,.0f}")
    st.metric("10-Yr Total EBITDA", f"${opt_data['EBITDA'].sum():,.0f}")

st.markdown("---")

# Visualizations
st.subheader("Scenario Comparison Charts")

viz_col1, viz_col2 = st.columns(2)

# Prepare data for multi-scenario chart
multi_scenario_data = []
for scenario_name, df in scenarios_results.items():
    temp_df = df.copy()
    temp_df["Scenario"] = scenario_name
    multi_scenario_data.append(temp_df)

combined_df = pd.concat(multi_scenario_data, ignore_index=True)

with viz_col1:
    st.subheader("Visitor Volume Projection")
    fig_visitors = px.line(
        combined_df,
        x="Year",
        y="Visitors",
        color="Scenario",
        title="Annual Visitor Projections",
        markers=True,
    )
    st.plotly_chart(fig_visitors, use_container_width=True)

with viz_col2:
    st.subheader("Annual EBITDA")
    fig_ebitda = px.line(
        combined_df,
        x="Year",
        y="EBITDA",
        color="Scenario",
        title="EBITDA Projections",
        markers=True,
    )
    st.plotly_chart(fig_ebitda, use_container_width=True)

st.markdown("---")

# Detailed scenario tables
for scenario_name, df in scenarios_results.items():
    st.subheader(f"{scenario_name} - Detailed Projection")
    
    display_df = df.copy()
    for col in ["Revenue", "Costs", "EBITDA"]:
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")
    display_df["Visitors"] = display_df["Visitors"].apply(lambda x: f"{x:,}")
    display_df["EBITDA Margin"] = display_df["EBITDA Margin"].apply(lambda x: f"{x:.1f}%")
    
    st.dataframe(display_df, hide_index=True, use_container_width=True)
    st.markdown("---")

# Sensitivity analysis
st.subheader("Scenario Range Analysis")

sensitivity_col1, sensitivity_col2 = st.columns(2)

with sensitivity_col1:
    st.markdown("**Year 10 EBITDA Range**")
    
    cons_yr10 = scenarios_results["Conservative"].iloc[-1]["EBITDA"]
    base_yr10 = scenarios_results["Base Case"].iloc[-1]["EBITDA"]
    opt_yr10 = scenarios_results["Optimistic"].iloc[-1]["EBITDA"]
    
    fig_range = go.Figure(data=[
        go.Bar(
            x=["Conservative", "Base Case", "Optimistic"],
            y=[cons_yr10, base_yr10, opt_yr10],
            marker_color=["#FF6B6B", "#4ECDC4", "#45B7D1"],
        )
    ])
    fig_range.update_layout(
        title="Year 10 EBITDA by Scenario",
        yaxis_title="EBITDA ($)",
    )
    st.plotly_chart(fig_range, use_container_width=True)

with sensitivity_col2:
    st.markdown("**10-Year Cumulative EBITDA**")
    
    cons_total = scenarios_results["Conservative"]["EBITDA"].sum()
    base_total = scenarios_results["Base Case"]["EBITDA"].sum()
    opt_total = scenarios_results["Optimistic"]["EBITDA"].sum()
    
    fig_total = go.Figure(data=[
        go.Bar(
            x=["Conservative", "Base Case", "Optimistic"],
            y=[cons_total, base_total, opt_total],
            marker_color=["#FF6B6B", "#4ECDC4", "#45B7D1"],
        )
    ])
    fig_total.update_layout(
        title="10-Year Cumulative EBITDA",
        yaxis_title="Total EBITDA ($)",
    )
    st.plotly_chart(fig_total, use_container_width=True)

st.markdown("---")

st.info(
    "💡 **Key Takeaway**: Use these scenarios to stress-test your business model and ensure "
    "financial resilience across different market conditions."
)
