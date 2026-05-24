# modules/styling.py
# Custom CSS and styling for Streamlit application

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

/* ─── Root variables ─────────────────────────────── */
:root {
    --primary: #1E3A5F;
    --primary-light: #2E6DA4;
    --accent: #3498DB;
    --accent-light: #EBF5FB;
    --success: #27AE60;
    --warning: #F39C12;
    --danger: #E74C3C;
    --bg: #F7F9FC;
    --card-bg: #FFFFFF;
    --border: #E2E8F0;
    --text: #2D3748;
    --text-muted: #718096;
    --shadow: 0 2px 12px rgba(30,58,95,0.08);
    --shadow-hover: 0 6px 24px rgba(30,58,95,0.15);
    --radius: 12px;
}

/* ─── Global ─────────────────────────────────────── */
.stApp {
    background-color: var(--bg) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text) !important;
}

/* ─── Cursor pointer — interactive elements ──────── */
button,
[role="button"],
.stButton > button,
.stDownloadButton > button,
[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] div[role="button"],
[data-baseweb="select"] *,
[data-baseweb="radio"] label,
[data-baseweb="checkbox"] label,
[data-testid="stDateInput"] input,
[data-testid="stDateInput"] div,
[data-testid="stNumberInput"] button,
.stRadio label,
.stCheckbox label,
label[data-testid],
[role="option"],
[role="radio"],
[role="checkbox"],
select,
input[type="radio"],
input[type="checkbox"],
.stSelectbox label,
.stMultiSelect label {
    cursor: pointer !important;
}

/* ─── Sidebar ────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1E3A5F 0%, #2E6DA4 100%) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stNumberInput label {
    color: #C8DCF0 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.03em !important;
    text-transform: uppercase !important;
}

/* ─── Fix: date input text visible in sidebar ────── */
[data-testid="stSidebar"] [data-testid="stDateInput"] input,
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="number"] {
    color: #1F2937 !important;
    background: rgba(255,255,255,0.95) !important;
    border: 1px solid rgba(255,255,255,0.4) !important;
    border-radius: 7px !important;
}
[data-testid="stSidebar"] [data-testid="stDateInput"] div[data-baseweb="input"] {
    background: rgba(255,255,255,0.95) !important;
    border-radius: 7px !important;
}
/* Number inputs in sidebar */
[data-testid="stSidebar"] [data-testid="stNumberInput"] input {
    color: #1F2937 !important;
    background: rgba(255,255,255,0.95) !important;
}
/* Text inputs in sidebar (bucket names) */
[data-testid="stSidebar"] input[type="text"] {
    color: #1F2937 !important;
    background: rgba(255,255,255,0.92) !important;
}

[data-testid="stSidebar"] .stSelectbox > div > div {
    background: rgba(255,255,255,0.12) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 8px !important;
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
    font-family: 'DM Serif Display', serif !important;
}
[data-testid="stSidebar"] .stRadio > div {
    background: rgba(255,255,255,0.08) !important;
    border-radius: 8px !important;
    padding: 8px !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.2) !important;
}

/* ─── Bucket badge list in sidebar ───────────────── */
.bucket-badge {
    display: inline-block;
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.78rem;
    color: #E8F4FD !important;
    margin: 2px 2px;
    white-space: nowrap;
}
.bucket-badge-container {
    display: flex;
    flex-wrap: wrap;
    gap: 4px;
    margin-top: 6px;
    padding: 8px;
    background: rgba(0,0,0,0.12);
    border-radius: 8px;
}

/* ─── Sidebar small remove button ────────────────── */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(231,76,60,0.7) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 6px !important;
    font-size: 0.75rem !important;
    padding: 4px 10px !important;
    box-shadow: none !important;
    width: 100% !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(192,57,43,0.9) !important;
    transform: none !important;
}

