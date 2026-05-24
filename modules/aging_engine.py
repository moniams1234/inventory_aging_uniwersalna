# modules/aging_engine.py
# Core aging calculation logic

import pandas as pd
from datetime import date


DEFAULT_BUCKETS_EN = [
    {"name": "0–3 months",    "from_day": 0,   "to_day": 90},
    {"name": "3–6 months",    "from_day": 91,  "to_day": 180},
    {"name": "6–9 months",    "from_day": 181, "to_day": 270},
    {"name": "9–12 months",   "from_day": 271, "to_day": 365},
    {"name": "1–2 years",     "from_day": 366, "to_day": 730},
    {"name": "Above 2 years", "from_day": 731, "to_day": None},
]

DEFAULT_BUCKETS_PL = [
    {"name": "0–3 miesiące",  "from_day": 0,   "to_day": 90},
    {"name": "3–6 miesięcy",  "from_day": 91,  "to_day": 180},
    {"name": "6–9 miesięcy",  "from_day": 181, "to_day": 270},
    {"name": "9–12 miesięcy", "from_day": 271, "to_day": 365},
    {"name": "1–2 lata",      "from_day": 366, "to_day": 730},
    {"name": "Powyżej 2 lat", "from_day": 731, "to_day": None},
]


def get_default_buckets(lang: str) -> list:
    return DEFAULT_BUCKETS_PL if lang == "pl" else DEFAULT_BUCKETS_EN


# ── Helper ────────────────────────────────────────────────────────────────────
def _unique_keep_order(cols: list) -> list:
    """Return list with duplicates removed, preserving first occurrence order.
    Also filters out None/empty values."""
    seen = set()
    result = []
    for c in cols:
        if c and c not in seen:
            seen.add(c)
            result.append(c)
    return result


def assign_bucket(age_days: float, buckets: list) -> str:
    """Assign an aging bucket label based on age in days."""
    if pd.isna(age_days) or age_days < 0:
        return "N/A"
    for b in buckets:
        from_d = b["from_day"]
        to_d = b["to_day"]
        if to_d is None:
            if age_days >= from_d:
                return b["name"]
        else:
            if from_d <= age_days <= to_d:
                return b["name"]
    return "N/A"


def calculate_aging(
    df: pd.DataFrame,
    mapping: dict,
    aging_date: date,
    buckets: list,
    use_batch: bool,
    method_label: str,
    t: dict,
) -> pd.DataFrame:
    """Main aging calculation — returns enriched DataFrame."""
    result = df.copy()

    date_col = mapping["receipt_date"]

    # Parse receipt dates into a temp column
    result["_receipt_date_parsed"] = pd.to_datetime(result[date_col], errors="coerce")

    aging_date_ts = pd.Timestamp(aging_date)
    result[t["out_aging_date"]] = aging_date
    result[t["out_age_days"]]   = (aging_date_ts - result["_receipt_date_parsed"]).dt.days
    result[t["out_age_months"]] = (result[t["out_age_days"]] / 30.44).round(1)

    result[t["out_bucket"]] = result[t["out_age_days"]].apply(
        lambda x: assign_bucket(x, buckets)
    )

    bucket_order = {b["name"]: i for i, b in enumerate(buckets)}
    result["_bucket_order"] = result[t["out_bucket"]].map(bucket_order).fillna(999)

    result[t["out_method"]] = method_label

    def _val_status(row):
        if pd.isna(row.get("_receipt_date_parsed")):
            return t.get("severity_error", "ERROR")
        if (row.get(t["out_age_days"]) or 0) < 0:
            return t.get("severity_warning", "WARNING")
        if row.get(t["out_bucket"]) == "N/A":
            return t.get("severity_warning", "WARNING")
        return t.get("ok", "OK")

    result[t["out_validation"]] = result.apply(_val_status, axis=1)
    result = result.drop(columns=["_receipt_date_parsed"])
    return result


def _make_pivot(df: pd.DataFrame, group_cols: list, value_col: str,
                bucket_col: str, buckets: list, t: dict) -> pd.DataFrame:
    """
    Generic helper: groupby → pivot buckets as columns → add Total.
    group_cols must already be deduplicated and NOT contain bucket_col.
    """
    all_cols = _unique_keep_order(group_cols + [bucket_col])
    pivot_cols = _unique_keep_order(group_cols)   # without bucket

    # groupby on deduplicated cols
    try:
        summary = (
            df.groupby(all_cols, dropna=False)[value_col]
            .sum()
            .reset_index()
        )
    except Exception:
        # fallback: plain groupby without pivot
        return df.groupby(all_cols, dropna=False)[value_col].sum().reset_index()

    try:
        pivot = summary.pivot_table(
            index=pivot_cols,
            columns=bucket_col,
            values=value_col,
            aggfunc="sum",
            fill_value=0,
        )
        # reset_index safely — avoid "already exists" by dropping the column
        # name from the index before calling reset_index when it clashes
        pivot.columns.name = None
        pivot = pivot.reset_index()

        bucket_names = [b["name"] for b in buckets]
        ordered_cols = pivot_cols + [c for c in bucket_names if c in pivot.columns]
        remaining    = [c for c in pivot.columns if c not in ordered_cols]
        pivot = pivot[ordered_cols + remaining]

        num_cols = [c for c in bucket_names if c in pivot.columns]
        pivot[t.get("total", "Total")] = pivot[num_cols].sum(axis=1)
        return pivot

    except Exception:
        return summary


