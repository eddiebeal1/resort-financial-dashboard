import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Revenue Forecast",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Revenue Forecast")
st.markdown("Model revenue by category based on visitor volumes and spending patterns")

# Initialize session state
if "revenue_forecast" not in st.session_state:
    st.session_state.revenue_forecast = None

if "demand_forecast" not in st.session_state:
    st.session_state.demand_forecast = None

# Get demand forecast data
demand_df = st.session_state.demand_forecast
if demand_df is None:
    st.warning("⚠️ Please complete the Demand Forecast first to get accurate revenue projections.")
    demo_visitors = 250000
else:
    demo_visitors = int(demand_df.iloc[0]["Total Visitors"])

st.markdown("---")

st.subheader("Revenue per Visitor by Category")
st.info("Enter the average revenue per visitor for each category")

# Create columns for revenue inputs
rev_col1, rev_col2, rev_col3, rev_col4 = st.columns(4)

with rev_col1:
    ticket_rpv = st.number_input(
        "Ticket Sales",
        min_value=0.00,
        max_value=200.00,
        value=50.00,
        step=1.00,
        format="$%.2f",
        help="Revenue per visitor from lift tickets"
    )

with rev_col2:
    snowplay_rpv = st.number_input(
        "Snowplay & Winter Ops",
        min_value=0.00,
        max_value=100.00,
        value=8.00,
        step=0.50,
        format="$%.2f",
        help="Tubing, sledding, and other winter operations"
    )

with rev_col3:
    ski_school_rpv = st.number_input(
        "Ski School",
        min_value=0.00,
        max_value=150.00,
        value=15.00,
        step=1.00,
        format="$%.2f",
        help="Lessons and instruction revenue"
    )

with rev_col4:
    retail_rpv = st.number_input(
        "Retail",
        min_value=0.00,
        max_value=100.00,
        value=12.00,
        step=0.50,
        format="$%.2f",
        help="Clothing, accessories, equipment sales"
    )

st.markdown("---")

rev_col5, rev_col6, rev_col7, rev_col8 = st.columns(4)

with rev_col5:
    rentals_rpv = st.number_input(
        "Rentals",
        min_value=0.00,
        max_value=100.00,
        value=9.00,
        step=0.50,
        format="$%.2f",
        help="Equipment rental revenue"
    )

with rev_col6:
    fb_rpv = st.number_input(
        "Food & Beverage",
        min_value=0.00,
        max_value=100.00,
        value=18.00,
        step=0.50,
        format="$%.2f",
        help="Dining and beverages revenue per visitor"
    )

with rev_col7:
    summer_rpv = st.number_input(
        "Summer Activities",
        min_value=0.00,
        max_value=100.00,
        value=8.00,
        step=0.50,
        format="$%.2f",
        help="Mountain biking, hiking, events, etc."
    )

with rev_col8:
    other_rpv = st.number_input(
        "Other Revenue",
        min_value=0.00,
        max_value=50.00,
        value=2.00,
        step=0.25,
        format="$%.2f",
        help="Miscellaneous revenue streams"
    )

st.markdown("---")

# Seasonal adjustments
st.subheader("Seasonal Revenue Adjustments")
st.info("Adjust revenue multipliers by season (1.0 = baseline, 1.5 = 50% higher, etc.)")

season_col1, season_col2, season_col3, season_col4 = st.columns(4)

with season_col1:
    winter_multiplier = st.slider(
        "Winter Multiplier",
        min_value=0.5,
        max_value=2.0,
        value=1.3,
        step=0.1,
    )

with season_col2:
    spring_multiplier = st.slider(
        "Spring Multiplier",
        min_value=0.5,
        max_value=2.0,
        value=0.9,
        step=0.1,
    )

with season_col3:
    summer_multiplier = st.slider(
        "Summer Multiplier",
        min_value=0.5,
        max_value=2.0,
        value=1.1,
        step=0.1,
    )

with season_col4:
    fall_multiplier = st.slider(
        "Fall Multiplier",
        min_value=0.5,
        max_value=2.0,
        value=0.8,
        step=0.1,
    )

st.markdown("---")

# Calculate revenue forecast
st.subheader("Revenue Forecast Results")

# Use demand forecast if available
if demand_df is not None:
    years = demand_df["Year"].values
    total_visitors = demand_df["Total Visitors"].values
    winter_visitors = demand_df["Winter"].values
    spring_visitors = demand_df["Spring"].values
    summer_visitors = demand_df["Summer"].values
    fall_visitors = demand_df["Fall"].values
else:
    # Demo data
    years = np.arange(0, 11)
    base_visitors = demo_visitors
    growth_rate = 0.035
    total_visitors = (base_visitors * (1 + growth_rate) ** years).astype(int)
    winter_visitors = (total_visitors * 0.50).astype(int)
    spring_visitors = (total_visitors * 0.15).astype(int)
    summer_visitors = (total_visitors * 0.20).astype(int)
    fall_visitors = (total_visitors * 0.15).astype(int)

