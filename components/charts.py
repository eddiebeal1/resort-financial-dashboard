import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def financial_performance_chart(
    projection: pd.DataFrame,
):
    chart_data = projection.melt(
        id_vars=["Period"],
        value_vars=[
            "Total Revenue",
            "Operating Expense",
            "EBITDA",
        ],
        var_name="Metric",
        value_name="Value",
    )

    figure = px.line(
        chart_data,
        x="Period",
        y="Value",
        color="Metric",
        markers=True,
        title="Financial Performance",
    )

    figure.update_layout(
        yaxis_title="USD",
        xaxis_title=None,
        legend_title=None,
        hovermode="x unified",
    )

    return figure


def visitation_chart(
    projection: pd.DataFrame,
):
    figure = px.line(
        projection,
        x="Period",
        y="Skier Visits",
        markers=True,
        title="Skier Visit Projection",
    )

    figure.update_layout(
        xaxis_title=None,
        yaxis_title="Skier Visits",
        hovermode="x unified",
    )

    return figure


def per_visit_chart(
    projection: pd.DataFrame,
):
    chart_data = projection.melt(
        id_vars=["Period"],
        value_vars=[
            "Ticket Revenue per Visit",
            "Ancillary Revenue per Visit",
            "Variable Expense per Visit",
        ],
        var_name="Metric",
        value_name="Value",
    )

    figure = px.line(
        chart_data,
        x="Period",
        y="Value",
        color="Metric",
        markers=True,
        title="Per-Visit Performance",
    )

    figure.update_layout(
        xaxis_title=None,
        yaxis_title="USD per visit",
        legend_title=None,
        hovermode="x unified",
    )

    return figure


def cash_flow_chart(
    projection: pd.DataFrame,
):
    figure = go.Figure()

    figure.add_bar(
        x=projection["Period"],
        y=-projection["Capital Investment"],
        name="Capital Investment",
    )

    figure.add_bar(
        x=projection["Period"],
        y=projection["Free Cash Flow"],
        name="Free Cash Flow",
    )

    figure.add_scatter(
        x=projection["Period"],
        y=projection["Cumulative Free Cash Flow"],
        name="Cumulative Free Cash Flow",
        mode="lines+markers",
    )

    figure.update_layout(
        title="Capital Investment and Cash Flow",
        xaxis_title=None,
        yaxis_title="USD",
        hovermode="x unified",
    )

    return figure