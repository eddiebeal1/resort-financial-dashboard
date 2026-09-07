import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

st.set_page_config(
    page_title="Risk Analysis",
    page_icon="⚠️",
    layout="wide",
)

st.title("⚠️ Risk Analysis")
st.markdown("Monte Carlo simulations and sensitivity analysis for financial projections")

st.markdown("---")

# Risk Parameters
st.subheader("Risk Parameters for Monte Carlo Simulation")

risk_col1, risk_col2, risk_col3, risk_col4 = st.columns(4)

with risk_col1:
    base_visitors = st.number_input(
        "Base Year Visitors",
        min_value=50000,
        value=250000,
        step=10000,
    )

with risk_col2:
    visitor_volatility = st.slider(
        "Visitor Volatility (%)",
        min_value=1,
        max_value=30,
        value=10,
        help="Standard deviation of visitor projections"
    )

with risk_col3:
    revenue_per_visitor = st.number_input(
        "Revenue Per Visitor ($)",
        min_value=20.00,
        value=100.00,
        step=5.00,
    )

with risk_col4:
    revenue_volatility = st.slider(
        "Revenue Volatility (%)",
        min_value=1,
        max_value=30,
        value=8,
        help="Standard deviation of revenue per visitor"
    )

risk_col5, risk_col6 = st.columns(2)

with risk_col5:
    cost_per_visitor = st.number_input(
        "Cost Per Visitor ($)",
        min_value=10.00,
        value=30.00,
        step=2.00,
    )

with risk_col6:
    cost_volatility = st.slider(
        "Cost Volatility (%)",
        min_value=1,
        max_value=20,
        value=6,
        help="Standard deviation of cost per visitor"
    )

st.markdown("---")

# Monte Carlo simulation
st.subheader("Monte Carlo Simulation Results")

num_simulations = st.slider("Number of Simulations", 100, 10000, 1000, 100)
num_years = 10
base_growth = 0.035

# Run Monte Carlo
np.random.seed(42)
simulations_results = []

for sim in range(num_simulations):
    yearly_data = []
    for year in range(num_years + 1):
        # Generate random variations
        visitor_factor = np.random.normal(1.0, visitor_volatility / 100)
        revenue_factor = np.random.normal(1.0, revenue_volatility / 100)
        cost_factor = np.random.normal(1.0, cost_volatility / 100)
        
        # Calculate values
        visitors = base_visitors * ((1 + base_growth) ** year) * visitor_factor
        revenue = visitors * revenue_per_visitor * revenue_factor
        costs = visitors * cost_per_visitor * cost_factor
        ebitda = revenue - costs
        
        yearly_data.append({
            "Year": year,
            "Visitors": visitors,
            "Revenue": revenue,
            "Costs": costs,
            "EBITDA": ebitda,
        })
    
    simulations_results.append(pd.DataFrame(yearly_data))

st.markdown("---")

# Calculate statistics
st.subheader("Statistical Analysis")

# Extract Year 10 EBITDA from all simulations
year_10_ebitdas = [sim.iloc[-1]["EBITDA"] for sim in simulations_results]
year_10_revenues = [sim.iloc[-1]["Revenue"] for sim in simulations_results]
year_10_costs = [sim.iloc[-1]["Costs"] for sim in simulations_results]

stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)

with stat_col1:
    st.metric("Mean Year 10 EBITDA", f"${np.mean(year_10_ebitdas):,.0f}")

with stat_col2:
    st.metric("Median Year 10 EBITDA", f"${np.median(year_10_ebitdas):,.0f}")

with stat_col3:
    st.metric("Std Dev Year 10 EBITDA", f"${np.std(year_10_ebitdas):,.0f}")

with stat_col4:
    st.metric("Coefficient of Variation", f"{(np.std(year_10_ebitdas) / np.mean(year_10_ebitdas) * 100):.1f}%")

st.markdown("---")

# Percentile analysis
st.subheader("EBITDA Distribution Analysis")

percentiles = [10, 25, 50, 75, 90]
percentile_values = [np.percentile(year_10_ebitdas, p) for p in percentiles]

percentile_data = pd.DataFrame({
    "Percentile": [f"{p}th" for p in percentiles],
    "Year 10 EBITDA": percentile_values,
})

# Format for display
display_percentile = percentile_data.copy()
display_percentile["Year 10 EBITDA"] = display_percentile["Year 10 EBITDA"].apply(lambda x: f"${x:,.0f}")

st.dataframe(display_percentile, hide_index=True, use_container_width=True)

st.markdown("---")

# Visualizations
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("EBITDA Distribution (Year 10)")
    
    fig_hist = go.Figure(data=[
        go.Histogram(
            x=year_10_ebitdas,
            nbinsx=50,
            name="EBITDA",
            marker_color="#45B7D1",
        )
    ])
    
    fig_hist.add_vline(
        x=np.mean(year_10_ebitdas),
        line_dash="dash",
        line_color="red",
        annotation_text="Mean",
    )
    
    fig_hist.update_layout(
        title="Distribution of Year 10 EBITDA Outcomes",
        xaxis_title="EBITDA ($)",
        yaxis_title="Frequency",
    )
    
    st.plotly_chart(fig_hist, use_container_width=True)

