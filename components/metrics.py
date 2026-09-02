import streamlit as st


def format_currency(value: float | None) -> str:
    if value is None:
        return "N/M"

    if value < 0:
        return f"(${abs(value):,.0f})"

    return f"${value:,.0f}"


def format_percentage(value: float | None) -> str:
    if value is None:
        return "N/M"

    return f"{value:.1%}"


def render_summary_metrics(metrics: dict) -> None:
    row_1 = st.columns(4)

    row_1[0].metric(
        "Year 10 Revenue",
        format_currency(
            metrics["Year 10 Revenue"]
        ),
    )

    row_1[1].metric(
        "Year 10 EBITDA",
        format_currency(
            metrics["Year 10 EBITDA"]
        ),
    )

    row_1[2].metric(
        "EBITDA Margin",
        format_percentage(
            metrics["Year 10 EBITDA Margin"]
        ),
    )

    row_1[3].metric(
        "Capital Investment",
        format_currency(
            metrics["Cumulative Capital Investment"]
        ),
    )

    row_2 = st.columns(4)

    row_2[0].metric(
        "10-Year NPV",
        format_currency(
            metrics["10-Year NPV"]
        ),
    )

    row_2[1].metric(
        "IRR",
        format_percentage(
            metrics["IRR"]
        ),
    )

    row_2[2].metric(
        "Payback",
        metrics["Payback Period"],
    )

    row_2[3].metric(
        "Gordon Growth EV",
        format_currency(
            metrics["Gordon Enterprise Value"]
        ),
    )