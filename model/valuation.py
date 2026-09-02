import math

import numpy as np
import numpy_financial as npf
import pandas as pd

from model.assumptions import ModelAssumptions


def calculate_npv(
    projection: pd.DataFrame,
    discount_rate: float,
) -> float:
    """
    Calculate the present value of Years 1 through 10 free cash flow.
    Baseline is excluded.
    """
    forecast_cash_flows = (
        projection.loc[
            projection["Year Number"] >= 1,
            "Free Cash Flow",
        ]
        .astype(float)
        .to_numpy()
    )

    return float(
        sum(
            cash_flow / ((1 + discount_rate) ** year)
            for year, cash_flow in enumerate(
                forecast_cash_flows,
                start=1,
            )
        )
    )


def calculate_irr(
    projection: pd.DataFrame,
) -> float | None:
    """
    Calculate IRR only when the cash-flow series contains
    at least one positive and one negative value.
    """
    forecast_cash_flows = (
        projection.loc[
            projection["Year Number"] >= 1,
            "Free Cash Flow",
        ]
        .astype(float)
        .to_numpy()
    )

    has_positive = np.any(forecast_cash_flows > 0)
    has_negative = np.any(forecast_cash_flows < 0)

    if not has_positive or not has_negative:
        return None

    irr = npf.irr(forecast_cash_flows)

    if irr is None or not np.isfinite(irr):
        return None

    return float(irr)


def calculate_payback_year(
    projection: pd.DataFrame,
) -> str:
    """
    Return the first forecast period in which cumulative
    free cash flow is nonnegative.
    """
    forecast = projection[
        projection["Year Number"] >= 1
    ]

    payback = forecast[
        forecast["Cumulative Free Cash Flow"] >= 0
    ]

    if payback.empty:
        return "Beyond Year 10"

    return str(payback.iloc[0]["Period"])


def calculate_terminal_values(
    projection: pd.DataFrame,
    assumptions: ModelAssumptions,
) -> dict:
    year_10 = projection.iloc[-1]

    year_10_fcf = float(
        year_10["Free Cash Flow"]
    )

    year_10_ebitda = float(
        year_10["EBITDA"]
    )

    if (
        assumptions.terminal_growth_rate
        >= assumptions.discount_rate
    ):
        gordon_terminal_value = None
        gordon_terminal_value_pv = None
    else:
        gordon_terminal_value = (
            year_10_fcf
            * (1 + assumptions.terminal_growth_rate)
            / (
                assumptions.discount_rate
                - assumptions.terminal_growth_rate
            )
        )

        gordon_terminal_value_pv = (
            gordon_terminal_value
            / ((1 + assumptions.discount_rate) ** 10)
        )

    exit_terminal_value = (
        year_10_ebitda
        * assumptions.exit_ebitda_multiple
    )

    exit_terminal_value_pv = (
        exit_terminal_value
        / ((1 + assumptions.discount_rate) ** 10)
    )

    operating_npv = calculate_npv(
        projection,
        assumptions.discount_rate,
    )

    return {
        "Operating NPV": operating_npv,
        "Gordon Terminal Value": gordon_terminal_value,
        "Gordon Terminal Value PV": gordon_terminal_value_pv,
        "Gordon Enterprise Value": (
            None
            if gordon_terminal_value_pv is None
            else operating_npv + gordon_terminal_value_pv
        ),
        "Exit Terminal Value": exit_terminal_value,
        "Exit Terminal Value PV": exit_terminal_value_pv,
        "Exit Enterprise Value": (
            operating_npv + exit_terminal_value_pv
        ),
    }


def calculate_summary_metrics(
    projection: pd.DataFrame,
    assumptions: ModelAssumptions,
) -> dict:
    year_10 = projection.iloc[-1]

    irr = calculate_irr(projection)
    valuation = calculate_terminal_values(
        projection,
        assumptions,
    )

    return {
        "Year 10 Revenue": float(
            year_10["Total Revenue"]
        ),
        "Year 10 EBITDA": float(
            year_10["EBITDA"]
        ),
        "Year 10 EBITDA Margin": float(
            year_10["EBITDA Margin"]
        ),
        "Cumulative Capital Investment": float(
            projection["Capital Investment"].sum()
        ),
        "10-Year NPV": valuation["Operating NPV"],
        "IRR": irr,
        "Payback Period": calculate_payback_year(
            projection
        ),
        **valuation,
    }