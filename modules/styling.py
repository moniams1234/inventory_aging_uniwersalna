# modules/styling.py
# Custom CSS — FA Fin Apps commercial SaaS style

import base64
import os

_LOGO_B64 = None

def _get_logo_b64() -> str:
    global _LOGO_B64
    if _LOGO_B64 is None:
        logo_path = os.path.join(os.path.dirname(__file__), "..", "assets", "fa_logo.png")
        logo_path = os.path.normpath(logo_path)
        try:
            with open(logo_path, "rb") as f:
                _LOGO_B64 = base64.b64encode(f.read()).decode()
        except Exception:
            _LOGO_B64 = ""
    return _LOGO_B64


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=DM+Serif+Display&display=swap');

:root {
    --navy:        #1B2B4B;
    --navy-mid:    #243654;
    --navy-light:  #2E4A73;
    --red:         #C0392B;
    --red-light:   #E74C3C;
    --red-muted:   #fadbd8;
    --blue-accent: #3498DB;
    --bg:          #F4F6FA;
    --bg2:         #EEF1F7;
    --card:        #FFFFFF;
    --border:      #E0E6EF;
    --text:        #1B2B4B;
    --text-mid:    #4A5568;
    --text-muted:  #8A9BB5;
    --success:     #27AE60;
    --warning:     #E67E22;
    --shadow-sm:   0 1px 4px rgba(27,43,75,0.07);
    --shadow:      0 3px 14px rgba(27,43,75,0.10);
    --shadow-lg:   0 8px 32px rgba(27,43,75,0.14);
    --radius:      12px;
    --radius-sm:   8px;
}

/* ── Global reset ─────────────────────────────────── */
.stApp { background: var(--bg) !important; font-family: 'Inter', sans-serif !important; color: var(--text) !important; }
* { box-sizing: border-box; }

/* ── Cursor ───────────────────────────────────────── */
button, [role="button"], .stButton > button, .stDownloadButton > button,
[data-testid="stFileUploader"] label, [data-testid="stFileUploader"] div[role="button"],
[data-baseweb="select"] *, [data-baseweb="radio"] label, [data-baseweb="checkbox"] label,
[data-testid="stDateInput"] input, [data-testid="stDateInput"] div,
.stRadio label, .stCheckbox label, label[data-testid],
[role="option"], [role="radio"], [role="checkbox"], select,
input[type="radio"], input[type="checkbox"],
.stSelectbox label, .stMultiSelect label,
.stTabs [data-baseweb="tab"] { cursor: pointer !important; }

/* ═══════════════════════════════════════════════════
   SIDEBAR — light professional
═══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: 2px 0 12px rgba(27,43,75,0.06) !important;
}
[data-testid="stSidebar"] * { color: var(--text) !important; }

/* sidebar logo area */
.sb-logo-wrap {
    display: flex; align-items: center; gap: 10px;
    padding: 6px 0 14px 0; border-bottom: 1px solid var(--border); margin-bottom: 14px;
}
.sb-logo-wrap img { width: 44px; height: 44px; object-fit: contain; border-radius: 8px; }
.sb-logo-text { line-height: 1.15; }
.sb-logo-text .sb-brand { font-size: 0.95rem; font-weight: 800; color: var(--navy) !important; letter-spacing: -0.01em; }
.sb-logo-text .sb-sub   { font-size: 0.65rem; color: var(--text-muted) !important; text-transform: uppercase; letter-spacing: 0.06em; }

/* sidebar section labels */
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stNumberInput > label,
[data-testid="stSidebar"] .stDateInput > label {
    font-size: 0.70rem !important; font-weight: 700 !important;
    text-transform: uppercase !important; letter-spacing: 0.06em !important;
    color: var(--text-muted) !important; margin-bottom: 3px !important;
}
[data-testid="stSidebar"] .stRadio > div {
    background: var(--bg) !important; border-radius: var(--radius-sm) !important; padding: 6px 8px !important;
}
[data-testid="stSidebar"] [data-testid="stDateInput"] input,
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="number"] {
    color: var(--text) !important; background: #fff !important;
    border: 1px solid var(--border) !important; border-radius: 6px !important;
}
[data-testid="stSidebar"] hr { border-color: var(--border) !important; margin: 10px 0 !important; }

