# app.py
# Inventory Aging Analyzer / Wiekowanie Zapasów
# Main Streamlit application entry point

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import traceback

# ── Module imports ─────────────────────────────────────────────────────────────
from modules.translations import get_t
from modules.data_loader import load_file, get_column_options
from modules.aging_engine import (
    get_default_buckets, calculate_aging,
    build_qty_summary, build_val_summary,
    build_warehouse_summary, build_batch_summary,
    build_summary_stats
)
from modules.excel_export import generate_excel
from modules.styling import inject_css, app_header, section_header
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
# SIDEBAR — Language & Configuration
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 📦 Inventory Aging")
    st.markdown("---")

    # Language selector
    lang = st.selectbox(
        "🌐 Język / Language",
        options=["pl", "en"],
        format_func=lambda x: "🇵🇱 Polski" if x == "pl" else "🇬🇧 English",
        key="lang_select"
    )
    t = get_t(lang)

    st.markdown("---")
    st.markdown(f"### {t['sidebar_title']}")

    # Aging method
    st.markdown(f"**{t['method_label']}**")
    method_options = [t["method_index"], t["method_batch"]]
    aging_method = st.radio(
        t["method_label"],
        options=method_options,
        label_visibility="collapsed"
    )
    use_batch = (aging_method == t["method_batch"])

    st.markdown("---")

    # Aging date
    st.markdown(f"**{t['date_label']}**")
    aging_date = st.date_input(
        t["date_label"],
        value=date.today(),
        label_visibility="collapsed"
    )

    st.markdown("---")

    # Bucket type
    st.markdown(f"**{t['buckets_type_label']}**")
    bucket_type = st.radio(
        t["buckets_type_label"],
        options=[t["buckets_default"], t["buckets_custom"]],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown(
        '<div style="color:rgba(255,255,255,0.5);font-size:0.75rem;text-align:center;">'
        'Inventory Aging Analyzer v1.0<br>© 2025</div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════════════════════
# Get fresh translation (in case lang changed)
# ══════════════════════════════════════════════════════════════════════════════
t = get_t(lang)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(
    app_header(t["app_title"], t["app_subtitle"]),
    unsafe_allow_html=True
)

# ── STEP 1: File Upload ────────────────────────────────────────────────────────
st.markdown(f'<div class="section-card">', unsafe_allow_html=True)
st.markdown(section_header(t["upload_header"]), unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    t["upload_label"],
    type=["xlsx", "xls", "csv"],
    help=t["upload_help"],
    label_visibility="collapsed"
)

df_raw = None
if uploaded_file is not None:
    with st.spinner("Loading file..."):
        df_raw = load_file(uploaded_file)

    if df_raw is not None:
        st.success(f"{t['upload_success']} — {t['rows_loaded']}: **{len(df_raw):,}** | {t['cols_loaded']}: **{len(df_raw.columns)}**")
        with st.expander(t["preview_header"], expanded=False):
            st.dataframe(df_raw.head(20), use_container_width=True, hide_index=True)
    else:
        st.error(t["error_file_read"])

st.markdown("</div>", unsafe_allow_html=True)

# ── STEP 2: Column Mapping ─────────────────────────────────────────────────────
mapping = {}
buckets = get_default_buckets(lang)

if df_raw is not None:
    col_options = [""] + get_column_options(df_raw)
    skip_label = t["col_skip"]

    # ── Column Mapping UI ────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown(section_header(t["mapping_header"]), unsafe_allow_html=True)
    st.caption(t["mapping_desc"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**📌 " + ("Kolumny wymagane" if lang == "pl" else "Mandatory columns") + "**")

        mat_idx = st.selectbox(t["col_material_index"], col_options, key="map_idx")
        receipt_date = st.selectbox(t["col_receipt_date"], col_options, key="map_date")
        mat_name = st.selectbox(t["col_material_name"], col_options, key="map_name")
        doc_number = st.selectbox(t["col_doc_number"], col_options, key="map_doc")
        quantity = st.selectbox(t["col_quantity"], col_options, key="map_qty")

    with col2:
        st.markdown("**🔧 " + ("Kolumny opcjonalne" if lang == "pl" else "Optional columns") + "**")

        col_opts_skip = [skip_label] + get_column_options(df_raw)
        value_col = st.selectbox(t["col_value"], col_opts_skip, key="map_val")
        warehouse_col = st.selectbox(t["col_warehouse"], col_opts_skip, key="map_wh")

        if use_batch:
            st.markdown("**🏷️ " + ("Kolumna partii (wymagana)" if lang == "pl" else "Batch column (required)") + "**")
            batch_col = st.selectbox(t["col_batch"], col_options, key="map_batch")
        else:
            batch_col = ""

    # Build mapping dict
    mapping = {
        "material_index": mat_idx if mat_idx else None,
        "receipt_date": receipt_date if receipt_date else None,
        "material_name": mat_name if mat_name else None,
        "doc_number": doc_number if doc_number else None,
        "quantity": quantity if quantity else None,
        "value": value_col if value_col and value_col != skip_label else None,
        "warehouse": warehouse_col if warehouse_col and warehouse_col != skip_label else None,
        "batch": batch_col if batch_col else None,
    }

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Aging Buckets UI ─────────────────────────────────────────────────────
    if bucket_type == t["buckets_custom"]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(section_header(t["buckets_header"]), unsafe_allow_html=True)
        st.info(t.get("bucket_last_unlimited", "Last bucket has no upper bound"))

        if "custom_buckets" not in st.session_state:
            st.session_state.custom_buckets = [
                {"name": t["bucket_0_3"], "from_day": 0, "to_day": 90},
                {"name": t["bucket_3_6"], "from_day": 91, "to_day": 180},
                {"name": t["bucket_1_2"], "from_day": 366, "to_day": 730},
                {"name": t["bucket_2plus"], "from_day": 731, "to_day": None},
            ]

        custom_buckets = st.session_state.custom_buckets
        new_buckets = []
        n = len(custom_buckets)

        for i, b in enumerate(custom_buckets):
            cols_b = st.columns([3, 1, 1, 0.5])
            with cols_b[0]:
                name = st.text_input(f"{t['bucket_name']} {i+1}", value=b.get("name", ""), key=f"bname_{i}", label_visibility="collapsed")
            with cols_b[1]:
                from_d = st.number_input(t["bucket_from"], value=b.get("from_day", 0), min_value=0, key=f"bfrom_{i}", label_visibility="collapsed")
            with cols_b[2]:
                if i == n - 1:
                    st.caption("∞")
                    to_d = None
                else:
                    to_d = st.number_input(t["bucket_to"], value=b.get("to_day") or 0, min_value=0, key=f"bto_{i}", label_visibility="collapsed")
            with cols_b[3]:
                remove = st.button(t["bucket_remove"], key=f"brem_{i}")
                if remove and n > 1:
                    continue
            new_buckets.append({"name": name, "from_day": int(from_d), "to_day": int(to_d) if to_d is not None else None})

        if st.button(t["bucket_add"]):
            last = new_buckets[-1] if new_buckets else {"to_day": 0}
            last_to = last.get("to_day") or 0
            new_buckets.append({"name": "", "from_day": last_to + 1, "to_day": last_to + 90})

        st.session_state.custom_buckets = new_buckets

        # Validate custom buckets
        bucket_errors = validate_custom_buckets(new_buckets)
        if bucket_errors:
            for err in bucket_errors:
                st.error(f"❌ {err}")
        else:
            buckets = new_buckets

        st.markdown("</div>", unsafe_allow_html=True)
    else:
        buckets = get_default_buckets(lang)

    # ── CALCULATE BUTTON ──────────────────────────────────────────────────────
    st.markdown('<div class="section-card">', unsafe_allow_html=True)

    # Info messages
    if not mapping.get("value"):
        st.info(t["info_no_value_col"])
    if not mapping.get("warehouse"):
        st.info(t["info_no_wh_col"])
    if use_batch and not mapping.get("batch"):
        st.warning(t["info_batch_required"])

    calc_col1, calc_col2 = st.columns([2, 1])
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

        # Only recalculate on button click
        if calc_clicked:
            try:
                with st.spinner("Calculating..."):
                    method_label = t["method_batch"] if use_batch else t["method_index"]

                    # Convert quantity to numeric
                    df_work = df_raw.copy()
                    qty_col_name = mapping["quantity"]
                    df_work[qty_col_name] = pd.to_numeric(df_work[qty_col_name], errors="coerce").fillna(0)

                    if mapping.get("value"):
                        val_col_name = mapping["value"]
                        df_work[val_col_name] = pd.to_numeric(df_work[val_col_name], errors="coerce").fillna(0)

                    # Validate data
                    validation_issues = validate_data(df_work, mapping, aging_date, use_batch, t)

                    # Calculate aging
                    df_result = calculate_aging(
                        df_work, mapping, aging_date, buckets, use_batch, method_label, t
                    )

                    # Build summaries
                    df_qty = build_qty_summary(df_result, mapping, buckets, use_batch, t)
                    df_val = build_val_summary(df_result, mapping, buckets, use_batch, t)
                    df_wh = build_warehouse_summary(df_result, mapping, buckets, t)
                    df_batch = build_batch_summary(df_result, mapping, buckets, use_batch, t)

                    # KPI stats
                    stats = build_summary_stats(df_result, mapping, buckets, t)

                    # Format validation log
                    val_log_rows = [[v["row"], v["type"], v["description"], v["severity"]] for v in validation_issues]

                    # Store in session state
                    st.session_state["results_ready"] = True
                    st.session_state["df_result"] = df_result
                    st.session_state["df_qty"] = df_qty
                    st.session_state["df_val"] = df_val
                    st.session_state["df_wh"] = df_wh
                    st.session_state["df_batch"] = df_batch
                    st.session_state["stats"] = stats
                    st.session_state["validation_issues"] = validation_issues
                    st.session_state["val_log_rows"] = val_log_rows
                    st.session_state["buckets_used"] = buckets
                    st.session_state["mapping_used"] = mapping
                    st.session_state["aging_date_used"] = aging_date
                    st.session_state["use_batch_used"] = use_batch

                    st.success(t["calc_success"])

            except Exception as e:
                st.error(f"{t['calc_error']}: {str(e)}")
                with st.expander("Debug info"):
                    st.code(traceback.format_exc())
                st.stop()

        # Retrieve from session state
        if st.session_state.get("results_ready"):
            df_result = st.session_state["df_result"]
            df_qty = st.session_state["df_qty"]
            df_val = st.session_state["df_val"]
            df_wh = st.session_state["df_wh"]
            df_batch = st.session_state["df_batch"]
            stats = st.session_state["stats"]
            validation_issues = st.session_state["validation_issues"]
            val_log_rows = st.session_state["val_log_rows"]
            buckets_used = st.session_state["buckets_used"]
            mapping_used = st.session_state["mapping_used"]
            aging_date_used = st.session_state["aging_date_used"]
            use_batch_used = st.session_state["use_batch_used"]

            # ── BUILD TABS ────────────────────────────────────────────────────
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

            # ── TAB: Dashboard ────────────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["dashboard_header"]), unsafe_allow_html=True)
                render_kpis(stats, t)
                st.write("")

                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    chart_aging_qty(
                        df_result, t["out_bucket"], mapping_used["quantity"], t, buckets_used
                    )
                with col_c2:
                    if mapping_used.get("value"):
                        chart_aging_val(df_result, t["out_bucket"], mapping_used["value"], t, buckets_used)

                if mapping_used.get("warehouse"):
                    chart_aging_warehouse(
                        df_result, mapping_used["warehouse"], t["out_bucket"], mapping_used["quantity"], t, buckets_used
                    )

                col_c3, col_c4 = st.columns(2)
                with col_c3:
                    chart_top10_oldest(
                        df_result, mapping_used["material_index"], mapping_used["material_name"],
                        t["out_age_days"], mapping_used["quantity"], t
                    )
                with col_c4:
                    if mapping_used.get("value"):
                        chart_top10_value(
                            df_result, mapping_used["material_index"], mapping_used["material_name"],
                            mapping_used["value"], t
                        )

            # ── TAB: Detailed Data ────────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["tab_detail"]), unsafe_allow_html=True)
                st.dataframe(df_result.drop(columns=["_bucket_order"], errors="ignore"), use_container_width=True, hide_index=True)

            # ── TAB: Quantity Summary ─────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["tab_qty_summary"]), unsafe_allow_html=True)
                st.dataframe(df_qty, use_container_width=True, hide_index=True)

            # ── TAB: Value Summary ────────────────────────────────────────────
            if df_val is not None:
                with tab_objs[tab_idx]:
                    tab_idx += 1
                    st.markdown(section_header(t["tab_val_summary"]), unsafe_allow_html=True)
                    st.dataframe(df_val, use_container_width=True, hide_index=True)

            # ── TAB: Warehouse Summary ────────────────────────────────────────
            if df_wh is not None:
                with tab_objs[tab_idx]:
                    tab_idx += 1
                    st.markdown(section_header(t["tab_wh_summary"]), unsafe_allow_html=True)
                    st.dataframe(df_wh, use_container_width=True, hide_index=True)

            # ── TAB: Batch Summary ────────────────────────────────────────────
            if df_batch is not None:
                with tab_objs[tab_idx]:
                    tab_idx += 1
                    st.markdown(section_header(t["tab_batch_summary"]), unsafe_allow_html=True)
                    st.dataframe(df_batch, use_container_width=True, hide_index=True)

            # ── TAB: Validation ───────────────────────────────────────────────
            with tab_objs[tab_idx]:
                tab_idx += 1
                st.markdown(section_header(t["validation_header"]), unsafe_allow_html=True)
                render_validation_table(validation_issues, t)

            # ── EXCEL DOWNLOAD ────────────────────────────────────────────────
            st.markdown("---")
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            st.markdown(section_header(t["download_button"]), unsafe_allow_html=True)

            with st.spinner(t.get("download_generating", "Generating...")):
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
    # No file uploaded — show instructions
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
