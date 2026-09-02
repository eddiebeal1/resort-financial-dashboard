from dataclasses import dataclass, asdict


@dataclass
class ModelAssumptions:
    scenario_name: str

    # Baseline operating assumptions
    baseline_skier_visits: float
    baseline_ticket_revenue_per_visit: float
    baseline_ancillary_revenue_per_visit: float
    baseline_variable_expense_per_visit: float
    baseline_fixed_expense: float

    # Forecast assumptions
    annual_visit_growth: float
    target_ticket_revenue_per_visit: float
    target_ancillary_revenue_per_visit: float
    target_variable_expense_per_visit: float
    annual_fixed_expense_growth: float

    # Capital assumptions
    capex_year_1: float
    capex_year_2: float
    capex_year_3: float

    # Cash flow and valuation assumptions
    tax_rate: float
    discount_rate: float
    terminal_growth_rate: float
    exit_ebitda_multiple: float

    def to_dict(self):
        return asdict(self)