/* ── Bucket badge list (default) ─────────────────── */
.bucket-badge {
    display: inline-block; background: #EEF1F7; border: 1px solid var(--border);
    border-radius: 20px; padding: 2px 9px; font-size: 0.72rem;
    color: var(--navy) !important; margin: 2px 2px; white-space: nowrap;
}
.bucket-badge-container { display: flex; flex-wrap: wrap; gap: 3px; margin-top: 5px; padding: 7px; background: var(--bg); border-radius: 8px; }

/* ── Custom bucket cards ────────────────────────── */
.cb-card {
    background: var(--bg); border: 1px solid var(--border);
    border-left: 3px solid var(--red); border-radius: 7px;
    padding: 5px 7px 3px 7px; margin-bottom: 4px;
}
.cb-card-header { font-size: 0.65rem; font-weight: 700; color: var(--red) !important; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 2px; }
.cb-hint { font-size: 0.68rem; color: var(--text-muted) !important; margin-bottom: 5px; line-height: 1.3; padding: 5px 7px; background: var(--bg2); border-radius: 6px; border-left: 2px solid var(--red); }

/* compact inputs in custom bucket section */
[data-testid="stSidebar"] .cb-inputs [data-testid="stNumberInput"] input,
[data-testid="stSidebar"] .cb-inputs [data-testid="stTextInput"] input {
    height: 26px !important; min-height: 26px !important;
    padding: 1px 5px !important; font-size: 0.75rem !important;
}
[data-testid="stSidebar"] .cb-inputs .stNumberInput,
[data-testid="stSidebar"] .cb-inputs .stTextInput { margin-bottom: 1px !important; }
[data-testid="stSidebar"] .cb-inputs label { font-size: 0.62rem !important; margin-bottom: 0 !important; padding-bottom: 0 !important; }

/* cb remove button */
[data-testid="stSidebar"] .cb-remove button {
    background: #FDECEA !important; color: var(--red) !important;
    border: 1px solid #f5c6c2 !important; border-radius: 5px !important;
    font-size: 0.65rem !important; padding: 1px 8px !important;
    min-height: 20px !important; height: 20px !important; box-shadow: none !important; cursor: pointer !important;
}
[data-testid="stSidebar"] .cb-remove button:hover { background: var(--red-muted) !important; transform: none !important; }

/* cb add button */
[data-testid="stSidebar"] .cb-add button {
    background: var(--bg) !important; color: var(--navy) !important;
    border: 1px dashed var(--border) !important; border-radius: 6px !important;
    font-size: 0.72rem !important; padding: 4px 10px !important; box-shadow: none !important;
    cursor: pointer !important; width: 100% !important;
}
[data-testid="stSidebar"] .cb-add button:hover { background: var(--bg2) !important; border-color: var(--navy-light) !important; transform: none !important; }

/* override ALL sidebar buttons (keep light) */
[data-testid="stSidebar"] .stButton > button {
    background: var(--bg) !important; color: var(--navy) !important;
    border: 1px solid var(--border) !important; border-radius: 6px !important;
    font-size: 0.72rem !important; padding: 4px 10px !important; box-shadow: none !important;
    cursor: pointer !important;
}
[data-testid="stSidebar"] .stButton > button:hover { background: var(--bg2) !important; transform: none !important; }

/* ═══════════════════════════════════════════════════
   MAIN AREA
═══════════════════════════════════════════════════ */