/* ─── Main header ────────────────────────────────── */
.app-header {
    background: linear-gradient(135deg, #1E3A5F 0%, #2E6DA4 100%);
    border-radius: var(--radius);
    padding: 28px 36px;
    margin-bottom: 28px;
    box-shadow: var(--shadow-hover);
    position: relative;
    overflow: hidden;
}
.app-header::before {
    content: '';
    position: absolute;
    top: -30px; right: -30px;
    width: 180px; height: 180px;
    border-radius: 50%;
    background: rgba(255,255,255,0.06);
}
.app-header h1 {
    color: #FFFFFF !important;
    font-family: 'DM Serif Display', serif !important;
    font-size: 2rem !important;
    margin: 0 !important;
    line-height: 1.2 !important;
}
.app-header p {
    color: #A8CAEB !important;
    margin: 4px 0 0 0 !important;
    font-size: 0.95rem !important;
}

/* ─── Section cards ──────────────────────────────── */
.section-card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 24px 28px;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    transition: box-shadow 0.2s ease;
}
.section-card:hover {
    box-shadow: var(--shadow-hover);
}
.section-title {
    color: var(--primary) !important;
    font-size: 1.1rem !important;
    font-weight: 700 !important;
    margin-bottom: 16px !important;
    padding-bottom: 10px !important;
    border-bottom: 2px solid var(--accent-light) !important;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ─── KPI cards ──────────────────────────────────── */
.kpi-card {
    background: var(--card-bg);
    border-radius: var(--radius);
    padding: 20px 24px;
    box-shadow: var(--shadow);
    border: 1px solid var(--border);
    border-left: 4px solid var(--accent);
    transition: all 0.25s ease;
    height: 100%;
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
}
.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 6px;
}
.kpi-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary);
    line-height: 1;
}
.kpi-value.danger { color: var(--danger); }
.kpi-value.warning { color: var(--warning); }
.kpi-value.success { color: var(--success); }
.kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 8px;
}

/* ─── Upload area ────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--accent) !important;
    border-radius: var(--radius) !important;
    background: var(--accent-light) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
}
[data-testid="stFileUploader"]:hover {
    background: #D6EAF8 !important;
    border-color: var(--primary) !important;
}

/* ─── Main area buttons ──────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 10px 24px !important;
    transition: all 0.25s ease !important;
    box-shadow: 0 2px 8px rgba(30,58,95,0.25) !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(30,58,95,0.35) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ─── Download button ────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--success) 0%, #2ECC71 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 12px 28px !important;
    box-shadow: 0 2px 8px rgba(39,174,96,0.3) !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
    font-size: 1rem !important;
    cursor: pointer !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(39,174,96,0.4) !important;
}

/* ─── Tabs ───────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card-bg) !important;
    border-radius: var(--radius) var(--radius) 0 0 !important;
    border-bottom: 2px solid var(--border) !important;
    padding: 0 8px !important;
    gap: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px 8px 0 0 !important;
    font-weight: 500 !important;
    color: var(--text-muted) !important;
    transition: all 0.2s ease !important;
    padding: 10px 18px !important;
    cursor: pointer !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-light) !important;
    color: var(--primary) !important;
    font-weight: 700 !important;
    border-bottom: 2px solid var(--accent) !important;
}

/* ─── DataFrames ─────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: var(--radius) !important;
    overflow: hidden !important;
    border: 1px solid var(--border) !important;
}

/* ─── Alerts ─────────────────────────────────────── */
.stAlert {
    border-radius: var(--radius) !important;
}

/* ─── Selectboxes ────────────────────────────────── */
.stSelectbox > div > div {
    border-radius: 8px !important;
    border-color: var(--border) !important;
    cursor: pointer !important;
}

/* ─── Number inputs ──────────────────────────────── */
.stNumberInput > div > div > input {
    border-radius: 8px !important;
    border-color: var(--border) !important;
    cursor: text !important;
}

/* ─── Expanders ──────────────────────────────────── */
.streamlit-expanderHeader {
    background: var(--accent-light) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    color: var(--primary) !important;
    cursor: pointer !important;
}

/* ─── Metrics ────────────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--card-bg) !important;
    border-radius: var(--radius) !important;
    padding: 16px !important;
    border: 1px solid var(--border) !important;
    box-shadow: var(--shadow) !important;
}

/* ─── Footer ─────────────────────────────────────── */
.app-footer {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.78rem;
    padding: 24px 0 12px;
    border-top: 1px solid var(--border);
    margin-top: 40px;
}
</style>
"""


def inject_css():
    """Inject custom CSS into Streamlit app."""
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def kpi_card(label: str, value: str, icon: str = "📊", css_class: str = "") -> str:
    """Render a KPI card HTML block."""
    return f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {css_class}">{value}</div>
    </div>
    """


def section_header(title: str) -> str:
    return f'<div class="section-title">{title}</div>'


def app_header(title: str, subtitle: str) -> str:
    return f"""
    <div class="app-header">
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """


def default_buckets_html(buckets: list) -> str:
    """Render default bucket list as badge HTML for sidebar."""
    badges = "".join(
        f'<span class="bucket-badge">{b["name"]}</span>' for b in buckets
    )
    return f'<div class="bucket-badge-container">{badges}</div>'
