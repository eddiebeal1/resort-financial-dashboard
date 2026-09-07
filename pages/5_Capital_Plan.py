import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Capital Plan",
    page_icon="🏗️",
    layout="wide",
)

st.title("🏗️ Capital Plan")
st.markdown("Plan and track capital investments and infrastructure improvements")

# Initialize session state
if "capital_plan" not in st.session_state:
    st.session_state.capital_plan = {}

st.markdown("---")

st.subheader("Capital Projects")
st.info("Add capital investment projects across your 10-year planning horizon")

# Capital project input
cap_col1, cap_col2, cap_col3, cap_col4 = st.columns(4)

with cap_col1:
    project_name = st.text_input(
        "Project Name",
        placeholder="e.g., Lift Modernization",
        key="project_name_input"
    )

with cap_col2:
    total_cost = st.number_input(
        "Total Project Cost ($)",
        min_value=0,
        value=500000,
        step=50000,
        key="project_cost_input"
    )

with cap_col3:
    start_year = st.number_input(
        "Start Year",
        min_value=0,
        max_value=9,
        value=0,
        key="project_start_input"
    )

with cap_col4:
    duration = st.number_input(
        "Duration (Years)",
        min_value=1,
        max_value=5,
        value=1,
        key="project_duration_input"
    )

# Depreciation input
depr_col1, depr_col2 = st.columns(2)

with depr_col1:
    useful_life = st.number_input(
        "Useful Life (Years)",
        min_value=1,
        max_value=50,
        value=10,
        key="project_life_input"
    )

with depr_col2:
    depreciation_method = st.selectbox(
        "Depreciation Method",
        ["Straight Line", "Accelerated (150% Declining Balance)"],
        key="depr_method_input"
    )

add_project = st.button("Add Project", use_container_width=True)

if add_project and project_name:
    if "projects" not in st.session_state:
        st.session_state.projects = []
    
    st.session_state.projects.append({
        "name": project_name,
        "cost": total_cost,
        "start_year": start_year,
        "duration": duration,
        "useful_life": useful_life,
        "depreciation_method": depreciation_method,
    })
    st.success(f"✅ Project '{project_name}' added!")

st.markdown("---")

# Display existing projects
if "projects" in st.session_state and st.session_state.projects:
    st.subheader("Capital Projects Summary")
    
    projects_display = []
    for proj in st.session_state.projects:
        projects_display.append({
            "Project": proj["name"],
            "Cost": f"${proj['cost']:,.0f}",
            "Start Year": proj["start_year"],
            "Duration": f"{proj['duration']} yr(s)",
            "Life": f"{proj['useful_life']} yrs",
        })
    
    projects_df = pd.DataFrame(projects_display)
    st.dataframe(projects_df, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Calculate annual capex schedule
    st.subheader("Annual Capital Expenditure Schedule")
    
    capex_schedule = {f"Year {i}": 0 for i in range(10)}
    depreciation_schedule = {f"Year {i}": 0 for i in range(10)}
    
    for proj in st.session_state.projects:
        annual_capex = proj["cost"] / proj["duration"]
        
        for year in range(proj["start_year"], min(proj["start_year"] + proj["duration"], 10)):
            capex_schedule[f"Year {year}"] += annual_capex
        
        # Calculate depreciation
        start_depreciation = proj["start_year"] + proj["duration"]
        if proj["depreciation_method"] == "Straight Line":
            annual_depreciation = proj["cost"] / proj["useful_life"]
            for year in range(start_depreciation, min(start_depreciation + proj["useful_life"], 10)):
                depreciation_schedule[f"Year {year}"] += annual_depreciation
        else:  # Accelerated
            rate = 1.5 / proj["useful_life"]
            book_value = proj["cost"]
            for year in range(start_depreciation, 10):
                if book_value > 0:
                    depr = book_value * rate
                    depreciation_schedule[f"Year {year}"] += depr
                    book_value -= depr
    
    # Create capex display
    capex_data = []
    for year in range(10):
        capex_data.append({
            "Year": year,
            "Capital Expenditure": capex_schedule[f"Year {year}"],
            "Depreciation Expense": depreciation_schedule[f"Year {year}"],
        })
    
    capex_df = pd.DataFrame(capex_data)
    
    display_capex = capex_df.copy()
    for col in ["Capital Expenditure", "Depreciation Expense"]:
        display_capex[col] = display_capex[col].apply(lambda x: f"${x:,.0f}")
    
    st.dataframe(display_capex, hide_index=True, use_container_width=True)
    
    st.markdown("---")
    
    # Visualizations
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.subheader("Annual Capital Expenditure")
        fig_capex = px.bar(
            capex_df,
            x="Year",
            y="Capital Expenditure",
            title="Annual Capex Schedule",
        )
        fig_capex.update_yaxes(title="Capex ($)")
        fig_capex.update_xaxes(title="Year")
        st.plotly_chart(fig_capex, use_container_width=True)
    
    with viz_col2:
        st.subheader("Depreciation Expense")
        fig_depr = px.bar(
            capex_df,
            x="Year",
            y="Depreciation Expense",
            title="Annual Depreciation Expense",
        )
        fig_depr.update_yaxes(title="Depreciation ($)")
        fig_depr.update_xaxes(title="Year")
        st.plotly_chart(fig_depr, use_container_width=True)
    
    st.markdown("---")
    
    # Summary metrics
    st.subheader("Capital Plan Summary")
    summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
    
    total_capex = capex_df["Capital Expenditure"].sum()
    peak_capex_year = capex_df.loc[capex_df["Capital Expenditure"].idxmax(), "Year"]
    peak_capex = capex_df["Capital Expenditure"].max()
    total_depr = capex_df["Depreciation Expense"].sum()
    
    with summary_col1:
        st.metric("Total 10-Year Capex", f"${total_capex/1e6:.1f}M")
    
    with summary_col2:
        st.metric("Peak Capex Year", f"Year {int(peak_capex_year)}: ${peak_capex/1e6:.1f}M")
    
    with summary_col3:
        st.metric("Total Depreciation", f"${total_depr/1e6:.1f}M")
    
    with summary_col4:
        st.metric("Avg Annual Capex", f"${total_capex/10/1e6:.1f}M")

else:
    st.info("📌 Add capital projects to begin planning your infrastructure investments.")

st.markdown("---")

# Common capex templates
st.subheader("Common Capital Projects (Templates)")

template_col1, template_col2, template_col3 = st.columns(3)

templates = {
    "Lift System Upgrade": 2500000,
    "Base Lodge Renovation": 1500000,
    "Snow Making Equipment": 800000,
    "Terrain Development": 1200000,
    "IT Infrastructure": 300000,
    "Fleet Vehicles": 400000,
}

for i, (template_name, template_cost) in enumerate(templates.items()):
    if i % 3 == 0:
        col = template_col1
    elif i % 3 == 1:
        col = template_col2
    else:
        col = template_col3
    
    with col:
        if st.button(f"Use: {template_name} (${template_cost/1e6:.1f}M)", use_container_width=True):
            if "projects" not in st.session_state:
                st.session_state.projects = []
            
            st.session_state.projects.append({
                "name": template_name,
                "cost": template_cost,
                "start_year": 0,
                "duration": 1,
                "useful_life": 10,
                "depreciation_method": "Straight Line",
            })
            st.rerun()

st.success("✅ Capital plan data ready for use in financial projections.")