/* ── App header ───────────────────────────────────── */
.app-header {
    background: linear-gradient(120deg, var(--navy) 0%, var(--navy-light) 100%);
    border-radius: var(--radius); padding: 28px 36px 24px 36px;
    margin-bottom: 24px; box-shadow: var(--shadow-lg);
    position: relative; overflow: hidden; display: flex; align-items: center; gap: 20px;
}
.app-header::after {
    content: ''; position: absolute; right: -60px; top: -60px;
    width: 220px; height: 220px; border-radius: 50%;
    background: rgba(255,255,255,0.04);
}
.app-header::before {
    content: ''; position: absolute; right: 80px; bottom: -40px;
    width: 120px; height: 120px; border-radius: 50%;
    background: rgba(192,57,43,0.15);
}
.app-header-logo { flex-shrink: 0; }
.app-header-logo img { width: 64px; height: 64px; object-fit: contain; border-radius: 10px; }
.app-header-text h1 {
    color: #FFFFFF !important; font-family: 'Inter', sans-serif !important;
    font-size: 1.75rem !important; font-weight: 800 !important;
    margin: 0 0 4px 0 !important; line-height: 1.15 !important; letter-spacing: -0.02em !important;
}
.app-header-text p { color: rgba(255,255,255,0.72) !important; margin: 0 !important; font-size: 0.88rem !important; line-height: 1.4 !important; }
.app-header-red-bar { width: 40px; height: 3px; background: var(--red); border-radius: 2px; margin: 6px 0; }

/* ── Hero section ─────────────────────────────────── */
.hero-section {
    background: var(--card); border-radius: var(--radius);
    padding: 28px 32px; margin-bottom: 20px;
    box-shadow: var(--shadow-sm); border: 1px solid var(--border);
}
.hero-section h2 { color: var(--navy) !important; font-size: 1.25rem !important; font-weight: 700 !important; margin: 0 0 6px 0 !important; }
.hero-section .hero-sub { color: var(--text-mid) !important; font-size: 0.9rem !important; margin-bottom: 18px !important; }
.feat-grid { display: flex; flex-wrap: wrap; gap: 8px; }
.feat-pill {
    display: inline-flex; align-items: center; gap: 6px;
    background: #EEF1F7; border: 1px solid var(--border);
    border-radius: 20px; padding: 5px 13px;
    font-size: 0.78rem; font-weight: 600; color: var(--navy) !important;
}
.feat-pill .feat-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--red); flex-shrink: 0; }

/* ── Section cards ────────────────────────────────── */
.section-card {
    background: var(--card); border-radius: var(--radius);
    padding: 22px 26px; margin-bottom: 18px;
    box-shadow: var(--shadow-sm); border: 1px solid var(--border);
    transition: box-shadow 0.2s;
}
.section-card:hover { box-shadow: var(--shadow); }
.section-title {
    color: var(--navy) !important; font-size: 1rem !important; font-weight: 700 !important;
    margin-bottom: 14px !important; padding-bottom: 10px !important;
    border-bottom: 2px solid #EEF1F7 !important;
    display: flex; align-items: center; gap: 7px;
}

/* ── KPI cards ────────────────────────────────────── */
.kpi-card {
    background: var(--card); border-radius: var(--radius);
    padding: 18px 20px; box-shadow: var(--shadow-sm);
    border: 1px solid var(--border); border-top: 3px solid var(--navy);
    transition: all 0.22s ease; height: 100%;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: var(--shadow); }
.kpi-card.accent-red { border-top-color: var(--red); }
.kpi-card.accent-blue { border-top-color: var(--blue-accent); }
.kpi-card.accent-green { border-top-color: var(--success); }
.kpi-label { font-size: 0.68rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.07em; margin-bottom: 6px; }
.kpi-value { font-size: 1.65rem; font-weight: 800; color: var(--navy); line-height: 1; }
.kpi-value.danger  { color: var(--red); }
.kpi-value.warning { color: var(--warning); }
.kpi-value.success { color: var(--success); }
.kpi-icon { font-size: 1.2rem; margin-bottom: 6px; }

