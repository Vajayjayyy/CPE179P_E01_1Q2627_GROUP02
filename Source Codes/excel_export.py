from io import BytesIO
import pandas as pd

def create_excel_report(records: list[dict]) -> bytes:
    columns = [
        "filename", "recognized_code", "iso6346_valid", "check_digit_valid",
        "message", "trocr_full_image_text"
    ]
    rows = []
    for record in records:
        rows.append({column: record.get(column, "") for column in columns})
    frame = pd.DataFrame(rows, columns=columns)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        frame.to_excel(writer, index=False, sheet_name="OCR Results")
        worksheet = writer.sheets["OCR Results"]
        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions
        for column_cells in worksheet.columns:
            max_length = max(len(str(cell.value or "")) for cell in column_cells)
            worksheet.column_dimensions[column_cells[0].column_letter].width = min(max_length + 2, 55)
    return output.getvalue()