# Calculate revenue by category
revenue_data = []

for i, year in enumerate(years):
    # Adjust visitor counts by season for revenue calculations
    winter_rev = winter_visitors[i] * winter_multiplier
    spring_rev = spring_visitors[i] * spring_multiplier
    summer_rev = summer_visitors[i] * summer_multiplier
    fall_rev = fall_visitors[i] * fall_multiplier
    
    total_yr_visitors = winter_rev + spring_rev + summer_rev + fall_rev
    
    # Calculate revenue for each category
    ticket_rev = total_yr_visitors * ticket_rpv
    snowplay_rev = total_yr_visitors * snowplay_rpv
    ski_school_rev = total_yr_visitors * ski_school_rpv
    retail_rev = total_yr_visitors * retail_rpv
    rentals_rev = total_yr_visitors * rentals_rpv
    fb_rev = total_yr_visitors * fb_rpv
    summer_rev_cat = total_yr_visitors * summer_rpv
    other_rev = total_yr_visitors * other_rpv
    
    total_revenue = (ticket_rev + snowplay_rev + ski_school_rev + retail_rev + 
                     rentals_rev + fb_rev + summer_rev_cat + other_rev)
    
    revenue_data.append({
        "Year": int(year),
        "Ticket Sales": ticket_rev,
        "Snowplay & Winter Ops": snowplay_rev,
        "Ski School": ski_school_rev,
        "Retail": retail_rev,
        "Rentals": rentals_rev,
        "Food & Beverage": fb_rev,
        "Summer Activities": summer_rev_cat,
        "Other Revenue": other_rev,
        "Total Revenue": total_revenue,
    })

revenue_df = pd.DataFrame(revenue_data)
st.session_state.revenue_forecast = revenue_df

# Display revenue forecast
display_df = revenue_df.copy()
for col in display_df.columns:
    if col != "Year":
        display_df[col] = display_df[col].apply(lambda x: f"${x:,.0f}")

st.dataframe(display_df, hide_index=True, use_container_width=True)

st.markdown("---")

# Visualizations
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("Total Revenue Projection")
    fig_revenue = px.line(
        revenue_df,
        x="Year",
        y="Total Revenue",
        title="Annual Revenue Projection",
        markers=True,
    )
    fig_revenue.update_yaxes(title="Revenue ($)")
    fig_revenue.update_xaxes(title="Year")
    st.plotly_chart(fig_revenue, use_container_width=True)

with viz_col2:
    st.subheader("Revenue by Category (Year 1)")
    year1_data = revenue_df.iloc[0]
    categories = ["Ticket Sales", "Snowplay & Winter Ops", "Ski School", "Retail", 
                  "Rentals", "Food & Beverage", "Summer Activities", "Other Revenue"]
    values = [year1_data[cat] for cat in categories]
    
    fig_mix = px.pie(
        names=categories,
        values=values,
        title="Revenue Mix - Year 1",
    )
    st.plotly_chart(fig_mix, use_container_width=True)

st.markdown("---")

# Stacked area chart
st.subheader("Revenue Composition Over Time")
categories_to_plot = ["Ticket Sales", "Food & Beverage", "Retail", "Rentals", 
                      "Ski School", "Snowplay & Winter Ops", "Summer Activities", "Other Revenue"]

fig_stacked = go.Figure()

for category in categories_to_plot:
    fig_stacked.add_trace(go.Scatter(
        x=revenue_df["Year"],
        y=revenue_df[category],
        mode='lines',
        name=category,
        stackgroup='one',
        fillcolor=None,
    ))

fig_stacked.update_layout(
    title="Revenue Composition Over Time",
    xaxis_title="Year",
    yaxis_title="Revenue ($)",
    hovermode='x unified',
)

st.plotly_chart(fig_stacked, use_container_width=True)

st.markdown("---")

# Summary metrics
st.subheader("Revenue Summary")
summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

year1_revenue = revenue_df.iloc[0]["Total Revenue"]
year10_revenue = revenue_df.iloc[-1]["Total Revenue"]
total_10yr_revenue = revenue_df["Total Revenue"].sum()
avg_annual_revenue = revenue_df["Total Revenue"].mean()

with summary_col1:
    st.metric("Year 1 Revenue", f"${year1_revenue/1e6:.1f}M")

with summary_col2:
    st.metric("Year 10 Revenue", f"${year10_revenue/1e6:.1f}M")

with summary_col3:
    st.metric("10-Year Total", f"${total_10yr_revenue/1e6:.1f}M")

with summary_col4:
    st.metric("Avg Annual", f"${avg_annual_revenue/1e6:.1f}M")

st.success("✅ Revenue forecast saved to session! Use in Expense Forecast and Scenario Builder.")