/* ── Upload area ──────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 2px dashed var(--border) !important; border-radius: var(--radius) !important;
    background: #F8FAFD !important; cursor: pointer !important; transition: all 0.2s !important;
}
[data-testid="stFileUploader"]:hover { background: #EEF1F7 !important; border-color: var(--navy) !important; }

/* ── Main buttons ─────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%) !important;
    color: #fff !important; border: none !important; border-radius: var(--radius-sm) !important;
    font-weight: 700 !important; font-size: 0.88rem !important; padding: 10px 22px !important;
    box-shadow: 0 2px 8px rgba(27,43,75,0.22) !important; cursor: pointer !important;
    transition: all 0.22s !important; letter-spacing: 0.01em !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 16px rgba(27,43,75,0.30) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ──────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--success) 0%, #2ecc71 100%) !important;
    color: #fff !important; border: none !important; border-radius: var(--radius-sm) !important;
    font-weight: 700 !important; padding: 12px 24px !important; width: 100% !important;
    font-size: 0.95rem !important; box-shadow: 0 2px 8px rgba(39,174,96,0.25) !important;
    cursor: pointer !important; transition: all 0.22s !important;
}
.stDownloadButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 4px 16px rgba(39,174,96,0.35) !important; }

/* ── Tabs ─────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card) !important; border-radius: var(--radius) var(--radius) 0 0 !important;
    border-bottom: 2px solid var(--border) !important; padding: 0 8px !important; gap: 3px !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 7px 7px 0 0 !important; font-weight: 500 !important; color: var(--text-muted) !important;
    transition: all 0.18s !important; padding: 9px 16px !important; font-size: 0.85rem !important;
}
.stTabs [aria-selected="true"] {
    background: #EEF1F7 !important; color: var(--navy) !important; font-weight: 700 !important;
    border-bottom: 2px solid var(--navy) !important;
}

/* ── Data frames ──────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius: var(--radius) !important; overflow: hidden !important; border: 1px solid var(--border) !important; }

/* ── Alerts ───────────────────────────────────────── */
.stAlert { border-radius: var(--radius-sm) !important; }

/* ── Selectboxes ──────────────────────────────────── */
.stSelectbox > div > div { border-radius: var(--radius-sm) !important; border-color: var(--border) !important; cursor: pointer !important; }

/* ── Number inputs ────────────────────────────────── */
.stNumberInput > div > div > input { border-radius: var(--radius-sm) !important; border-color: var(--border) !important; }

/* ── Expanders ────────────────────────────────────── */
.streamlit-expanderHeader { background: var(--bg) !important; border-radius: var(--radius-sm) !important; font-weight: 600 !important; color: var(--navy) !important; cursor: pointer !important; }

/* ── Metrics ──────────────────────────────────────── */
[data-testid="metric-container"] { background: var(--card) !important; border-radius: var(--radius) !important; padding: 16px !important; border: 1px solid var(--border) !important; box-shadow: var(--shadow-sm) !important; }

/* ── Footer ───────────────────────────────────────── */
.app-footer {
    text-align: center; color: var(--text-muted); font-size: 0.75rem;
    padding: 20px 0 10px; border-top: 1px solid var(--border); margin-top: 36px;
    display: flex; align-items: center; justify-content: center; gap: 8px;
}
.app-footer img { width: 22px; height: 22px; object-fit: contain; opacity: 0.6; border-radius: 4px; }


