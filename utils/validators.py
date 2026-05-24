# utils/validators.py
# Validation logic for column mapping, data quality, and aging buckets

import pandas as pd
from datetime import date


def validate_column_mapping(mapping: dict, use_batch: bool) -> list:
    """
    Validate that all mandatory columns are mapped.
    Returns list of error messages.
    """
    errors = []
    mandatory = ["material_index", "receipt_date", "material_name", "doc_number", "quantity"]
    for col in mandatory:
        if not mapping.get(col):
            errors.append(col)
    if use_batch and not mapping.get("batch"):
        errors.append("batch")
    return errors


def validate_data(df: pd.DataFrame, mapping: dict, aging_date: date, use_batch: bool, t: dict) -> list:
    """
    Validate data quality. Returns list of validation log entries:
    {"row": int, "type": str, "description": str, "severity": str}
    """
    issues = []

    qty_col = mapping.get("quantity")
    date_col = mapping.get("receipt_date")
    batch_col = mapping.get("batch")
    idx_col = mapping.get("material_index")

    for i, row in df.iterrows():
        row_num = i + 2  # Excel-style row number (1-indexed + header)

        # Check receipt date
        if date_col:
            val = row.get(date_col)
            if pd.isna(val) or val is None:
                issues.append({
                    "row": row_num,
                    "type": "MISSING_DATE" if t.get("severity_error") == "BŁĄD" else "MISSING_DATE",
                    "description": f"Empty stock receipt date in row {row_num}" if t.get("severity_error") == "ERROR" else f"Pusta data przyjęcia w wierszu {row_num}",
                    "severity": t.get("severity_error", "ERROR")
                })
            else:
                try:
                    d = pd.to_datetime(val)
                    if d.date() > aging_date:
                        issues.append({
                            "row": row_num,
                            "type": "FUTURE_DATE",
                            "description": f"Receipt date {d.date()} is after aging date {aging_date}",
                            "severity": t.get("severity_warning", "WARNING")
                        })
                except Exception:
                    issues.append({
                        "row": row_num,
                        "type": "INVALID_DATE",
                        "description": f"Invalid date value in row {row_num}: {val}",
                        "severity": t.get("severity_error", "ERROR")
                    })

        # Check quantity
        if qty_col:
            val = row.get(qty_col)
            if pd.isna(val) or val is None:
                issues.append({
                    "row": row_num,
                    "type": "MISSING_QTY",
                    "description": f"Missing quantity in row {row_num}",
                    "severity": t.get("severity_warning", "WARNING")
                })
            else:
                try:
                    q = float(val)
                    if q < 0:
                        issues.append({
                            "row": row_num,
                            "type": "NEGATIVE_QTY",
                            "description": f"Negative quantity ({q}) in row {row_num}",
                            "severity": t.get("severity_warning", "WARNING")
                        })
                except Exception:
                    issues.append({
                        "row": row_num,
                        "type": "INVALID_QTY",
                        "description": f"Non-numeric quantity in row {row_num}: {val}",
                        "severity": t.get("severity_error", "ERROR")
                    })

        # Check batch if required
        if use_batch and batch_col:
            val = row.get(batch_col)
            if pd.isna(val) or str(val).strip() == "":
                issues.append({
                    "row": row_num,
                    "type": "MISSING_BATCH",
                    "description": f"Missing batch number in row {row_num}",
                    "severity": t.get("severity_warning", "WARNING")
                })

    return issues


def validate_custom_buckets(buckets: list) -> list:
    """
    Validate custom bucket definitions.
    Each bucket: {"name": str, "from_day": int, "to_day": int or None}
    Returns list of error strings.
    """
    errors = []
    if not buckets:
        errors.append("No buckets defined.")
        return errors

    prev_to = -1
    for i, b in enumerate(buckets):
        name = b.get("name", "").strip()
        from_day = b.get("from_day")
        to_day = b.get("to_day")  # None means unlimited

        if not name:
            errors.append(f"Bucket {i+1}: name is empty.")
        if from_day is None or from_day < 0:
            errors.append(f"Bucket {i+1}: invalid 'from' day.")
            continue
        if to_day is not None and to_day <= from_day:
            errors.append(f"Bucket '{name}': 'to' must be greater than 'from'.")
        if from_day <= prev_to:
            errors.append(f"Bucket '{name}': overlaps with previous bucket.")
        prev_to = to_day if to_day is not None else float("inf")

    return errors
