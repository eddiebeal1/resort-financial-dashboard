import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Demand Forecast",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Demand Forecast")
st.markdown("Project visitor volumes based on your inputs and market assumptions")

# Initialize session state
if "demand_forecast" not in st.session_state:
    st.session_state.demand_forecast = None

st.markdown("---")

# Input section
st.subheader("Visitor Volume Assumptions")

input_col1, input_col2, input_col3 = st.columns(3)

with input_col1:
    base_year_visitors = st.number_input(
        "Base Year Annual Visitors",
        min_value=10000,
        max_value=1000000,
        value=250000,
        step=10000,
        help="Starting visitor count for projections"
    )

with input_col2:
    forecast_years = st.number_input(
        "Forecast Period (Years)",
        min_value=1,
        max_value=20,
        value=10,
        help="Number of years to project"
    )

with input_col3:
    annual_growth_rate = st.slider(
        "Annual Growth Rate (%)",
        min_value=-10.0,
        max_value=20.0,
        value=3.5,
        step=0.1,
        help="Expected annual visitor growth rate"
    )

st.markdown("---")

# Seasonal breakdown
st.subheader("Seasonal Distribution")
st.info("Enter the percentage of annual visitors for each season")

seasonal_col1, seasonal_col2, seasonal_col3, seasonal_col4 = st.columns(4)

with seasonal_col1:
    winter_pct = st.slider(
        "Winter (%)",
        min_value=0,
        max_value=100,
        value=50,
        help="Oct - Mar"
    )

with seasonal_col2:
    spring_pct = st.slider(
        "Spring (%)",
        min_value=0,
        max_value=100,
        value=15,
        help="Apr - May"
    )

with seasonal_col3:
    summer_pct = st.slider(
        "Summer (%)",
        min_value=0,
        max_value=100,
        value=20,
        help="Jun - Aug"
    )

with seasonal_col4:
    fall_pct = st.slider(
        "Fall (%)",
        min_value=0,
        max_value=100,
        value=15,
        help="Sep"
    )

total_pct = winter_pct + spring_pct + summer_pct + fall_pct
if total_pct != 100:
    st.warning(f"⚠️ Seasonal percentages sum to {total_pct}%. They must equal 100%.")

st.markdown("---")

# Visitor segment breakdown
st.subheader("Visitor Segment Mix")
st.info("Enter the percentage breakdown of visitor types")

segment_col1, segment_col2, segment_col3, segment_col4 = st.columns(4)

with segment_col1:
    skier_pct = st.slider(
        "Skiers/Snowboarders (%)",
        min_value=0,
        max_value=100,
        value=45,
    )

with segment_col2:
    snowplay_pct = st.slider(
        "Snowplay/Tubing (%)",
        min_value=0,
        max_value=100,
        value=25,
    )

with segment_col3:
    summer_activity_pct = st.slider(
        "Summer Activity (%)",
        min_value=0,
        max_value=100,
        value=20,
    )

with segment_col4:
    other_segment_pct = st.slider(
        "Other (%)",
        min_value=0,
        max_value=100,
        value=10,
    )

segment_total = skier_pct + snowplay_pct + summer_activity_pct + other_segment_pct
if segment_total != 100:
    st.warning(f"⚠️ Segment percentages sum to {segment_total}%. They must equal 100%.")

st.markdown("---")

# Generate forecast
st.subheader("Demand Forecast Results")

# Create forecast dataframe
years = np.arange(0, forecast_years + 1)
visitors = base_year_visitors * (1 + annual_growth_rate/100) ** years

forecast_df = pd.DataFrame({
    "Year": years,
    "Total Visitors": visitors.astype(int),
    "Winter": (visitors * winter_pct / 100).astype(int),
    "Spring": (visitors * spring_pct / 100).astype(int),
    "Summer": (visitors * summer_pct / 100).astype(int),
    "Fall": (visitors * fall_pct / 100).astype(int),
    "Skiers": (visitors * skier_pct / 100).astype(int),
    "Snowplay": (visitors * snowplay_pct / 100).astype(int),
    "Summer Activity": (visitors * summer_activity_pct / 100).astype(int),
    "Other": (visitors * other_segment_pct / 100).astype(int),
})

# Store in session state
st.session_state.demand_forecast = forecast_df

# Display forecast table
st.dataframe(forecast_df, hide_index=True, use_container_width=True)

st.markdown("---")

# Visualizations
viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    st.subheader("Total Visitor Projection")
    fig_total = px.line(
        forecast_df,
        x="Year",
        y="Total Visitors",
        title="Annual Visitor Volume Projection",
        markers=True,
        line_shape="linear"
    )
    fig_total.update_xaxes(title="Year")
    fig_total.update_yaxes(title="Visitors")
    st.plotly_chart(fig_total, use_container_width=True)

with viz_col2:
    st.subheader("Seasonal Distribution (Year 1)")
    seasonal_data = {
        "Season": ["Winter", "Spring", "Summer", "Fall"],
        "Visitors": [
            int(base_year_visitors * winter_pct / 100),
            int(base_year_visitors * spring_pct / 100),
            int(base_year_visitors * summer_pct / 100),
            int(base_year_visitors * fall_pct / 100),
        ]
    }
    fig_seasonal = px.pie(
        seasonal_data,
        names="Season",
        values="Visitors",
        title="Seasonal Visitor Distribution"
    )
    st.plotly_chart(fig_seasonal, use_container_width=True)

st.markdown("---")

# Segment breakdown
segment_col1, segment_col2 = st.columns(2)

with segment_col1:
    st.subheader("Visitor Segment Mix (Year 1)")
    segment_data = {
        "Segment": ["Skiers", "Snowplay", "Summer Activity", "Other"],
        "Visitors": [
            int(base_year_visitors * skier_pct / 100),
            int(base_year_visitors * snowplay_pct / 100),
            int(base_year_visitors * summer_activity_pct / 100),
            int(base_year_visitors * other_segment_pct / 100),
        ]
    }
    fig_segment = px.bar(
        segment_data,
        x="Segment",
        y="Visitors",
        title="Visitor Segment Distribution"
    )
    st.plotly_chart(fig_segment, use_container_width=True)

with segment_col2:
    st.subheader("Summary Statistics")
    summary_stats = {
        "Metric": [
            "Base Year Visitors",
            "Year 10 Visitors",
            "Total Growth",
            "Annual Growth Rate",
            "Average Annual Visitors",
            "Peak Year Visitors",
        ],
        "Value": [
            f"{int(base_year_visitors):,}",
            f"{int(forecast_df.iloc[-1]['Total Visitors']):,}",
            f"{((forecast_df.iloc[-1]['Total Visitors'] / base_year_visitors - 1) * 100):.1f}%",
            f"{annual_growth_rate:.1f}%",
            f"{forecast_df['Total Visitors'].mean():,.0f}",
            f"{forecast_df['Total Visitors'].max():,}",
        ]
    }
    summary_stats_df = pd.DataFrame(summary_stats)
    st.dataframe(summary_stats_df, hide_index=True, use_container_width=True)

st.success(
    "✅ Demand forecast saved to session! Use these projections in Revenue and Expense forecasts."
)
