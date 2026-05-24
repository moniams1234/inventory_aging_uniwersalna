# modules/ui_components.py
# Reusable UI component functions

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.styling import kpi_card


PLOTLY_COLORS = [
    "#2E6DA4", "#27AE60", "#F39C12", "#E74C3C",
    "#8E44AD", "#16A085", "#D35400", "#2C3E50"
]


def render_kpis(stats: dict, t: dict):
    """Render KPI cards row."""
    cols = st.columns(3)

    def fmt_num(v):
        if v is None:
            return "N/A"
        if isinstance(v, float):
            return f"{v:,.2f}"
        return f"{int(v):,}"

    def fmt_pct(v):
        if v is None:
            return "N/A"
        return f"{v:.1f}%"

    kpis = [
        (t["kpi_total_qty"], fmt_num(stats.get("total_qty")), "📦", ""),
        (t["kpi_total_value"], fmt_num(stats.get("total_value")), "💰", ""),
        (t["kpi_materials"], fmt_num(stats.get("n_materials")), "🏷️", ""),
    ]

    for i, (label, value, icon, cls) in enumerate(kpis):
        if value == "N/A" and label == t["kpi_total_value"]:
            continue
        with cols[i % 3]:
            st.markdown(kpi_card(label, value, icon, cls), unsafe_allow_html=True)
            st.write("")

    cols2 = st.columns(3)
    above_1y = stats.get("above_1y_pct", 0)
    above_2y = stats.get("above_2y_pct", 0)
    n_wh = stats.get("n_warehouses")

    kpis2 = [
        (t["kpi_above_1y"], fmt_pct(above_1y), "⏳", "warning" if above_1y > 20 else ""),
        (t["kpi_above_2y"], fmt_pct(above_2y), "🔴", "danger" if above_2y > 10 else ""),
        (t["kpi_warehouses"], fmt_num(n_wh) if n_wh else "N/A", "🏭", ""),
    ]
    for i, (label, value, icon, cls) in enumerate(kpis2):
        with cols2[i]:
            st.markdown(kpi_card(label, value, icon, cls), unsafe_allow_html=True)
            st.write("")


def chart_aging_qty(df: pd.DataFrame, bucket_col: str, qty_col: str, t: dict, buckets: list):
    """Bar chart: aging by quantity."""
    bucket_order = [b["name"] for b in buckets]
    agg = df.groupby(bucket_col)[qty_col].sum().reset_index()
    agg = agg.set_index(bucket_col).reindex(bucket_order).reset_index().dropna(subset=[qty_col])

    fig = px.bar(
        agg, x=bucket_col, y=qty_col,
        title=t["chart_qty_title"],
        labels={bucket_col: t["chart_bucket_axis"], qty_col: t["chart_qty_axis"]},
        color=bucket_col,
        color_discrete_sequence=PLOTLY_COLORS,
        template="plotly_white"
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(size=15, color="#1E3A5F"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    fig.update_traces(marker_line_width=0)
    st.plotly_chart(fig, use_container_width=True)


def chart_aging_val(df: pd.DataFrame, bucket_col: str, val_col: str, t: dict, buckets: list):
    """Bar chart: aging by value."""
    bucket_order = [b["name"] for b in buckets]
    agg = df.groupby(bucket_col)[val_col].sum().reset_index()
    agg = agg.set_index(bucket_col).reindex(bucket_order).reset_index().dropna(subset=[val_col])

    fig = px.bar(
        agg, x=bucket_col, y=val_col,
        title=t["chart_val_title"],
        labels={bucket_col: t["chart_bucket_axis"], val_col: t["chart_val_axis"]},
        color=bucket_col,
        color_discrete_sequence=PLOTLY_COLORS[::-1],
        template="plotly_white"
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(size=15, color="#1E3A5F"),
        margin=dict(l=20, r=20, t=50, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_aging_warehouse(df: pd.DataFrame, wh_col: str, bucket_col: str, qty_col: str, t: dict, buckets: list):
    """Stacked bar: aging by warehouse."""
    bucket_order = [b["name"] for b in buckets]
    agg = df.groupby([wh_col, bucket_col])[qty_col].sum().reset_index()

    fig = px.bar(
        agg, x=wh_col, y=qty_col, color=bucket_col,
        title=t["chart_wh_title"],
        labels={wh_col: t["chart_wh_axis"], qty_col: t["chart_qty_axis"], bucket_col: ""},
        color_discrete_sequence=PLOTLY_COLORS,
        template="plotly_white",
        barmode="stack",
        category_orders={bucket_col: bucket_order}
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=12),
        title_font=dict(size=15, color="#1E3A5F"),
        margin=dict(l=20, r=20, t=50, b=20),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_top10_oldest(df: pd.DataFrame, idx_col: str, name_col: str, age_days_col: str, qty_col: str, t: dict):
    """Horizontal bar: top 10 oldest material indexes."""
    agg = df.groupby([idx_col, name_col]).agg(
        max_age=(age_days_col, "max"),
        total_qty=(qty_col, "sum")
    ).reset_index().nlargest(10, "max_age")

    agg["label"] = agg[idx_col].astype(str) + " - " + agg[name_col].astype(str).str[:30]

    fig = px.bar(
        agg, y="label", x="max_age",
        orientation="h",
        title=t["chart_top10_old"],
        labels={"label": t["chart_material_axis"], "max_age": t["out_age_days"] if "out_age_days" in t else "Age (days)"},
        color="max_age",
        color_continuous_scale=["#85C1E9", "#E74C3C"],
        template="plotly_white"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11),
        title_font=dict(size=15, color="#1E3A5F"),
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_top10_value(df: pd.DataFrame, idx_col: str, name_col: str, val_col: str, t: dict):
    """Horizontal bar: top 10 highest value aged items."""
    agg = df.groupby([idx_col, name_col])[val_col].sum().reset_index().nlargest(10, val_col)
    agg["label"] = agg[idx_col].astype(str) + " - " + agg[name_col].astype(str).str[:30]

    fig = px.bar(
        agg, y="label", x=val_col,
        orientation="h",
        title=t["chart_top10_val"],
        labels={"label": t["chart_material_axis"], val_col: t["chart_val_axis"]},
        color=val_col,
        color_continuous_scale=["#A9DFBF", "#1E8449"],
        template="plotly_white"
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", size=11),
        title_font=dict(size=15, color="#1E3A5F"),
        margin=dict(l=20, r=20, t=50, b=20),
        showlegend=False,
        coloraxis_showscale=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_validation_table(issues: list, t: dict):
    """Render validation issues as styled dataframe."""
    if not issues:
        st.success(t["val_no_issues"])
        return

    st.warning(f"⚠️ {len(issues)} {t['val_issues_found']}")
    df_issues = pd.DataFrame(issues)
    df_issues.columns = [t["val_row"], t["val_type"], t["val_desc"], t["val_severity"]]
    st.dataframe(df_issues, use_container_width=True, hide_index=True)