/* ═══════════════════════════════════════════════════
   PREMIUM DARK SIDEBAR + FIXED CUSTOM BUCKET CONTRAST
   Added patch: visible +/- buttons and bucket numbers
═══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #08111F 0%, #111C33 45%, #172554 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.10) !important;
    box-shadow: 8px 0 28px rgba(2,6,23,0.24) !important;
}
[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
}

.sb-logo-wrap {
    border-bottom: 1px solid rgba(255,255,255,0.12) !important;
}
.sb-logo-text .sb-brand { color: #FFFFFF !important; }
.sb-logo-text .sb-sub { color: #94A3B8 !important; }

[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.12) !important;
}

[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stRadio > label,
[data-testid="stSidebar"] .stNumberInput > label,
[data-testid="stSidebar"] .stDateInput > label,
[data-testid="stSidebar"] .stTextInput > label {
    color: #CBD5E1 !important;
}

[data-testid="stSidebar"] .stRadio > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
[data-testid="stSidebar"] .stRadio label,
[data-testid="stSidebar"] .stRadio p {
    color: #E5E7EB !important;
    font-weight: 500 !important;
}

/* Sidebar inputs: white fields, dark readable values */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] [data-baseweb="input"] input,
[data-testid="stSidebar"] [data-baseweb="select"] div {
    color: #0F172A !important;
}
[data-testid="stSidebar"] [data-testid="stDateInput"] input,
[data-testid="stSidebar"] input[type="text"],
[data-testid="stSidebar"] input[type="number"] {
    background: #FFFFFF !important;
    color: #0F172A !important;
    border: 1px solid rgba(148,163,184,0.45) !important;
    border-radius: 9px !important;
}
[data-testid="stSidebar"] input::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

/* Custom bucket area */
.cb-hint {
    background: rgba(255,255,255,0.07) !important;
    border-left: 3px solid #EF4444 !important;
    color: #CBD5E1 !important;
    font-size: 0.70rem !important;
    padding: 6px 8px !important;
    margin-bottom: 8px !important;
}
.cb-card {
    background: rgba(255,255,255,0.055) !important;
    border: 1px solid rgba(148,163,184,0.18) !important;
    border-left: 3px solid #EF4444 !important;
    border-radius: 11px !important;
    padding: 6px 9px !important;
    margin: 8px 0 5px 0 !important;
}
.cb-card-header,
.custom-bucket-index,
.bucket-number {
    color: #FFFFFF !important;
    font-size: 0.86rem !important;
    line-height: 1.05 !important;
    font-weight: 900 !important;
    letter-spacing: 0.02em !important;
    text-shadow: 0 1px 2px rgba(0,0,0,0.35) !important;
}
.cb-card-header::first-letter,
.custom-bucket-index::first-letter,
.bucket-number::first-letter {
    color: #FF5A5F !important;
}

[data-testid="stSidebar"] .cb-inputs [data-testid="stNumberInput"] input,
[data-testid="stSidebar"] .cb-inputs [data-testid="stTextInput"] input {
    height: 30px !important;
    min-height: 30px !important;
    padding: 3px 8px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    color: #0F172A !important;
}
[data-testid="stSidebar"] .cb-inputs .stNumberInput,
[data-testid="stSidebar"] .cb-inputs .stTextInput {
    margin-bottom: 2px !important;
}