with viz_col2:
    st.subheader("Downside Risk Analysis")
    
    # Create confidence intervals
    confidence_levels = [90, 75, 50]
    colors = ["#FF6B6B", "#FFA500", "#45B7D1"]
    
    fig_box = go.Figure()
    
    for i, (conf, color) in enumerate(zip(confidence_levels, colors)):
        lower = np.percentile(year_10_ebitdas, (100 - conf) / 2)
        upper = np.percentile(year_10_ebitdas, 100 - (100 - conf) / 2)
        
        fig_box.add_trace(go.Box(
            y=year_10_ebitdas,
            name=f"{conf}% Confidence",
            marker_color=color,
        ))
    
    fig_box.update_layout(
        title="Confidence Intervals - Year 10 EBITDA",
        yaxis_title="EBITDA ($)",
    )
    
    st.plotly_chart(fig_box, use_container_width=True)

st.markdown("---")

# Sensitivity Analysis
st.subheader("Sensitivity Analysis")

st.info("How sensitive is Year 10 EBITDA to changes in key assumptions?")

# Calculate sensitivity to each variable
sensitivity_data = []

# Visitor volume sensitivity
for delta in [-20, -10, 0, 10, 20]:
    adj_visitors = base_visitors * (1 + base_growth) ** 10 * (1 + delta/100)
    adj_revenue = adj_visitors * revenue_per_visitor
    adj_costs = adj_visitors * cost_per_visitor
    adj_ebitda = adj_revenue - adj_costs
    sensitivity_data.append({
        "Variable": "Visitor Volume",
        "Change (%)": delta,
        "Year 10 EBITDA": adj_ebitda,
    })

# Revenue per visitor sensitivity
for delta in [-20, -10, 0, 10, 20]:
    adj_rpv = revenue_per_visitor * (1 + delta/100)
    adj_visitors = base_visitors * (1 + base_growth) ** 10
    adj_revenue = adj_visitors * adj_rpv
    adj_costs = adj_visitors * cost_per_visitor
    adj_ebitda = adj_revenue - adj_costs
    sensitivity_data.append({
        "Variable": "Revenue Per Visitor",
        "Change (%)": delta,
        "Year 10 EBITDA": adj_ebitda,
    })

# Cost per visitor sensitivity
for delta in [-20, -10, 0, 10, 20]:
    adj_cpv = cost_per_visitor * (1 + delta/100)
    adj_visitors = base_visitors * (1 + base_growth) ** 10
    adj_revenue = adj_visitors * revenue_per_visitor
    adj_costs = adj_visitors * adj_cpv
    adj_ebitda = adj_revenue - adj_costs
    sensitivity_data.append({
        "Variable": "Cost Per Visitor",
        "Change (%)": delta,
        "Year 10 EBITDA": adj_ebitda,
    })

sensitivity_df = pd.DataFrame(sensitivity_data)

# Visualize sensitivity
fig_sensitivity = px.line(
    sensitivity_df,
    x="Change (%)",
    y="Year 10 EBITDA",
    color="Variable",
    title="Sensitivity Analysis: Impact on Year 10 EBITDA",
    markers=True,
)

st.plotly_chart(fig_sensitivity, use_container_width=True)

st.markdown("---")

# Risk Summary
st.subheader("Risk Summary")

risk_summary_col1, risk_summary_col2, risk_summary_col3 = st.columns(3)

with risk_summary_col1:
    st.markdown("**Downside Risk (10th Percentile)**")
    downside = np.percentile(year_10_ebitdas, 10)
    mean_ebitda = np.mean(year_10_ebitdas)
    downside_pct = ((downside - mean_ebitda) / mean_ebitda * 100)
    st.write(f"${downside:,.0f}")
    st.write(f"({downside_pct:.1f}% vs mean)")

with risk_summary_col2:
    st.markdown("**Base Case (50th Percentile)**")
    median_ebitda = np.percentile(year_10_ebitdas, 50)
    st.write(f"${median_ebitda:,.0f}")
    st.write("(Median outcome)")

with risk_summary_col3:
    st.markdown("**Upside Potential (90th Percentile)**")
    upside = np.percentile(year_10_ebitdas, 90)
    upside_pct = ((upside - mean_ebitda) / mean_ebitda * 100)
    st.write(f"${upside:,.0f}")
    st.write(f"(+{upside_pct:.1f}% vs mean)")

st.markdown("---")

st.info(
    "💡 **Key Insight**: Review the sensitivity analysis to identify which variables have the greatest impact "
    "on profitability. Focus risk mitigation efforts on the most sensitive drivers."
)
