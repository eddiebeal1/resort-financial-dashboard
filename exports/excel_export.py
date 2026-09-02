from io import BytesIO

import pandas as pd


def create_excel_export(
    assumptions: dict,
    projection: pd.DataFrame,
    metrics: dict,
) -> bytes:
    output = BytesIO()

    assumptions_df = pd.DataFrame(
        list(assumptions.items()),
        columns=["Assumption", "Value"],
    )

    metrics_df = pd.DataFrame(
        list(metrics.items()),
        columns=["Metric", "Value"],
    )

    with pd.ExcelWriter(
        output,
        engine="openpyxl",
    ) as writer:
        assumptions_df.to_excel(
            writer,
            sheet_name="Assumptions",
            index=False,
        )

        projection.to_excel(
            writer,
            sheet_name="10-Year Projection",
            index=False,
        )

        metrics_df.to_excel(
            writer,
            sheet_name="Summary Metrics",
            index=False,
        )

        for sheet_name in writer.sheets:
            worksheet = writer.sheets[sheet_name]
            worksheet.freeze_panes = "A2"

            for column_cells in worksheet.columns:
                maximum_length = max(
                    len(str(cell.value))
                    if cell.value is not None
                    else 0
                    for cell in column_cells
                )

                worksheet.column_dimensions[
                    column_cells[0].column_letter
                ].width = min(
                    maximum_length + 2,
                    35,
                )

    output.seek(0)
    return output.getvalue()