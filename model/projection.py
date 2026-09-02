import numpy as np
import pandas as pd

from model.assumptions import ModelAssumptions


def straight_line_ramp(
    baseline_value: float,
    target_value: float,
    periods: int,
) -> np.ndarray:
    """
    Produce a straight-line progression from baseline to target.
    The returned array includes the baseline period.
    """
    return np.linspace(
        baseline_value,
        target_value,
        periods + 1,
    )


def build_projection(
    assumptions: ModelAssumptions,
    forecast_years: int = 10,
) -> pd.DataFrame:
    """
    Build a baseline plus 10-year resort financial projection.
    """

    years = np.arange(0, forecast_years + 1)

    skier_visits = (
        assumptions.baseline_skier_visits
        * (1 + assumptions.annual_visit_growth) ** years
    )

    ticket_revenue_per_visit = straight_line_ramp(
        assumptions.baseline_ticket_revenue_per_visit,
        assumptions.target_ticket_revenue_per_visit,
        forecast_years,
    )

    ancillary_revenue_per_visit = straight_line_ramp(
        assumptions.baseline_ancillary_revenue_per_visit,
        assumptions.target_ancillary_revenue_per_visit,
        forecast_years,
    )

    variable_expense_per_visit = straight_line_ramp(
        assumptions.baseline_variable_expense_per_visit,
        assumptions.target_variable_expense_per_visit,
        forecast_years,
    )

    ticket_revenue = (
        skier_visits
        * ticket_revenue_per_visit
    )

    ancillary_revenue = (
        skier_visits
        * ancillary_revenue_per_visit
    )

    total_revenue = (
        ticket_revenue
        + ancillary_revenue
    )

    variable_expense = (
        skier_visits
        * variable_expense_per_visit
    )

    fixed_expense = (
        assumptions.baseline_fixed_expense
        * (1 + assumptions.annual_fixed_expense_growth) ** years
    )

    total_operating_expense = (
        variable_expense
        + fixed_expense
    )

    ebitda = (
        total_revenue
        - total_operating_expense
    )

    ebitda_margin = np.divide(
        ebitda,
        total_revenue,
        out=np.zeros_like(ebitda),
        where=total_revenue != 0,
    )

    capex = np.zeros(forecast_years + 1)

    if forecast_years >= 1:
        capex[1] = assumptions.capex_year_1

    if forecast_years >= 2:
        capex[2] = assumptions.capex_year_2

    if forecast_years >= 3:
        capex[3] = assumptions.capex_year_3

    taxable_income = np.maximum(
        ebitda,
        0,
    )

    taxes = (
        taxable_income
        * assumptions.tax_rate
    )

    operating_cash_flow = (
        ebitda
        - taxes
    )

    free_cash_flow = (
        operating_cash_flow
        - capex
    )

    cumulative_free_cash_flow = (
        np.cumsum(free_cash_flow)
    )

    projection = pd.DataFrame(
        {
            "Year Number": years,
            "Period": [
                "Baseline" if year == 0 else f"Year {year}"
                for year in years
            ],
            "Skier Visits": skier_visits,
            "Ticket Revenue per Visit": ticket_revenue_per_visit,
            "Ancillary Revenue per Visit": ancillary_revenue_per_visit,
            "Total Revenue per Visit": (
                ticket_revenue_per_visit
                + ancillary_revenue_per_visit
            ),
            "Ticket Revenue": ticket_revenue,
            "Ancillary Revenue": ancillary_revenue,
            "Total Revenue": total_revenue,
            "Variable Expense per Visit": variable_expense_per_visit,
            "Variable Expense": variable_expense,
            "Fixed Expense": fixed_expense,
            "Operating Expense": total_operating_expense,
            "EBITDA": ebitda,
            "EBITDA Margin": ebitda_margin,
            "Taxes": taxes,
            "Operating Cash Flow": operating_cash_flow,
            "Capital Investment": capex,
            "Free Cash Flow": free_cash_flow,
            "Cumulative Free Cash Flow": cumulative_free_cash_flow,
        }
    )

    return projection