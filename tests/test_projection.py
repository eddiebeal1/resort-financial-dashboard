from model.assumptions import ModelAssumptions
from model.projection import build_projection


def test_projection_has_baseline_plus_ten_years():
    assumptions = ModelAssumptions(
        scenario_name="Test",
        baseline_skier_visits=100_000,
        baseline_ticket_revenue_per_visit=50,
        baseline_ancillary_revenue_per_visit=20,
        baseline_variable_expense_per_visit=30,
        baseline_fixed_expense=2_000_000,
        annual_visit_growth=0.02,
        target_ticket_revenue_per_visit=60,
        target_ancillary_revenue_per_visit=25,
        target_variable_expense_per_visit=35,
        annual_fixed_expense_growth=0.025,
        capex_year_1=5_000_000,
        capex_year_2=0,
        capex_year_3=0,
        tax_rate=0.25,
        discount_rate=0.10,
        terminal_growth_rate=0.025,
        exit_ebitda_multiple=8,
    )

    projection = build_projection(
        assumptions
    )

    assert len(projection) == 11

    assert (
        projection.iloc[0]["Period"]
        == "Baseline"
    )

    assert (
        projection.iloc[-1]["Period"]
        == "Year 10"
    )


def test_revenue_equals_component_sum():
    assumptions = ModelAssumptions(
        scenario_name="Test",
        baseline_skier_visits=100_000,
        baseline_ticket_revenue_per_visit=50,
        baseline_ancillary_revenue_per_visit=20,
        baseline_variable_expense_per_visit=30,
        baseline_fixed_expense=2_000_000,
        annual_visit_growth=0.02,
        target_ticket_revenue_per_visit=60,
        target_ancillary_revenue_per_visit=25,
        target_variable_expense_per_visit=35,
        annual_fixed_expense_growth=0.025,
        capex_year_1=5_000_000,
        capex_year_2=0,
        capex_year_3=0,
        tax_rate=0.25,
        discount_rate=0.10,
        terminal_growth_rate=0.025,
        exit_ebitda_multiple=8,
    )

    projection = build_projection(
        assumptions
    )

    calculated_revenue = (
        projection["Ticket Revenue"]
        + projection["Ancillary Revenue"]
    )

    difference = (
        projection["Total Revenue"]
        - calculated_revenue
    ).abs().max()

    assert difference < 0.01