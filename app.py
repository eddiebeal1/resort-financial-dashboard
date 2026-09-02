import streamlit as st

from components.charts import (
    cash_flow_chart,
    financial_performance_chart,
    per_visit_chart,
    visitation_chart,
)
from components.inputs import render_assumption_inputs
from components.metrics import render_summary_metrics
from exports.excel_export import create_excel_export
from model.projection import build_projection
from model.validation import validate_assumptions
from model.valuation import calculate_summary_metrics


st.set_page_config(
    page_title="Resort Financial Model",
    page_icon="🏔️",
    layout="wide",
)

st.title("Resort Financial Model")
st.caption(
    "Interactive baseline, capital program, "
    "10-year projection, and valuation dashboard"
)

assumptions = render_assumption_inputs()

validation_errors = validate_assumptions(
    assumptions
)

if validation_errors:
    st.error(
        "Correct the following assumptions before "
        "reviewing the results:"
    )

    for error in validation_errors:
        st.write(f"- {error}")

    st.stop()

projection = build_projection(
    assumptions
)

metrics = calculate_summary_metrics(
    projection,
    assumptions,
)

st.subheader(assumptions.scenario_name)

render_summary_metrics(metrics)

dashboard_tab, detail_tab, valuation_tab = st.tabs(
    [
        "Executive Dashboard",
        "Model Detail",
        "Valuation",
    ]
)

with dashboard_tab:
    chart_col_1, chart_col_2 = st.columns(2)

    with chart_col_1:
        st.plotly_chart(
            financial_performance_chart(
                projection
            ),
            use_container_width=True,
        )

    with chart_col_2:
        st.plotly_chart(
            visitation_chart(
                projection
            ),
            use_container_width=True,
        )

    chart_col_3, chart_col_4 = st.columns(2)

    with chart_col_3:
        st.plotly_chart(
            per_visit_chart(
                projection
            ),
            use_container_width=True,
        )

    with chart_col_4:
        st.plotly_chart(
            cash_flow_chart(
                projection
            ),
            use_container_width=True,
        )

with detail_tab:
    st.subheader(
        "Baseline Through Year 10"
    )

    display_projection = projection.copy()

    currency_columns = [
        "Ticket Revenue per Visit",
        "Ancillary Revenue per Visit",
        "Total Revenue per Visit",
        "Ticket Revenue",
        "Ancillary Revenue",
        "Total Revenue",
        "Variable Expense per Visit",
        "Variable Expense",
        "Fixed Expense",
        "Operating Expense",
        "EBITDA",
        "Taxes",
        "Operating Cash Flow",
        "Capital Investment",
        "Free Cash Flow",
        "Cumulative Free Cash Flow",
    ]

    column_configuration = {
        column: st.column_config.NumberColumn(
            column,
            format="$%.0f",
        )
        for column in currency_columns
    }

    column_configuration[
        "Skier Visits"
    ] = st.column_config.NumberColumn(
        "Skier Visits",
        format="%.0f",
    )

    column_configuration[
        "EBITDA Margin"
    ] = st.column_config.NumberColumn(
        "EBITDA Margin",
        format="percent",
    )

    st.dataframe(
        display_projection,
        column_config=column_configuration,
        hide_index=True,
        use_container_width=True,
    )

with valuation_tab:
    valuation_col_1, valuation_col_2 = (
        st.columns(2)
    )

    valuation_col_1.metric(
        "Gordon Growth Enterprise Value",
        (
            "N/M"
            if metrics["Gordon Enterprise Value"] is None
            else f"${metrics['Gordon Enterprise Value']:,.0f}"
        ),
    )

    valuation_col_2.metric(
        "Exit Multiple Enterprise Value",
        f"${metrics['Exit Enterprise Value']:,.0f}",
    )

    st.write(
        "The 10-year NPV excludes terminal value. "
        "The enterprise value measures add the "
        "present value of the applicable terminal value."
    )

excel_file = create_excel_export(
    assumptions.to_dict(),
    projection,
    metrics,
)

st.download_button(
    label="Download Model to Excel",
    data=excel_file,
    file_name=(
        f"{assumptions.scenario_name}"
        .lower()
        .replace(" ", "_")
        + ".xlsx"
    ),
    mime=(
        "application/vnd.openxmlformats-officedocument."
        "spreadsheetml.sheet"
    ),
)