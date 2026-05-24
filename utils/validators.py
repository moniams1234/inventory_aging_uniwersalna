# utils/validators.py
# Validation logic for column mapping, data quality, and aging buckets

import pandas as pd
from datetime import date


def validate_column_mapping(mapping: dict, use_batch: bool) -> list:
    """
    Validate that all mandatory columns are mapped.
    Returns list of missing field names.
    """
    errors = []
    mandatory = ["material_index", "receipt_date", "material_name", "doc_number", "quantity"]
    for col in mandatory:
        if not mapping.get(col):
            errors.append(col)
    if use_batch and not mapping.get("batch"):
        errors.append("batch")
    return errors


def validate_data(df: pd.DataFrame, mapping: dict, aging_date: date,
                  use_batch: bool, t: dict) -> list:
    """
    Validate data quality. Returns list of validation log entries:
    {"row": int, "type": str, "description": str, "severity": str}
    """
    issues = []

    qty_col = mapping.get("quantity")
    date_col = mapping.get("receipt_date")
    batch_col = mapping.get("batch")

    sev_error = t.get("severity_error", "ERROR")
    sev_warn = t.get("severity_warning", "WARNING")

    for i, row in df.iterrows():
        row_num = i + 2  # Excel-style (1-indexed + header row)

        # Check receipt date
        if date_col:
            val = row.get(date_col)
            if pd.isna(val) or val is None:
                issues.append({
                    "row": row_num,
                    "type": "MISSING_DATE",
                    "description": f"Empty receipt date in row {row_num}",
                    "severity": sev_error
                })
            else:
                try:
                    d = pd.to_datetime(val)
                    if d.date() > aging_date:
                        issues.append({
                            "row": row_num,
                            "type": "FUTURE_DATE",
                            "description": f"Receipt date {d.date()} is after aging date {aging_date}",
                            "severity": sev_warn
                        })
                except Exception:
                    issues.append({
                        "row": row_num,
                        "type": "INVALID_DATE",
                        "description": f"Invalid date in row {row_num}: {val}",
                        "severity": sev_error
                    })

        # Check quantity
        if qty_col:
            val = row.get(qty_col)
            if pd.isna(val) or val is None:
                issues.append({
                    "row": row_num,
                    "type": "MISSING_QTY",
                    "description": f"Missing quantity in row {row_num}",
                    "severity": sev_warn
                })
            else:
                try:
                    q = float(val)
                    if q < 0:
                        issues.append({
                            "row": row_num,
                            "type": "NEGATIVE_QTY",
                            "description": f"Negative quantity ({q}) in row {row_num}",
                            "severity": sev_warn
                        })
                except Exception:
                    issues.append({
                        "row": row_num,
                        "type": "INVALID_QTY",
                        "description": f"Non-numeric quantity in row {row_num}: {val}",
                        "severity": sev_error
                    })

        # Check batch if required
        if use_batch and batch_col:
            val = row.get(batch_col)
            if pd.isna(val) or str(val).strip() == "":
                issues.append({
                    "row": row_num,
                    "type": "MISSING_BATCH",
                    "description": f"Missing batch number in row {row_num}",
                    "severity": sev_warn
                })

    return issues


def validate_custom_buckets(buckets: list, t: dict | None = None) -> tuple[list, list]:
    """
    Validate custom bucket definitions.
    Each bucket: {"name": str, "from_day": int, "to_day": int | None}

    Returns:
        errors  - list of hard error strings (block calculation)
        warnings - list of warning strings (show but allow)
    """
    errors = []
    warnings = []

    if not buckets:
        msg = (t or {}).get("bucket_error_none", "No buckets defined.")
        errors.append(msg)
        return errors, warnings

    # Check that at most one bucket has to_day = None, and it must be the last one
    open_indices = [i for i, b in enumerate(buckets) if b.get("to_day") is None]
    if len(open_indices) > 1:
        msg = (t or {}).get("bucket_error_only_one_open",
                             "Only one bucket can be open-ended (no 'Day to').")
        errors.append(msg)

    if len(open_indices) == 1 and open_indices[0] != len(buckets) - 1:
        msg = (t or {}).get("bucket_error_multi_open",
                             "Only the last bucket can have an empty 'Day to'.")
        errors.append(msg)

    prev_to = -1
    for i, b in enumerate(buckets):
        name = str(b.get("name", "")).strip()
        from_day = b.get("from_day")
        to_day = b.get("to_day")  # None means open-ended

        if not name:
            tmpl = (t or {}).get("bucket_error_empty_name", "Bucket {n}: name is empty.")
            errors.append(tmpl.format(n=i + 1))

        if from_day is None or (isinstance(from_day, (int, float)) and from_day < 0):
            tmpl = (t or {}).get("bucket_error_invalid_from", "Bucket {n}: invalid 'Day from'.")
            errors.append(tmpl.format(n=i + 1))
            continue  # skip further checks for this bucket

        if to_day is not None and to_day <= from_day:
            tmpl = (t or {}).get("bucket_error_to_lte_from",
                                  "Bucket '{name}': 'Day to' must be greater than 'Day from'.")
            errors.append(tmpl.format(name=name or f"#{i+1}"))

        if from_day <= prev_to:
            tmpl = (t or {}).get("bucket_error_overlaps",
                                  "Bucket '{name}': overlaps with previous bucket.")
            errors.append(tmpl.format(name=name or f"#{i+1}"))

        # Gap detection (warning only)
        if prev_to >= 0 and from_day > prev_to + 1:
            tmpl = (t or {}).get("bucket_warn_gap",
                                  "Warning: gap detected between buckets")
            warnings.append(f"{tmpl}: {prev_to}–{from_day - 1}")

        prev_to = to_day if to_day is not None else float("inf")

    return errors, warnings