def build_qty_summary(df: pd.DataFrame, mapping: dict, buckets: list,
                      use_batch: bool, t: dict) -> pd.DataFrame:
    """Quantity pivot table by material (+ optional warehouse / batch)."""
    idx_col    = mapping["material_index"]
    name_col   = mapping["material_name"]
    qty_col    = mapping["quantity"]
    wh_col     = mapping.get("warehouse")
    batch_col  = mapping.get("batch")
    bucket_col = t["out_bucket"]

    base = [idx_col, name_col]
    if wh_col:    base.append(wh_col)
    if use_batch and batch_col: base.append(batch_col)

    group_cols = _unique_keep_order(base)
    return _make_pivot(df, group_cols, qty_col, bucket_col, buckets, t)


def build_val_summary(df: pd.DataFrame, mapping: dict, buckets: list,
                      use_batch: bool, t: dict) -> pd.DataFrame | None:
    """Value pivot table. Returns None when no value column is mapped."""
    val_col = mapping.get("value")
    if not val_col:
        return None

    idx_col    = mapping["material_index"]
    name_col   = mapping["material_name"]
    wh_col     = mapping.get("warehouse")
    batch_col  = mapping.get("batch")
    bucket_col = t["out_bucket"]

    base = [idx_col, name_col]
    if wh_col:    base.append(wh_col)
    if use_batch and batch_col: base.append(batch_col)

    group_cols = _unique_keep_order(base)
    return _make_pivot(df, group_cols, val_col, bucket_col, buckets, t)


def build_warehouse_summary(df: pd.DataFrame, mapping: dict, buckets: list,
                             t: dict) -> pd.DataFrame | None:
    """Warehouse-level aging summary. Returns None when no warehouse column."""
    wh_col = mapping.get("warehouse")
    if not wh_col:
        return None

    qty_col    = mapping["quantity"]
    val_col    = mapping.get("value")
    bucket_col = t["out_bucket"]

    group_cols = _unique_keep_order([wh_col, bucket_col])

    agg_dict = {qty_col: "sum"}
    if val_col:
        agg_dict[val_col] = "sum"

    try:
        summary = (
            df.groupby(group_cols, dropna=False)
            .agg(agg_dict)
            .reset_index()
        )
    except Exception:
        summary = df[group_cols + list(agg_dict.keys())].copy()
    return summary


def build_batch_summary(df: pd.DataFrame, mapping: dict, buckets: list,
                        use_batch: bool, t: dict) -> pd.DataFrame | None:
    """Batch-level aging summary. Returns None when not applicable."""
    if not use_batch:
        return None
    batch_col = mapping.get("batch")
    if not batch_col:
        return None

    idx_col    = mapping["material_index"]
    name_col   = mapping["material_name"]
    qty_col    = mapping["quantity"]
    val_col    = mapping.get("value")
    bucket_col = t["out_bucket"]

    group_cols = _unique_keep_order([idx_col, name_col, batch_col, bucket_col])

    agg_dict = {qty_col: "sum"}
    if val_col:
        agg_dict[val_col] = "sum"

    try:
        summary = (
            df.groupby(group_cols, dropna=False)
            .agg(agg_dict)
            .reset_index()
        )
    except Exception:
        summary = df[group_cols + list(agg_dict.keys())].copy()
    return summary


def build_summary_stats(df: pd.DataFrame, mapping: dict, buckets: list,
                        t: dict) -> dict:
    """KPI statistics dictionary."""
    qty_col      = mapping["quantity"]
    val_col      = mapping.get("value")
    wh_col       = mapping.get("warehouse")
    idx_col      = mapping["material_index"]
    age_days_col = t["out_age_days"]

    stats = {
        "total_qty":    df[qty_col].sum(),
        "total_value":  df[val_col].sum() if val_col else None,
        "n_materials":  df[idx_col].nunique(),
        "n_warehouses": df[wh_col].nunique() if wh_col else None,
    }

    total = stats["total_qty"]
    above_1y = df[df[age_days_col] > 365][qty_col].sum()
    above_2y = df[df[age_days_col] > 730][qty_col].sum()
    stats["above_1y_pct"] = (above_1y / total * 100) if total > 0 else 0
    stats["above_2y_pct"] = (above_2y / total * 100) if total > 0 else 0

    return stats