/* Streamlit number_input +/- controls — make + and - visible */
[data-testid="stSidebar"] [data-testid="stNumberInput"] button,
[data-testid="stSidebar"] [data-testid="stNumberInput"] button svg,
[data-testid="stSidebar"] [data-testid="stNumberInput"] button p,
[data-testid="stSidebar"] [data-testid="stNumberInput"] button span,
[data-testid="stSidebar"] div[data-baseweb="input"] button,
[data-testid="stSidebar"] div[data-baseweb="input"] button svg,
[data-testid="stSidebar"] div[data-baseweb="input"] button p,
[data-testid="stSidebar"] div[data-baseweb="input"] button span {
    color: #0F172A !important;
    fill: #0F172A !important;
    stroke: #0F172A !important;
    opacity: 1 !important;
    font-weight: 900 !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover,
[data-testid="stSidebar"] div[data-baseweb="input"] button:hover {
    background: #E2E8F0 !important;
    color: #DC2626 !important;
}
[data-testid="stSidebar"] [data-testid="stNumberInput"] button:hover svg,
[data-testid="stSidebar"] div[data-baseweb="input"] button:hover svg {
    fill: #DC2626 !important;
    stroke: #DC2626 !important;
}

.custom-bucket-help {
    color: #CBD5E1 !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    margin: 4px 0 6px 0 !important;
}

[data-testid="stSidebar"] .cb-remove button {
    background: rgba(239,68,68,0.12) !important;
    color: #FECACA !important;
    border: 1px solid rgba(248,113,113,0.35) !important;
    border-radius: 8px !important;
    font-size: 0.70rem !important;
    font-weight: 700 !important;
    min-height: 26px !important;
    height: 26px !important;
    padding: 2px 10px !important;
}
[data-testid="stSidebar"] .cb-remove button:hover {
    background: rgba(239,68,68,0.22) !important;
    color: #FFFFFF !important;
}
[data-testid="stSidebar"] .cb-add button {
    background: rgba(255,255,255,0.07) !important;
    color: #FFFFFF !important;
    border: 1px dashed rgba(255,255,255,0.24) !important;
}
[data-testid="stSidebar"] .cb-add button:hover {
    background: rgba(255,255,255,0.12) !important;
    border-color: #EF4444 !important;
}

/* Keep default bucket badges readable on dark sidebar */
.bucket-badge-container {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}
.bucket-badge {
    background: rgba(255,255,255,0.10) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #FFFFFF !important;
}

</style>
"""


def inject_css():
    import streamlit as st
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def get_logo_img_tag(width: int = 44) -> str:
    b64 = _get_logo_b64()
    if not b64:
        return ""
    return f'<img src="data:image/png;base64,{b64}" width="{width}" style="object-fit:contain;border-radius:8px;">'


def sidebar_logo_html(t: dict) -> str:
    b64 = _get_logo_b64()
    img = f'<img src="data:image/png;base64,{b64}" style="width:44px;height:44px;object-fit:contain;border-radius:8px;">' if b64 else "📦"
    return f"""
    <div class="sb-logo-wrap">
        <div class="sb-logo-img">{img}</div>
        <div class="sb-logo-text">
            <div class="sb-brand">FA Fin Apps</div>
            <div class="sb-sub">Inventory Aging</div>
        </div>
    </div>"""


def app_header_html(t: dict) -> str:
    logo_tag = get_logo_img_tag(64)
    return f"""
    <div class="app-header">
        <div class="app-header-logo">{logo_tag}</div>
        <div class="app-header-text">
            <h1>{t['app_title']}</h1>
            <div class="app-header-red-bar"></div>
            <p>{t['app_subtitle']}</p>
        </div>
    </div>"""


def hero_section_html(t: dict) -> str:
    feats = [t.get(k, "") for k in ["feat_fast","feat_buckets","feat_report","feat_excel","feat_batch"]]
    pills = "".join(f'<span class="feat-pill"><span class="feat-dot"></span>{f}</span>' for f in feats if f)
    return f"""
    <div class="hero-section">
        <div class="feat-grid">{pills}</div>
    </div>"""


def section_header(title: str) -> str:
    return f'<div class="section-title">{title}</div>'


# backward-compat alias
def app_header(title: str, subtitle: str) -> str:
    return f"""
    <div class="app-header">
        <div class="app-header-text">
            <h1>{title}</h1><div class="app-header-red-bar"></div>
            <p>{subtitle}</p>
        </div>
    </div>"""


def footer_html(t: dict) -> str:
    b64 = _get_logo_b64()
    img = f'<img src="data:image/png;base64,{b64}">' if b64 else ""
    return f'<div class="app-footer">{img}<span>{t.get("powered_by","Powered by FA Fin Apps")}</span></div>'


def kpi_card(label: str, value: str, icon: str = "📊", css_class: str = "", accent: str = "") -> str:
    return f"""
    <div class="kpi-card {accent}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value {css_class}">{value}</div>
    </div>"""


def default_buckets_html(buckets: list) -> str:
    badges = "".join(f'<span class="bucket-badge">{b["name"]}</span>' for b in buckets)
    return f'<div class="bucket-badge-container">{badges}</div>'
