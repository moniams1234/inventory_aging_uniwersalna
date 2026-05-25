# modules/ui_components.py
# Charts, KPI cards, validation table — FA Fin Apps SaaS style

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from modules.styling import kpi_card

# ── FA brand palette ──────────────────────────────────────────────────────────
FA_COLORS = [
    "#1B2B4B",  # navy
    "#3498DB",  # blue
    "#2E86AB",  # teal-blue
    "#A8DADC",  # light teal
    "#C0392B",  # red
    "#E67E22",  # orange
    "#F39C12",  # amber
    "#95A5A6",  # grey
]

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter, sans-serif", size=12, color="#1B2B4B"),
    margin=dict(l=10, r=10, t=44, b=10),
    title_font=dict(size=14, color="#1B2B4B", family="Inter, sans-serif"),
)


def _bucket_agg(df, bucket_col, value_col, buckets):
    bucket_order = [b["name"] for b in buckets]
    agg = df.groupby(bucket_col)[value_col].sum().reset_index()
    agg = agg.set_index(bucket_col).reindex(bucket_order).reset_index().dropna(subset=[value_col])
    return agg


def render_kpis(stats: dict, t: dict):
    """Render KPI cards in 4-column layout."""
    def fmt_num(v, decimals=2):
        if v is None: return "N/A"
        if isinstance(v, float): return f"{v:,.{decimals}f}"
        return f"{int(v):,}"

    def fmt_pct(v):
        if v is None: return "N/A"
        return f"{v:.1f}%"

    n_records = stats.get("n_records", "N/A")
    n_batches = stats.get("n_batches")

    row1 = [
        (t["kpi_total_records"], fmt_num(n_records, 0) if n_records != "N/A" else "N/A", "🗂️", "", ""),
        (t["kpi_total_qty"],     fmt_num(stats.get("total_qty")), "📦", "", ""),
        (t["kpi_total_value"],   fmt_num(stats.get("total_value")), "💰", "", "accent-blue"),
        (t["kpi_materials"],     fmt_num(stats.get("n_materials"), 0), "🏷️", "", ""),
    ]
    row2 = [
        (t["kpi_warehouses"],  fmt_num(stats.get("n_warehouses"), 0) if stats.get("n_warehouses") is not None else "N/A", "🏭", "", ""),
        (t["kpi_batches"],     fmt_num(n_batches, 0) if n_batches is not None else "N/A", "🔖", "", ""),
        (t["kpi_above_1y"],    fmt_pct(stats.get("above_1y_pct")), "⏳", "warning" if (stats.get("above_1y_pct") or 0) > 20 else "", "accent-red"),
        (t["kpi_above_2y"],    fmt_pct(stats.get("above_2y_pct")), "🔴", "danger"  if (stats.get("above_2y_pct") or 0) > 10 else "", "accent-red"),
    ]

    for row in [row1, row2]:
        cols = st.columns(4)
        for i, (label, value, icon, cls, accent) in enumerate(row):
            with cols[i]:
                st.markdown(kpi_card(label, value, icon, cls, accent), unsafe_allow_html=True)
                st.write("")


