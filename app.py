# app.py
# Inventory Aging Analyzer / Wiekowanie Zapasów
# Main Streamlit application entry point

import streamlit as st
import pandas as pd
from datetime import date
import traceback

# ── Module imports ─────────────────────────────────────────────────────────────
from modules.translations import get_t
from modules.data_loader import load_file, load_file_raw, get_column_options
from modules.aging_engine import (
    get_default_buckets, calculate_aging,
    build_qty_summary, build_val_summary,
    build_warehouse_summary, build_batch_summary,
    build_summary_stats
)
from modules.excel_export import generate_excel
from modules.styling import inject_css, app_header, section_header, default_buckets_html
from modules.ui_components import (
    render_kpis, chart_aging_qty, chart_aging_val,
    chart_aging_warehouse, chart_top10_oldest, chart_top10_value,
    render_validation_table
)
from utils.validators import validate_column_mapping, validate_data, validate_custom_buckets

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Inventory Aging Analyzer",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_css()

# ══════════════════════════════════════════════════════════════════════════════
# Helper: initialise custom buckets session state if needed
# ══════════════════════════════════════════════════════════════════════════════
def _init_custom_buckets(lang: str):
    """Set default custom buckets the first time (or after lang change resets)."""
    t_init = get_t(lang)
    st.session_state["custom_buckets"] = [
        {"name": t_init["bucket_0_3"],   "from_day": 0,   "to_day": 90},
        {"name": t_init["bucket_3_6"],   "from_day": 91,  "to_day": 180},
        {"name": t_init["bucket_6_9"],   "from_day": 181, "to_day": 270},
        {"name": t_init["bucket_9_12"],  "from_day": 271, "to_day": 365},
        {"name": t_init["bucket_1_2"],   "from_day": 366, "to_day": 730},
        {"name": t_init["bucket_2plus"], "from_day": 731, "to_day": None},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Language & Configuration
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📦 Inventory Aging")
    st.markdown("---")

    # ── Language ──────────────────────────────────────────────────────────────
    lang = st.selectbox(
        "🌐 Język / Language",
        options=["pl", "en"],
        format_func=lambda x: "🇵🇱 Polski" if x == "pl" else "🇬🇧 English",
        key="lang_select"
    )
    t = get_t(lang)

    st.markdown("---")
    st.markdown(f"### {t['sidebar_title']}")

    # ── Aging method ──────────────────────────────────────────────────────────
    st.markdown(f"**{t['method_label']}**")
    method_options = [t["method_index"], t["method_batch"]]
    aging_method = st.radio(
        t["method_label"],
        options=method_options,
        label_visibility="collapsed",
        key="aging_method_radio"
    )
    use_batch = (aging_method == t["method_batch"])

    st.markdown("---")

    # ── Aging date ────────────────────────────────────────────────────────────
    st.markdown(f"**{t['date_label']}**")
    aging_date = st.date_input(
        t["date_label"],
        value=date.today(),
        label_visibility="collapsed",
        key="aging_date_input"
    )

    st.markdown("---")

    # ── Aging buckets ─────────────────────────────────────────────────────────
    st.markdown(f"**{t['buckets_type_label']}**")
    bucket_type = st.radio(
        t["buckets_type_label"],
        options=[t["buckets_default"], t["buckets_custom"]],
        label_visibility="collapsed",
        key="bucket_type_radio"
    )

    default_buckets_list = get_default_buckets(lang)

    if bucket_type == t["buckets_default"]:
        # ── Show default bucket badges ────────────────────────────────────────
        st.markdown(
            f'<div style="color:#C8DCF0;font-size:0.78rem;font-weight:600;'
            f'text-transform:uppercase;letter-spacing:0.04em;margin-bottom:4px;">'
            f'{t["buckets_default_title"]}</div>',
            unsafe_allow_html=True
        )
        st.markdown(default_buckets_html(default_buckets_list), unsafe_allow_html=True)
        buckets = default_buckets_list

    else:
        # ── Custom bucket editor in sidebar ───────────────────────────────────
        st.markdown(
            f'<div style="color:#C8DCF0;font-size:0.78rem;font-weight:600;'
            f'text-transform:uppercase;letter-spacing:0.04em;margin-bottom:6px;">'
            f'{t["buckets_custom_title"]}</div>',
            unsafe_allow_html=True
        )

        # Initialise session state on first load
        if "custom_buckets" not in st.session_state:
            _init_custom_buckets(lang)

        # ── Handle remove-bucket actions (flagged in previous run) ────────────
        if st.session_state.get("_remove_bucket_idx") is not None:
            idx_to_remove = st.session_state.pop("_remove_bucket_idx")
            cb = st.session_state.get("custom_buckets", [])
            if len(cb) > 1 and 0 <= idx_to_remove < len(cb):
                cb.pop(idx_to_remove)
                st.session_state["custom_buckets"] = cb

        # ── Handle add-bucket action ──────────────────────────────────────────
        if st.session_state.get("_add_bucket"):
            st.session_state.pop("_add_bucket")
            cb = st.session_state.get("custom_buckets", [])
            if cb:
                last_to = cb[-1].get("to_day")
                new_from = (last_to + 1) if last_to is not None else 731
            else:
                new_from = 0
            cb.append({"name": "", "from_day": new_from, "to_day": new_from + 89})
            st.session_state["custom_buckets"] = cb

        cb_list = st.session_state.get("custom_buckets", [])

        for i, b in enumerate(cb_list):
            st.markdown(
                f'<div style="color:rgba(255,255,255,0.6);font-size:0.72rem;'
                f'margin-top:6px;margin-bottom:1px;">— {t["bucket_name"]} {i+1}</div>',
                unsafe_allow_html=True
            )
            new_name = st.text_input(
                f"{t['bucket_name']} {i+1}",
                value=b.get("name", ""),
                key=f"cb_name_{i}",
                label_visibility="collapsed"
            )
            col_f, col_t = st.columns(2)
            with col_f:
                new_from = st.number_input(
                    t["bucket_from"], value=int(b.get("from_day") or 0),
                    min_value=0, step=1, key=f"cb_from_{i}",
                    label_visibility="collapsed"
                )
            with col_t:
                # Allow empty (open-ended) only for last bucket
                is_last = (i == len(cb_list) - 1)
                current_to = b.get("to_day")
                if is_last:
                    # Show number input; 0 treated as "open / None"
                    to_val = st.number_input(
                        t["bucket_to"],
                        value=int(current_to) if current_to is not None else 0,
                        min_value=0, step=1, key=f"cb_to_{i}",
                        help=t.get("bucket_to_help", ""),
                        label_visibility="collapsed"
                    )
                    new_to = int(to_val) if to_val > 0 else None
                else:
                    to_val = st.number_input(
                        t["bucket_to"],
                        value=int(current_to) if current_to is not None else int(new_from) + 89,
                        min_value=1, step=1, key=f"cb_to_{i}",
                        label_visibility="collapsed"
                    )
                    new_to = int(to_val)

            # Update bucket in session state immediately
            cb_list[i] = {"name": new_name, "from_day": int(new_from), "to_day": new_to}

            if st.button(t["bucket_remove"], key=f"cb_rem_{i}"):
                st.session_state["_remove_bucket_idx"] = i
                st.rerun()

        st.session_state["custom_buckets"] = cb_list

        # Add bucket button
        if st.button(t["bucket_add"], key="cb_add_btn"):
            st.session_state["_add_bucket"] = True
            st.rerun()

        # Validate
        bucket_errors, bucket_warnings = validate_custom_buckets(cb_list, t)

        if bucket_warnings:
            for w in bucket_warnings:
                st.markdown(
                    f'<div style="background:rgba(243,156,18,0.2);border-radius:6px;'
                    f'padding:6px 10px;font-size:0.78rem;color:#FFF3CD;margin-top:4px;">⚠️ {w}</div>',
                    unsafe_allow_html=True
                )
        if bucket_errors:
            for e in bucket_errors:
                st.markdown(
                    f'<div style="background:rgba(231,76,60,0.25);border-radius:6px;'
                    f'padding:6px 10px;font-size:0.78rem;color:#FADADD;margin-top:4px;">❌ {e}</div>',
                    unsafe_allow_html=True
                )
            buckets = default_buckets_list   # fallback to defaults if errors
        else:
            buckets = cb_list

    st.markdown("---")
    st.markdown(
        '<div style="color:rgba(255,255,255,0.45);font-size:0.73rem;text-align:center;">'
        'Inventory Aging Analyzer v1.1<br>© 2025</div>',
        unsafe_allow_html=True
    )

# ── Refresh translation after sidebar (lang may have changed) ─────────────────
t = get_t(lang)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(app_header(t["app_title"], t["app_subtitle"]), unsafe_allow_html=True)

# ── STEP 1: File Upload ────────────────────────────────────────────────────────
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown(section_header(t["upload_header"]), unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    t["upload_label"],
    type=["xlsx", "xls", "csv"],
    help=t["upload_help"],
    label_visibility="collapsed",
    key="file_uploader"
)

df_raw = None

if uploaded_file is not None:
    # ── Raw preview for header row selection ──────────────────────────────────
    with st.expander(t["header_row_preview"], expanded=False):
        df_peek = load_file_raw(uploaded_file)
        if df_peek is not None:
            st.dataframe(df_peek.head(6), use_container_width=True)
        else:
            st.warning(t["error_file_read"])

    col_hr1, col_hr2 = st.columns([1, 3])
    with col_hr1:
        header_row = st.number_input(
            t["header_row_label"],
            min_value=1,
            max_value=50,
            value=st.session_state.get("header_row_val", 1),
            step=1,
            help=t["header_row_help"],
            key="header_row_input"
        )
        st.session_state["header_row_val"] = int(header_row)

    # Load with chosen header row
    with st.spinner("Loading..."):
        df_raw = load_file(uploaded_file, header_row=int(header_row))

    if df_raw is not None:
        st.success(
            f"{t['upload_success']} — {t['rows_loaded']}: **{len(df_raw):,}** "
            f"| {t['cols_loaded']}: **{len(df_raw.columns)}**"
        )
        with st.expander(t["preview_header"], expanded=False):
            st.dataframe(df_raw.head(20), use_container_width=True, hide_index=True)
    else:
        st.error(t["error_file_read"])

st.markdown("</div>", unsafe_allow_html=True)

# ── STEP 2: Column Mapping ─────────────────────────────────────────────────────
mapping = {}

if df_raw is not None:
    col_options = [""] + get_column_options(df_raw)
    skip_label = t["col_skip"]

    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(section_header(t["mapping_header"]), unsafe_allow_html=True)
    st.caption(t["mapping_desc"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"**📌 {t['mandatory_cols']}**")
        mat_idx      = st.selectbox(t["col_material_index"], col_options, key="map_idx")
        receipt_date = st.selectbox(t["col_receipt_date"],   col_options, key="map_date")
        mat_name     = st.selectbox(t["col_material_name"],  col_options, key="map_name")
        doc_number   = st.selectbox(t["col_doc_number"],     col_options, key="map_doc")
        quantity     = st.selectbox(t["col_quantity"],       col_options, key="map_qty")

    with col2:
        st.markdown(f"**🔧 {t['optional_cols']}**")
        col_opts_skip = [skip_label] + get_column_options(df_raw)
        value_col     = st.selectbox(t["col_value"],     col_opts_skip, key="map_val")
        warehouse_col = st.selectbox(t["col_warehouse"], col_opts_skip, key="map_wh")

        if use_batch:
            st.markdown(f"**🏷️ {t['batch_col_required']}**")
            batch_col = st.selectbox(t["col_batch"], col_options, key="map_batch")
        else:
            batch_col = ""

    mapping = {
        "material_index": mat_idx      if mat_idx else None,
        "receipt_date":   receipt_date if receipt_date else None,
        "material_name":  mat_name     if mat_name else None,
        "doc_number":     doc_number   if doc_number else None,
        "quantity":       quantity     if quantity else None,
        "value":          value_col    if value_col and value_col != skip_label else None,
        "warehouse":      warehouse_col if warehouse_col and warehouse_col != skip_label else None,
        "batch":          batch_col    if batch_col else None,
    }

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Info / warnings before calculation ────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    if not mapping.get("value"):
        st.info(t["info_no_value_col"])
    if not mapping.get("warehouse"):
        st.info(t["info_no_wh_col"])
    if use_batch and not mapping.get("batch"):
        st.warning(t["info_batch_required"])

    calc_col1, _ = st.columns([2, 1])
    with calc_col1:
        calc_clicked = st.button(t["calc_button"], type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════════════
    # CALCULATION & RESULTS
    # ══════════════════════════════════════════════════════════════════════════
    if calc_clicked or st.session_state.get("results_ready"):

        # Validate mandatory column mapping
        missing_cols = validate_column_mapping(mapping, use_batch)
        if missing_cols:
            st.error(f"❌ {t['error_missing_cols']}{', '.join(missing_cols)}")
            st.stop()

        if calc_clicked:
            try:
                with st.spinner("Calculating..."):
                    method_label = t["method_batch"] if use_batch else t["method_index"]

                    df_work = df_raw.copy()
                    qty_col_name = mapping["quantity"]
                    df_work[qty_col_name] = pd.to_numeric(
                        df_work[qty_col_name], errors="coerce"
                    ).fillna(0)

                    if mapping.get("value"):
                        val_col_name = mapping["value"]
                        df_work[val_col_name] = pd.to_numeric(
                            df_work[val_col_name], errors="coerce"
                        ).fillna(0)

                    validation_issues = validate_data(df_work, mapping, aging_date, use_batch, t)

                    df_result = calculate_aging(
                        df_work, mapping, aging_date, buckets, use_batch, method_label, t
                    )

                    df_qty   = build_qty_summary(df_result, mapping, buckets, use_batch, t)
                    df_val   = build_val_summary(df_result, mapping, buckets, use_batch, t)
                    df_wh    = build_warehouse_summary(df_result, mapping, buckets, t)
                    df_batch = build_batch_summary(df_result, mapping, buckets, use_batch, t)
                    stats    = build_summary_stats(df_result, mapping, buckets, t)

                    val_log_rows = [
                        [v["row"], v["type"], v["description"], v["severity"]]
                        for v in validation_issues
                    ]

                    st.session_state.update({
                        "results_ready":     True,
                        "df_result":         df_result,
                        "df_qty":            df_qty,
                        "df_val":            df_val,
                        "df_wh":             df_wh,
                        "df_batch":          df_batch,
                        "stats":             stats,
                        "validation_issues": validation_issues,
                        "val_log_rows":      val_log_rows,
                        "buckets_used":      buckets,
                        "mapping_used":      mapping,
                        "aging_date_used":   aging_date,
                        "use_batch_used":    use_batch,
                    })

                    st.success(t["calc_success"])

            except Exception as e:
                st.error(f"{t['calc_error']}: {str(e)}")
                with st.expander("Debug info"):
                    st.code(traceback.format_exc())
                st.stop()

        # ── Read results from session state ────────────────────────────────────
        if st.session_state.get("results_ready"):
            df_result        = st.session_state["df_result"]
            df_qty           = st.session_state["df_qty"]
            df_val           = st.session_state["df_val"]
            df_wh            = st.session_state["df_wh"]
            df_batch         = st.session_state["df_batch"]
            stats            = st.session_state["stats"]
            validation_issues= st.session_state["validation_issues"]
            val_log_rows     = st.session_state["val_log_rows"]
            buckets_used     = st.session_state["buckets_used"]
            mapping_used     = st.session_state["mapping_used"]
            aging_date_used  = st.session_state["aging_date_used"]
            use_batch_used   = st.session_state["use_batch_used"]

            # ── Build tab list ──────────────────────────────────────────────
            tabs_to_show = [t["tab_dashboard"], t["tab_detail"], t["tab_qty_summary"]]
            if df_val is not None:
                tabs_to_show.append(t["tab_val_summary"])
            if df_wh is not None:
                tabs_to_show.append(t["tab_wh_summary"])
            if df_batch is not None:
                tabs_to_show.append(t["tab_batch_summary"])
            tabs_to_show.append(t["tab_validation"])

            tab_objs = st.tabs(tabs_to_show)
            tab_idx = 0

            # ── Dashboard ──────────────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["dashboard_header"]), unsafe_allow_html=True)
                render_kpis(stats, t)
                st.write("")

                cc1, cc2 = st.columns(2)
                with cc1:
                    chart_aging_qty(
                        df_result, t["out_bucket"], mapping_used["quantity"], t, buckets_used
                    )
                with cc2:
                    if mapping_used.get("value"):
                        chart_aging_val(
                            df_result, t["out_bucket"], mapping_used["value"], t, buckets_used
                        )

                if mapping_used.get("warehouse"):
                    chart_aging_warehouse(
                        df_result, mapping_used["warehouse"],
                        t["out_bucket"], mapping_used["quantity"], t, buckets_used
                    )

                cc3, cc4 = st.columns(2)
                with cc3:
                    chart_top10_oldest(
                        df_result, mapping_used["material_index"], mapping_used["material_name"],
                        t["out_age_days"], mapping_used["quantity"], t
                    )
                with cc4:
                    if mapping_used.get("value"):
                        chart_top10_value(
                            df_result, mapping_used["material_index"],
                            mapping_used["material_name"], mapping_used["value"], t
                        )

            # ── Detailed data ───────────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["tab_detail"]), unsafe_allow_html=True)
                st.dataframe(
                    df_result.drop(columns=["_bucket_order"], errors="ignore"),
                    use_container_width=True, hide_index=True
                )

            # ── Quantity summary ────────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["tab_qty_summary"]), unsafe_allow_html=True)
                st.dataframe(df_qty, use_container_width=True, hide_index=True)

            # ── Value summary ───────────────────────────────────────────────
            if df_val is not None:
                with tab_objs[tab_idx]:
                    tab_idx += 1
                    st.markdown(section_header(t["tab_val_summary"]), unsafe_allow_html=True)
                    st.dataframe(df_val, use_container_width=True, hide_index=True)

            # ── Warehouse summary ───────────────────────────────────────────
            if df_wh is not None:
                with tab_objs[tab_idx]:
                    tab_idx += 1
                    st.markdown(section_header(t["tab_wh_summary"]), unsafe_allow_html=True)
                    st.dataframe(df_wh, use_container_width=True, hide_index=True)

            # ── Batch summary ───────────────────────────────────────────────
            if df_batch is not None:
                with tab_objs[tab_idx]:
                    tab_idx += 1
                    st.markdown(section_header(t["tab_batch_summary"]), unsafe_allow_html=True)
                    st.dataframe(df_batch, use_container_width=True, hide_index=True)

            # ── Validation log ──────────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["validation_header"]), unsafe_allow_html=True)
                render_validation_table(validation_issues, t)

            # ── Excel download ──────────────────────────────────────────────
            st.markdown("---")
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(section_header(t["download_button"]), unsafe_allow_html=True)

            excel_bytes = generate_excel(
                df_detail=df_result.drop(columns=["_bucket_order"], errors="ignore"),
                df_qty=df_qty,
                df_val=df_val,
                df_wh=df_wh,
                df_batch=df_batch,
                validation_log=val_log_rows,
                mapping=mapping_used,
                aging_date=aging_date_used,
                buckets=buckets_used,
                stats=stats,
                t=t
            )

            filename = f"inventory_aging_{aging_date_used.strftime('%Y%m%d')}.xlsx"
            st.download_button(
                label=t["download_button"],
                data=excel_bytes,
                file_name=filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
            st.markdown("</div>", unsafe_allow_html=True)

else:
    # No file uploaded yet
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="text-align:center; padding: 48px 24px;">
            <div style="font-size:4rem; margin-bottom:16px;">📦</div>
            <h3 style="color:#1E3A5F; font-family:'DM Serif Display',serif;">{t['step1']}</h3>
            <p style="color:#718096; font-size:1rem; max-width:400px; margin:0 auto;">
                {t['instructions']}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="app-footer">Inventory Aging Analyzer · Built with Streamlit & Python</div>',
    unsafe_allow_html=True
)
