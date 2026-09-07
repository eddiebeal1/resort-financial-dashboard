import streamlit as st

# Configure page
st.set_page_config(
    page_title="Resort Financial Dashboard V2",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add custom styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("🏔️ Resort Financial Dashboard V2")
st.sidebar.markdown("---")

st.markdown("""
    <div class="main-header">Resort Financial Dashboard V2</div>
    <div class="sub-header">Comprehensive Financial Planning & Analysis Tool</div>
""", unsafe_allow_html=True)

# Home content
st.markdown("""
## Welcome to Your Financial Planning Suite

This enhanced dashboard provides comprehensive tools for resort financial planning and analysis.

### 📊 Available Tools

Navigate using the sidebar to access:

1. **Financial Summary** - Overview of key financial metrics and KPIs
2. **Demand Forecast** - Project visitor volumes based on your inputs
3. **Revenue Forecast** - Model revenue by category (Tickets, Food & Beverage, Retail, etc.)
4. **Expense Forecast** - Estimate operating expenses with fixed/variable cost breakdown
5. **Capital Plan** - Plan and track capital investments
6. **Funding Strategy** - Evaluate financing options and capital structures
7. **Scenario Builder** - Compare multiple financial scenarios side-by-side
8. **Risk Analysis** - Monte Carlo simulations and sensitivity analysis

### 🚀 Quick Start

1. Start with **Demand Forecast** to project visitor volumes
2. Move to **Revenue Forecast** to estimate income streams
3. Model expenses in **Expense Forecast**
4. Use **Scenario Builder** to compare different assumptions
5. Run **Risk Analysis** to understand downside scenarios

### 📈 Features

- Interactive input forms for dynamic projections
- Real-time calculations and visualizations
- Multi-scenario comparison capabilities
- Statistical risk analysis (Monte Carlo, sensitivity)
- Export capabilities for further analysis

---

**Version 2.0** | Enhanced Financial Planning Suite
""")

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Tip**: Start with Demand Forecast to establish visitor volume projections, "
    "then model revenue and expenses based on those volumes."
)
