from model.assumptions import ModelAssumptions


def validate_assumptions(
    assumptions: ModelAssumptions,
) -> list:
    errors = []

    if assumptions.baseline_skier_visits <= 0:
        errors.append(
            "Baseline skier visits must be greater than zero."
        )

    if assumptions.discount_rate <= 0:
        errors.append(
            "The discount rate must be greater than zero."
        )

    if (
        assumptions.terminal_growth_rate
        >= assumptions.discount_rate
    ):
        errors.append(
            "Terminal growth must be below the discount rate."
        )

    if not 0 <= assumptions.tax_rate <= 1:
        errors.append(
            "Tax rate must be between 0% and 100%."
        )

    if assumptions.exit_ebitda_multiple < 0:
        errors.append(
            "The exit EBITDA multiple cannot be negative."
        )

    revenue_inputs = [
        assumptions.baseline_ticket_revenue_per_visit,
        assumptions.baseline_ancillary_revenue_per_visit,
        assumptions.target_ticket_revenue_per_visit,
        assumptions.target_ancillary_revenue_per_visit,
    ]

    if any(value < 0 for value in revenue_inputs):
        errors.append(
            "Revenue per visit assumptions cannot be negative."
        )

    expense_inputs = [
        assumptions.baseline_variable_expense_per_visit,
        assumptions.baseline_fixed_expense,
        assumptions.target_variable_expense_per_visit,
    ]

    if any(value < 0 for value in expense_inputs):
        errors.append(
            "Expense assumptions cannot be negative."
        )

    capex_inputs = [
        assumptions.capex_year_1,
        assumptions.capex_year_2,
        assumptions.capex_year_3,
    ]

    if any(value < 0 for value in capex_inputs):
        errors.append(
            "Capital investment cannot be negative."
        )

    return errors