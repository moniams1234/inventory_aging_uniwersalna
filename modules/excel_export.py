# modules/excel_export.py
# Excel report generation with corporate formatting

import pandas as pd
import io
from datetime import date


def generate_excel(
    df_detail: pd.DataFrame,
    df_qty: pd.DataFrame,
    df_val: pd.DataFrame | None,
    df_wh: pd.DataFrame | None,
    df_batch: pd.DataFrame | None,
    validation_log: list,
    mapping: dict,
    aging_date: date,
    buckets: list,
    stats: dict,
    t: dict
) -> bytes:
    """
    Generate Excel report with multiple sheets, formatting, and conditional formatting.
    Returns bytes of the Excel file.
    """
    output = io.BytesIO()

    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        wb = writer.book

        # ── Formats ──────────────────────────────────────────────────────────
        header_fmt = wb.add_format({
            "bold": True, "bg_color": "#1E3A5F", "font_color": "#FFFFFF",
            "border": 1, "border_color": "#CCCCCC", "text_wrap": True,
            "valign": "vcenter", "align": "center"
        })
        date_fmt = wb.add_format({"num_format": "yyyy-mm-dd", "border": 1, "border_color": "#E0E0E0"})
        num2_fmt = wb.add_format({"num_format": "#,##0.00", "border": 1, "border_color": "#E0E0E0"})
        text_fmt = wb.add_format({"border": 1, "border_color": "#E0E0E0"})
        int_fmt = wb.add_format({"num_format": "#,##0", "border": 1, "border_color": "#E0E0E0"})

        warn_fmt = wb.add_format({"bg_color": "#FFF3CD", "border": 1, "border_color": "#E0E0E0"})
        error_fmt = wb.add_format({"bg_color": "#F8D7DA", "border": 1, "border_color": "#E0E0E0"})
        ok_fmt = wb.add_format({"bg_color": "#D4EDDA", "border": 1, "border_color": "#E0E0E0"})
        orange_fmt = wb.add_format({"bg_color": "#FFD580", "border": 1, "border_color": "#E0E0E0", "num_format": "#,##0.00"})
        red_fmt = wb.add_format({"bg_color": "#FF9999", "border": 1, "border_color": "#E0E0E0", "num_format": "#,##0.00"})

        subheader_fmt = wb.add_format({
            "bold": True, "bg_color": "#2E6DA4", "font_color": "#FFFFFF",
            "border": 1, "border_color": "#CCCCCC", "align": "center"
        })
        total_fmt = wb.add_format({
            "bold": True, "bg_color": "#F0F4F8", "num_format": "#,##0.00",
            "border": 1, "border_color": "#CCCCCC"
        })

        # ── Helper: write DataFrame to sheet ─────────────────────────────────
        def write_sheet(df: pd.DataFrame, sheet_name: str, date_cols: list = None,
                        num_cols: list = None, freeze_rows: int = 1):
            if df is None or df.empty:
                ws = wb.add_worksheet(sheet_name)
                ws.write(0, 0, "No data", text_fmt)
                return

            df.to_excel(writer, sheet_name=sheet_name, index=False, startrow=0)
            ws = writer.sheets[sheet_name]

            # Header format
            for col_idx, col_name in enumerate(df.columns):
                ws.write(0, col_idx, col_name, header_fmt)

            # Data formatting
            for row_idx in range(len(df)):
                for col_idx, col_name in enumerate(df.columns):
                    val = df.iloc[row_idx, col_idx]
                    if date_cols and col_name in date_cols:
                        ws.write(row_idx + 1, col_idx, str(val)[:10] if pd.notna(val) else "", date_fmt)
                    elif num_cols and col_name in num_cols:
                        try:
                            ws.write_number(row_idx + 1, col_idx, float(val) if pd.notna(val) else 0, num2_fmt)
                        except Exception:
                            ws.write(row_idx + 1, col_idx, val if pd.notna(val) else "", text_fmt)
                    else:
                        if pd.isna(val):
                            ws.write(row_idx + 1, col_idx, "", text_fmt)
                        elif isinstance(val, (int, float)):
                            ws.write_number(row_idx + 1, col_idx, val, num2_fmt)
                        else:
                            ws.write(row_idx + 1, col_idx, str(val), text_fmt)

            # Auto column widths
            for col_idx, col_name in enumerate(df.columns):
                max_len = max(len(str(col_name)), 10)
                for row_idx in range(min(len(df), 200)):
                    v = df.iloc[row_idx, col_idx]
                    max_len = max(max_len, len(str(v)) if pd.notna(v) else 0)
                ws.set_column(col_idx, col_idx, min(max_len + 2, 40))

            ws.freeze_panes(freeze_rows, 0)
            ws.autofilter(0, 0, len(df), len(df.columns) - 1)

        # ── Identify numeric/date columns ─────────────────────────────────
        qty_col = mapping.get("quantity")
        val_col = mapping.get("value")
        date_col = mapping.get("receipt_date")
        age_days_col = t["out_age_days"]
        age_months_col = t["out_age_months"]
        bucket_col = t["out_bucket"]
        aging_date_col = t["out_aging_date"]

        num_cols_detail = [c for c in [qty_col, val_col, age_days_col, age_months_col] if c]
        date_cols_detail = [c for c in [date_col, aging_date_col] if c]

        # ── Sheet: Detailed Data ──────────────────────────────────────────
        write_sheet(df_detail, t["sheet_detail"], date_cols=date_cols_detail, num_cols=num_cols_detail)

        # Conditional formatting on bucket column in detail sheet
        if not df_detail.empty and bucket_col in df_detail.columns:
            ws_d = writer.sheets[t["sheet_detail"]]
            bucket_idx = list(df_detail.columns).index(bucket_col)
            bucket_names_old = [b["name"] for b in buckets if b.get("from_day", 0) >= 366]
            bucket_names_very_old = [b["name"] for b in buckets if b.get("from_day", 0) >= 731]

            for row_idx in range(len(df_detail)):
                bval = df_detail.iloc[row_idx].get(bucket_col, "")
                if bval in bucket_names_very_old:
                    ws_d.write(row_idx + 1, bucket_idx, bval, error_fmt)
                elif bval in bucket_names_old:
                    ws_d.write(row_idx + 1, bucket_idx, bval, warn_fmt)

        # ── Sheet: Quantity Summary ──────────────────────────────────────
        num_cols_qty = [c for c in df_qty.columns if c not in [
            mapping.get("material_index"), mapping.get("material_name"),
            mapping.get("warehouse"), mapping.get("batch"), t["out_bucket"]
        ]]
        write_sheet(df_qty, t["sheet_qty"], num_cols=num_cols_qty)

        # ── Sheet: Value Summary ─────────────────────────────────────────
        if df_val is not None:
            num_cols_val = [c for c in df_val.columns if c not in [
                mapping.get("material_index"), mapping.get("material_name"),
                mapping.get("warehouse"), mapping.get("batch"), t["out_bucket"]
            ]]
            write_sheet(df_val, t["sheet_val"], num_cols=num_cols_val)

        # ── Sheet: Warehouse Summary ─────────────────────────────────────
        if df_wh is not None:
            write_sheet(df_wh, t["sheet_wh"], num_cols=[qty_col, val_col] if val_col else [qty_col])

        # ── Sheet: Batch Summary ─────────────────────────────────────────
        if df_batch is not None:
            write_sheet(df_batch, t["sheet_batch"], num_cols=[qty_col, val_col] if val_col else [qty_col])

        # ── Sheet: Summary ───────────────────────────────────────────────
        ws_sum = wb.add_worksheet(t["sheet_summary"])
        ws_sum.set_column(0, 0, 35)
        ws_sum.set_column(1, 1, 20)

        title_fmt = wb.add_format({"bold": True, "font_size": 14, "font_color": "#1E3A5F"})
        label_fmt = wb.add_format({"bold": True, "bg_color": "#EBF2FF", "border": 1, "border_color": "#CCCCCC"})
        value_fmt_s = wb.add_format({"num_format": "#,##0.00", "border": 1, "border_color": "#CCCCCC"})
        pct_fmt = wb.add_format({"num_format": "0.00%", "border": 1, "border_color": "#CCCCCC"})

        ws_sum.write(0, 0, t["app_title"] if "app_title" in t else "Inventory Aging Analyzer", title_fmt)
        ws_sum.write(1, 0, f"{t.get('out_aging_date','Aging Date')}: {aging_date}", text_fmt)

        row = 3
        kpis = [
            (t.get("kpi_total_qty", "Total Quantity"), stats.get("total_qty", 0), value_fmt_s),
            (t.get("kpi_total_value", "Total Value"), stats.get("total_value"), value_fmt_s),
            (t.get("kpi_materials", "Material Indexes"), stats.get("n_materials", 0), int_fmt),
            (t.get("kpi_warehouses", "Warehouses"), stats.get("n_warehouses"), int_fmt),
            (t.get("kpi_above_1y", "Share above 1 year"), stats.get("above_1y_pct", 0) / 100 if stats.get("above_1y_pct") else None, pct_fmt),
            (t.get("kpi_above_2y", "Share above 2 years"), stats.get("above_2y_pct", 0) / 100 if stats.get("above_2y_pct") else None, pct_fmt),
        ]
        for label, value, fmt in kpis:
            ws_sum.write(row, 0, label, label_fmt)
            if value is not None:
                ws_sum.write_number(row, 1, float(value), fmt)
            else:
                ws_sum.write(row, 1, "N/A", text_fmt)
            row += 1

        # Bucket breakdown
        row += 1
        ws_sum.write(row, 0, t.get("buckets_header", "Aging Buckets"), subheader_fmt)
        ws_sum.write(row, 1, t.get("kpi_total_qty", "Total Quantity"), subheader_fmt)
        row += 1
        bucket_col_name = t["out_bucket"]
        qty_col_name = mapping["quantity"]
        if bucket_col_name in df_detail.columns:
            bucket_summary = df_detail.groupby(bucket_col_name)[qty_col_name].sum()
            for bname, bqty in bucket_summary.items():
                ws_sum.write(row, 0, bname, label_fmt)
                ws_sum.write_number(row, 1, float(bqty) if pd.notna(bqty) else 0, value_fmt_s)
                row += 1

        ws_sum.freeze_panes(2, 0)

        # ── Sheet: Validation Log ────────────────────────────────────────
        if validation_log:
            df_val_log = pd.DataFrame(validation_log)
            df_val_log.columns = [
                t.get("val_row", "Row"),
                t.get("val_type", "Type"),
                t.get("val_desc", "Description"),
                t.get("val_severity", "Severity")
            ]
        else:
            df_val_log = pd.DataFrame(columns=[
                t.get("val_row", "Row"),
                t.get("val_type", "Type"),
                t.get("val_desc", "Description"),
                t.get("val_severity", "Severity")
            ])

        df_val_log.to_excel(writer, sheet_name=t["sheet_validation"], index=False, startrow=0)
        ws_vl = writer.sheets[t["sheet_validation"]]
        for col_idx, col_name in enumerate(df_val_log.columns):
            ws_vl.write(0, col_idx, col_name, header_fmt)
        ws_vl.set_column(0, 0, 10)
        ws_vl.set_column(1, 1, 20)
        ws_vl.set_column(2, 2, 60)
        ws_vl.set_column(3, 3, 15)

        severity_col_idx = 3
        sev_error = t.get("severity_error", "ERROR")
        sev_warn = t.get("severity_warning", "WARNING")
        for row_idx, row_data in df_val_log.iterrows():
            sev = row_data.iloc[3]
            for col_idx in range(len(df_val_log.columns)):
                val = row_data.iloc[col_idx]
                if sev == sev_error:
                    fmt = error_fmt
                elif sev == sev_warn:
                    fmt = warn_fmt
                else:
                    fmt = ok_fmt
                ws_vl.write(row_idx + 1, col_idx, str(val) if pd.notna(val) else "", fmt)

        ws_vl.freeze_panes(1, 0)
        ws_vl.autofilter(0, 0, len(df_val_log), len(df_val_log.columns) - 1)

    output.seek(0)
    return output.read()