def chart_aging_qty(df: pd.DataFrame, bucket_col: str, qty_col: str, t: dict, buckets: list):
    """Donut chart — aging by quantity (matches reference image)."""
    agg = _bucket_agg(df, bucket_col, qty_col, buckets)
    total = agg[qty_col].sum()

    fig = go.Figure(go.Pie(
        labels=agg[bucket_col],
        values=agg[qty_col],
        hole=0.52,
        marker_colors=FA_COLORS[:len(agg)],
        textinfo="percent",
        textfont_size=11,
        hovertemplate="%{label}<br>%{value:,.2f} (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=t["chart_qty_title"], x=0, xanchor="left"),
        legend=dict(orientation="v", x=1.02, y=0.5, font_size=11),
        annotations=[dict(
            text=f"<b>{total:,.0f}</b><br><span style='font-size:10px'>{t.get('chart_total_qty_label','Total')}</span>",
            x=0.5, y=0.5, showarrow=False, font_size=13, align="center"
        )],
        showlegend=True,
        height=300,
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_aging_val(df: pd.DataFrame, bucket_col: str, val_col: str, t: dict, buckets: list):
    """Horizontal bar chart — aging by value (matches reference image)."""
    agg = _bucket_agg(df, bucket_col, val_col, buckets)

    fig = go.Figure(go.Bar(
        y=agg[bucket_col],
        x=agg[val_col],
        orientation="h",
        marker_color=FA_COLORS[:len(agg)],
        text=[f"{v/1e6:.2f}M" if v >= 1e6 else f"{v:,.0f}" for v in agg[val_col]],
        textposition="outside",
        hovertemplate="%{y}<br>%{x:,.2f}<extra></extra>",
    ))
    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=t["chart_val_title"], x=0, xanchor="left"),
        xaxis=dict(showgrid=True, gridcolor="#EEF1F7", zeroline=False, title=t["chart_val_axis"]),
        yaxis=dict(autorange="reversed", tickfont_size=11),
        height=300,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_aging_warehouse(df: pd.DataFrame, wh_col: str, bucket_col: str, qty_col: str, t: dict, buckets: list):
    """Horizontal grouped bar — top warehouses by value (matches reference)."""
    bucket_order = [b["name"] for b in buckets]
    agg = df.groupby([wh_col, bucket_col])[qty_col].sum().reset_index()

    # Pivot → total per warehouse → top 5
    wh_totals = agg.groupby(wh_col)[qty_col].sum().nlargest(5).index
    agg = agg[agg[wh_col].isin(wh_totals)]

    fig = go.Figure()
    for i, bname in enumerate(bucket_order):
        sub = agg[agg[bucket_col] == bname]
        if sub.empty: continue
        fig.add_trace(go.Bar(
            y=sub[wh_col], x=sub[qty_col],
            name=bname, orientation="h",
            marker_color=FA_COLORS[i % len(FA_COLORS)],
            hovertemplate=f"{bname}<br>%{{y}}<br>%{{x:,.2f}}<extra></extra>",
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=t["chart_wh_title"], x=0, xanchor="left"),
        barmode="stack",
        xaxis=dict(showgrid=True, gridcolor="#EEF1F7", zeroline=False, title=t["chart_qty_axis"]),
        yaxis=dict(autorange="reversed", tickfont_size=11),
        legend=dict(orientation="h", y=-0.22, x=0, font_size=10),
        height=320,
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_top10_oldest(df: pd.DataFrame, idx_col: str, name_col: str,
                       age_days_col: str, qty_col: str, t: dict):
    """Horizontal bar — top 5 material groups by quantity (reference style)."""
    agg = (
        df.groupby([idx_col, name_col])
        .agg(total_qty=(qty_col, "sum"), max_age=(age_days_col, "max"))
        .reset_index()
        .nlargest(5, "total_qty")
    )
    agg["label"] = agg[name_col].str[:28].fillna(agg[idx_col].astype(str))

    fig = go.Figure()
    max_val = agg["total_qty"].max() if not agg.empty else 1

    for _, row in agg.iterrows():
        fig.add_trace(go.Bar(
            y=[row["label"]], x=[row["total_qty"]],
            orientation="h",
            marker=dict(color=FA_COLORS[1], opacity=0.85),
            text=[f"{row['total_qty']:,.0f}"],
            textposition="outside",
            hovertemplate=f"{row['label']}<br>{t['chart_qty_axis']}: %{{x:,.2f}}<extra></extra>",
            showlegend=False,
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=t["chart_top10_old"], x=0, xanchor="left"),
        xaxis=dict(showgrid=True, gridcolor="#EEF1F7", zeroline=False, range=[0, max_val * 1.22]),
        yaxis=dict(autorange="reversed", tickfont_size=11),
        height=280,
        showlegend=False,
        barmode="overlay",
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_top10_value(df: pd.DataFrame, idx_col: str, name_col: str, val_col: str, t: dict):
    """Horizontal bar — top 5 warehouses by value (reference style)."""
    agg = (
        df.groupby([idx_col, name_col])[val_col].sum()
        .reset_index().nlargest(5, val_col)
    )
    agg["label"] = agg[name_col].str[:28].fillna(agg[idx_col].astype(str))

    max_val = agg[val_col].max() if not agg.empty else 1

    fig = go.Figure()
    for _, row in agg.iterrows():
        fig.add_trace(go.Bar(
            y=[row["label"]], x=[row[val_col]],
            orientation="h",
            marker=dict(color=FA_COLORS[0], opacity=0.82),
            text=[f"{row[val_col]/1e6:.2f}M" if row[val_col] >= 1e6 else f"{row[val_col]:,.0f}"],
            textposition="outside",
            hovertemplate=f"{row['label']}<br>{t['chart_val_axis']}: %{{x:,.2f}}<extra></extra>",
            showlegend=False,
        ))

    fig.update_layout(
        **PLOTLY_LAYOUT,
        title=dict(text=t["chart_top10_val"], x=0, xanchor="left"),
        xaxis=dict(showgrid=True, gridcolor="#EEF1F7", zeroline=False, range=[0, max_val * 1.22]),
        yaxis=dict(autorange="reversed", tickfont_size=11),
        height=280,
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)


def render_validation_table(issues: list, t: dict):
    if not issues:
        st.success(t["val_no_issues"])
        return
    st.warning(f"⚠️ {len(issues)} {t['val_issues_found']}")
    df_issues = pd.DataFrame(issues)
    df_issues.columns = [t["val_row"], t["val_type"], t["val_desc"], t["val_severity"]]
    st.dataframe(df_issues, use_container_width=True, hide_index=True)
