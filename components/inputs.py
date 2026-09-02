import streamlit as st

from model.assumptions import ModelAssumptions


def render_assumption_inputs() -> ModelAssumptions:
    st.sidebar.header("Model Assumptions")

    scenario_name = st.sidebar.text_input(
        "Scenario name",
        value="Base Scenario",
    )

    with st.sidebar.expander(
        "1. Baseline",
        expanded=True,
    ):
        baseline_skier_visits = st.number_input(
            "Baseline skier visits",
            min_value=0,
            value=150_000,
            step=5_000,
        )

        baseline_ticket_revenue_per_visit = (
            st.number_input(
                "Ticket revenue per skier visit",
                min_value=0.0,
                value=65.0,
                step=1.0,
            )
        )

        baseline_ancillary_revenue_per_visit = (
            st.number_input(
                "Ancillary revenue per skier visit",
                min_value=0.0,
                value=25.0,
                step=1.0,
            )
        )

        baseline_variable_expense_per_visit = (
            st.number_input(
                "Variable expense per skier visit",
                min_value=0.0,
                value=35.0,
                step=1.0,
            )
        )

        baseline_fixed_expense = st.number_input(
            "Baseline fixed expense",
            min_value=0.0,
            value=4_000_000.0,
            step=100_000.0,
        )

    with st.sidebar.expander(
        "2. Forecast Drivers",
        expanded=True,
    ):
        annual_visit_growth = (
            st.slider(
                "Annual skier visit growth",
                min_value=-10.0,
                max_value=20.0,
                value=2.0,
                step=0.5,
            )
            / 100
        )

        target_ticket_revenue_per_visit = (
            st.number_input(
                "Year 10 ticket revenue per visit",
                min_value=0.0,
                value=85.0,
                step=1.0,
            )
        )

        target_ancillary_revenue_per_visit = (
            st.number_input(
                "Year 10 ancillary revenue per visit",
                min_value=0.0,
                value=40.0,
                step=1.0,
            )
        )

        target_variable_expense_per_visit = (
            st.number_input(
                "Year 10 variable expense per visit",
                min_value=0.0,
                value=42.0,
                step=1.0,
            )
        )

        annual_fixed_expense_growth = (
            st.slider(
                "Annual fixed expense growth",
                min_value=0.0,
                max_value=10.0,
                value=2.5,
                step=0.5,
            )
            / 100
        )

    with st.sidebar.expander(
        "3. Capital Program",
        expanded=False,
    ):
        capex_year_1 = st.number_input(
            "Year 1 capital investment",
            min_value=0.0,
            value=10_000_000.0,
            step=500_000.0,
        )

        capex_year_2 = st.number_input(
            "Year 2 capital investment",
            min_value=0.0,
            value=5_000_000.0,
            step=500_000.0,
        )

        capex_year_3 = st.number_input(
            "Year 3 capital investment",
            min_value=0.0,
            value=0.0,
            step=500_000.0,
        )

    with st.sidebar.expander(
        "4. Valuation",
        expanded=False,
    ):
        tax_rate = (
            st.slider(
                "Tax rate",
                min_value=0.0,
                max_value=50.0,
                value=25.0,
                step=1.0,
            )
            / 100
        )

        discount_rate = (
            st.slider(
                "Discount rate",
                min_value=1.0,
                max_value=20.0,
                value=10.0,
                step=0.5,
            )
            / 100
        )

        terminal_growth_rate = (
            st.slider(
                "Terminal growth rate",
                min_value=0.0,
                max_value=8.0,
                value=2.5,
                step=0.5,
            )
            / 100
        )

        exit_ebitda_multiple = st.number_input(
            "Exit EBITDA multiple",
            min_value=0.0,
            value=8.0,
            step=0.5,
        )

    return ModelAssumptions(
        scenario_name=scenario_name,
        baseline_skier_visits=float(
            baseline_skier_visits
        ),
        baseline_ticket_revenue_per_visit=float(
            baseline_ticket_revenue_per_visit
        ),
        baseline_ancillary_revenue_per_visit=float(
            baseline_ancillary_revenue_per_visit
        ),
        baseline_variable_expense_per_visit=float(
            baseline_variable_expense_per_visit
        ),
        baseline_fixed_expense=float(
            baseline_fixed_expense
        ),
        annual_visit_growth=float(
            annual_visit_growth
        ),
        target_ticket_revenue_per_visit=float(
            target_ticket_revenue_per_visit
        ),
        target_ancillary_revenue_per_visit=float(
            target_ancillary_revenue_per_visit
        ),
        target_variable_expense_per_visit=float(
            target_variable_expense_per_visit
        ),
        annual_fixed_expense_growth=float(
            annual_fixed_expense_growth
        ),
        capex_year_1=float(capex_year_1),
        capex_year_2=float(capex_year_2),
        capex_year_3=float(capex_year_3),
        tax_rate=float(tax_rate),
        discount_rate=float(discount_rate),
        terminal_growth_rate=float(
            terminal_growth_rate
        ),
        exit_ebitda_multiple=float(
            exit_ebitda_multiple
        ),
    )