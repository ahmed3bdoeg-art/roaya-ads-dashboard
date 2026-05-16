import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Roaya Ads Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap');

:root {
    --primary: #1A56DB;
    --primary-light: #EBF2FF;
    --primary-dark: #1240A8;
    --accent: #0EA5E9;
    --success: #059669;
    --success-light: #ECFDF5;
    --warning: #D97706;
    --warning-light: #FFFBEB;
    --danger: #DC2626;
    --danger-light: #FEF2F2;
    --neutral: #6B7280;
    --surface: #FFFFFF;
    --background: #F8FAFC;
    --border: #E5E7EB;
    --text-primary: #111827;
    --text-secondary: #6B7280;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
    --shadow-md: 0 4px 16px rgba(0,0,0,0.08), 0 2px 8px rgba(0,0,0,0.06);
    --shadow-lg: 0 20px 40px rgba(0,0,0,0.08);
    --radius: 14px;
    --radius-sm: 8px;
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
    background-color: var(--background);
    color: var(--text-primary);
}

/* Hide Streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
.block-container { padding: 0 2rem 2rem 2rem; max-width: 1600px; }

/* ── Hero Section ── */
.hero {
    background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 50%, #1A56DB 100%);
    border-radius: 0 0 var(--radius) var(--radius);
    padding: 2.5rem 3rem;
    margin: 0 -2rem 2.5rem -2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -10%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    left: 20%;
    width: 300px;
    height: 300px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 12px;
    font-weight: 600;
    color: rgba(255,255,255,0.9);
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #FFFFFF;
    line-height: 1.2;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.03em;
}
.hero-subtitle {
    font-size: 1rem;
    color: rgba(255,255,255,0.65);
    font-weight: 400;
    margin: 0;
}
.hero-stats {
    display: flex;
    gap: 2rem;
    margin-top: 2rem;
}
.hero-stat { color: rgba(255,255,255,0.8); }
.hero-stat-value { font-size: 1.5rem; font-weight: 700; color: #fff; }
.hero-stat-label { font-size: 0.75rem; color: rgba(255,255,255,0.5); text-transform: uppercase; letter-spacing: 0.05em; }

/* ── KPI Cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 1rem;
    margin-bottom: 2rem;
}
.kpi-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    position: relative;
    overflow: hidden;
    transition: box-shadow 0.2s, transform 0.2s;
}
.kpi-card:hover { box-shadow: var(--shadow-md); transform: translateY(-2px); }
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--primary), var(--accent));
    border-radius: var(--radius) var(--radius) 0 0;
}
.kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.07em;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-size: 1.65rem;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.03em;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.kpi-delta {
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--success);
    display: flex;
    align-items: center;
    gap: 4px;
}
.kpi-delta.neg { color: var(--danger); }
.kpi-icon {
    font-size: 1.4rem;
    margin-bottom: 0.75rem;
    display: block;
}

/* ── Section Headers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.25rem;
}
.section-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    letter-spacing: -0.02em;
    margin: 0;
}
.section-badge {
    background: var(--primary-light);
    color: var(--primary);
    font-size: 0.7rem;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* ── Cards ── */
.card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    margin-bottom: 1.25rem;
}

/* ── Recommendation Cards ── */
.rec-card {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
    box-shadow: var(--shadow-sm);
    border-left: 4px solid var(--primary);
    display: flex;
    align-items: flex-start;
    gap: 1rem;
}
.rec-card.critical { border-left-color: var(--danger); }
.rec-card.high { border-left-color: var(--warning); }
.rec-card.medium { border-left-color: var(--primary); }
.rec-card.low { border-left-color: var(--success); }
.rec-priority {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    padding: 3px 10px;
    border-radius: 999px;
    white-space: nowrap;
    margin-top: 2px;
}
.rec-priority.critical { background: var(--danger-light); color: var(--danger); }
.rec-priority.high { background: var(--warning-light); color: var(--warning); }
.rec-priority.medium { background: var(--primary-light); color: var(--primary); }
.rec-priority.low { background: var(--success-light); color: var(--success); }
.rec-content { flex: 1; }
.rec-title { font-weight: 700; font-size: 0.95rem; color: var(--text-primary); margin-bottom: 0.3rem; }
.rec-explanation { font-size: 0.82rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 0.5rem; }
.rec-action { font-size: 0.78rem; font-weight: 600; color: var(--primary); }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface);
    border-radius: var(--radius);
    padding: 6px;
    box-shadow: var(--shadow-sm);
    border: 1px solid var(--border);
    gap: 4px;
    margin-bottom: 1.5rem;
    flex-wrap: wrap;
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    color: var(--text-secondary) !important;
    padding: 8px 14px !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.15s !important;
}
.stTabs [aria-selected="true"] {
    background: var(--primary) !important;
    color: #fff !important;
    box-shadow: 0 2px 8px rgba(26,86,219,0.35) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%) !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #fff !important;
}
.sidebar-logo {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 1rem 0 1.5rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 1.5rem;
}
.sidebar-logo-icon {
    width: 38px; height: 38px;
    background: linear-gradient(135deg, var(--primary), var(--accent));
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
}
.sidebar-logo-text { font-weight: 800; font-size: 1rem; letter-spacing: -0.02em; }
.sidebar-logo-sub { font-size: 0.7rem; opacity: 0.5; }
.sidebar-section-label {
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    opacity: 0.4;
    margin-bottom: 0.75rem;
    margin-top: 1.5rem;
}
.upload-zone {
    background: rgba(255,255,255,0.04);
    border: 1px dashed rgba(255,255,255,0.15);
    border-radius: var(--radius);
    padding: 1.25rem;
    text-align: center;
    margin-bottom: 1rem;
}

/* ── Data Tables ── */
.stDataFrame { border-radius: var(--radius); overflow: hidden; }
.stDataFrame th {
    background: var(--primary) !important;
    color: #fff !important;
    font-weight: 600 !important;
}

/* ── Metrics override ── */
[data-testid="metric-container"] {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.25rem;
    box-shadow: var(--shadow-sm);
}

/* ── Status pills ── */
.status-pill {
    display: inline-flex; align-items: center; gap: 5px;
    padding: 3px 10px; border-radius: 999px;
    font-size: 0.72rem; font-weight: 600;
}
.status-active { background: var(--success-light); color: var(--success); }
.status-paused { background: var(--warning-light); color: var(--warning); }
.status-stopped { background: #FEE2E2; color: var(--danger); }

/* ── Score gauge ── */
.score-ring {
    width: 100px; height: 100px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem; font-weight: 800;
    color: var(--primary);
    background: conic-gradient(var(--primary) var(--pct), var(--border) 0);
    position: relative;
}
.score-ring::before {
    content: ''; position: absolute;
    width: 76px; height: 76px;
    background: var(--surface);
    border-radius: 50%;
}
.score-value { position: relative; z-index: 1; }

/* ── File log ── */
.file-log-item {
    display: flex; align-items: center; gap: 12px;
    background: var(--background);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    margin-bottom: 8px;
}
.file-log-icon { font-size: 1.4rem; }
.file-log-name { font-weight: 600; font-size: 0.9rem; }
.file-log-meta { font-size: 0.75rem; color: var(--text-secondary); }

/* ── Divider ── */
.divider { border: none; border-top: 1px solid var(--border); margin: 1.5rem 0; }

/* ── Health score ── */
.health-bar-wrap { background: var(--border); border-radius: 999px; height: 8px; margin-top: 8px; }
.health-bar { height: 8px; border-radius: 999px; background: linear-gradient(90deg, var(--primary), var(--accent)); }

/* ── Empty state ── */
.empty-state {
    text-align: center; padding: 4rem 2rem;
    background: var(--surface); border-radius: var(--radius);
    border: 1px dashed var(--border);
}
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-title { font-size: 1.3rem; font-weight: 700; color: var(--text-primary); margin-bottom: 0.5rem; }
.empty-desc { color: var(--text-secondary); font-size: 0.9rem; max-width: 400px; margin: 0 auto 1.5rem; }

/* Streamlit button override */
.stButton button {
    background: linear-gradient(135deg, var(--primary), var(--primary-dark));
    color: white;
    border: none;
    border-radius: var(--radius-sm);
    font-weight: 600;
    font-family: 'Plus Jakarta Sans', sans-serif;
    transition: all 0.2s;
}
.stButton button:hover {
    box-shadow: 0 4px 12px rgba(26,86,219,0.4);
    transform: translateY(-1px);
}

/* Selectbox, multiselect */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    border-radius: var(--radius-sm) !important;
    border-color: var(--border) !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 999px; }
::-webkit-scrollbar-thumb:hover { background: var(--neutral); }
</style>
""", unsafe_allow_html=True)

# ─── CONSTANTS ─────────────────────────────────────────────────────────────────
META_COLUMNS = {
    'campaign name': 'Campaign',
    'ad set name': 'Ad Set / Group',
    'ad name': 'Ad',
    'results': 'Results',
    'result indicator': 'Result Type',
    'cost per results': 'Cost / Result',
    'amount spent (egp)': 'Spend',
    'amount spent (usd)': 'Spend',
    'amount spent': 'Spend',
    'impressions': 'Impressions',
    'reach': 'Reach',
    'frequency': 'Frequency',
    'link clicks': 'Clicks',
    'ctr (link click-through rate)': 'CTR',
    'ctr': 'CTR',
    'cpc (cost per link click)': 'CPC',
    'cpc': 'CPC',
    'cpm (cost per 1,000 impressions)': 'CPM',
    'cpm': 'CPM',
    'landing page views': 'Landing Page Views',
    'purchases': 'Purchases',
    'purchase roas': 'ROAS',
    'reporting starts': 'Date',
    'reporting ends': 'Date End',
    'delivery': 'Delivery',
    'budget': 'Budget',
}
TIKTOK_COLUMNS = {
    'campaign name': 'Campaign',
    'ad group name': 'Ad Set / Group',
    'ad name': 'Ad',
    'primary status': 'Delivery',
    'cost': 'Spend',
    'impressions': 'Impressions',
    'reach': 'Reach',
    'frequency': 'Frequency',
    'clicks (destination)': 'Clicks',
    'ctr (destination)': 'CTR',
    'cpc (destination)': 'CPC',
    'cpm': 'CPM',
    'conversions': 'Results',
    'cost per conversion': 'Cost / Result',
    'conversion rate (cvr)': 'Conversion Rate',
    'results': 'Results',
    'cost per result': 'Cost / Result',
    'result type': 'Result Type',
    'form submissions': 'Form Submissions',
    '6-second focused views': '6s Views',
    '15-second focused views': '15s Views',
    'budget': 'Budget',
    'date': 'Date',
}

CHART_COLORS = ['#1A56DB', '#0EA5E9', '#6366F1', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#EC4899']
PLOTLY_LAYOUT = dict(
    font_family='Plus Jakarta Sans',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=30, b=30, l=10, r=10),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    xaxis=dict(showgrid=True, gridcolor='#F3F4F6', zeroline=False),
    yaxis=dict(showgrid=True, gridcolor='#F3F4F6', zeroline=False),
)

# ─── DEMO DATA GENERATOR ───────────────────────────────────────────────────────
def generate_demo_data():
    np.random.seed(42)
    rng = np.random
    n_days = 30
    dates = [datetime.today() - timedelta(days=i) for i in range(n_days - 1, -1, -1)]

    meta_campaigns = ['Ramadan Sale – Awareness', 'App Install – Egypt', 'Retargeting – Cart Abandon', 'Lead Gen – B2B']
    meta_adsets = ['Lookalike 2% Egypt', 'Interest: Shopping', 'Website Visitors 30d', 'Job Title Targeting']
    meta_ads = ['Video Ad v1', 'Carousel – Products', 'Static Image A', 'UGC Testimonial']

    tt_campaigns = ['TikTok Brand Wave', 'TikTok Conversions', 'TikTok TopView']
    tt_adgroups = ['18-24 Female Egypt', '25-34 Male MENA', 'Interest: Fashion']
    tt_ads = ['Creator Video A', 'Product Demo Clip', 'Hook Challenge']

    rows = []
    for camp in meta_campaigns:
        for adset in meta_adsets[:2]:
            for ad in meta_ads[:2]:
                for d in dates:
                    spend = rng.uniform(80, 600)
                    impr = int(spend * rng.uniform(200, 700))
                    reach = int(impr * rng.uniform(0.6, 0.9))
                    clicks = int(impr * rng.uniform(0.008, 0.04))
                    results = int(clicks * rng.uniform(0.03, 0.15))
                    views6 = int(impr * rng.uniform(0.15, 0.45))
                    views15 = int(views6 * rng.uniform(0.3, 0.7))
                    rows.append({
                        'Platform': 'Meta Ads', 'Report Level': 'Ad Level',
                        'Campaign': camp, 'Ad Set / Group': adset, 'Ad': ad,
                        'Date': d.strftime('%Y-%m-%d'), 'Delivery': rng.choice(['Active', 'Active', 'Paused']),
                        'Spend': round(spend, 2),
                        'Results': results, 'Impressions': impr, 'Reach': reach,
                        'Frequency': round(impr / reach, 2) if reach else 0,
                        'Clicks': clicks,
                        'CTR': round(clicks / impr * 100, 2) if impr else 0,
                        'CPC': round(spend / clicks, 2) if clicks else 0,
                        'CPM': round(spend / impr * 1000, 2) if impr else 0,
                        'Cost / Result': round(spend / results, 2) if results else 0,
                        'Purchases': int(results * rng.uniform(0.1, 0.3)),
                        'ROAS': round(rng.uniform(1.2, 5.5), 2),
                        'Landing Page Views': int(clicks * rng.uniform(0.5, 0.85)),
                        'Conversion Rate': round(results / clicks * 100, 2) if clicks else 0,
                        '6s Views': views6, '15s Views': views15,
                        'Hook Rate': round(views6 / impr * 100, 2) if impr else 0,
                        'Hold Rate': round(views15 / views6 * 100, 2) if views6 else 0,
                        'Result Type': 'Leads', 'Budget': round(rng.uniform(500, 2000), 0),
                        'Efficiency Score': 0, 'Source File': 'demo_meta.csv',
                    })
    for camp in tt_campaigns:
        for ag in tt_adgroups[:2]:
            for ad in tt_ads[:2]:
                for d in dates:
                    spend = rng.uniform(60, 400)
                    impr = int(spend * rng.uniform(300, 900))
                    reach = int(impr * rng.uniform(0.55, 0.85))
                    clicks = int(impr * rng.uniform(0.01, 0.05))
                    results = int(clicks * rng.uniform(0.04, 0.18))
                    views6 = int(impr * rng.uniform(0.2, 0.55))
                    views15 = int(views6 * rng.uniform(0.25, 0.65))
                    rows.append({
                        'Platform': 'TikTok Ads', 'Report Level': 'Ad Level',
                        'Campaign': camp, 'Ad Set / Group': ag, 'Ad': ad,
                        'Date': d.strftime('%Y-%m-%d'), 'Delivery': rng.choice(['Active', 'Active', 'Paused']),
                        'Spend': round(spend, 2),
                        'Results': results, 'Impressions': impr, 'Reach': reach,
                        'Frequency': round(impr / reach, 2) if reach else 0,
                        'Clicks': clicks,
                        'CTR': round(clicks / impr * 100, 2) if impr else 0,
                        'CPC': round(spend / clicks, 2) if clicks else 0,
                        'CPM': round(spend / impr * 1000, 2) if impr else 0,
                        'Cost / Result': round(spend / results, 2) if results else 0,
                        'Purchases': 0, 'ROAS': 0,
                        'Landing Page Views': int(clicks * rng.uniform(0.4, 0.8)),
                        'Conversion Rate': round(results / clicks * 100, 2) if clicks else 0,
                        '6s Views': views6, '15s Views': views15,
                        'Hook Rate': round(views6 / impr * 100, 2) if impr else 0,
                        'Hold Rate': round(views15 / views6 * 100, 2) if views6 else 0,
                        'Result Type': 'Conversions', 'Budget': round(rng.uniform(300, 1500), 0),
                        'Efficiency Score': 0, 'Source File': 'demo_tiktok.csv',
                    })

    df = pd.DataFrame(rows)
    df = compute_efficiency_score(df)
    return df

# ─── FILE PROCESSING ───────────────────────────────────────────────────────────
def detect_platform(df: pd.DataFrame) -> str:
    cols = [c.lower() for c in df.columns]
    if any('tiktok' in c for c in cols): return 'TikTok Ads'
    if 'ad group name' in cols: return 'TikTok Ads'
    if '6-second focused views' in cols or '15-second focused views' in cols: return 'TikTok Ads'
    if 'cost per conversion' in cols or 'conversion rate (cvr)' in cols: return 'TikTok Ads'
    if 'amount spent (egp)' in cols or 'amount spent (usd)' in cols: return 'Meta Ads'
    if 'purchase roas' in cols: return 'Meta Ads'
    if 'ad set name' in cols: return 'Meta Ads'
    return 'Meta Ads'

def detect_report_level(df: pd.DataFrame) -> str:
    cols = [c.lower() for c in df.columns]
    if 'ad name' in cols: return 'Ad Level'
    if 'ad set name' in cols or 'ad group name' in cols: return 'Ad Set / Group Level'
    if 'campaign name' in cols: return 'Campaign Level'
    if 'date' in cols: return 'Daily Breakdown'
    return 'Account Level'

def normalize_columns(df: pd.DataFrame, platform: str) -> pd.DataFrame:
    mapping = META_COLUMNS if platform == 'Meta Ads' else TIKTOK_COLUMNS
    df.columns = [c.strip() for c in df.columns]
    rename_map = {}
    for col in df.columns:
        cl = col.lower()
        if cl in mapping:
            target = mapping[cl]
            if target not in rename_map.values():
                rename_map[col] = target
    df = df.rename(columns=rename_map)
    return df

def remove_summary_rows(df: pd.DataFrame) -> tuple:
    mask = df.apply(lambda row: any(
        str(v).strip().lower().startswith('total of') for v in row
    ), axis=1)
    return df[~mask].copy(), int(mask.sum())

def ensure_numeric(df: pd.DataFrame, cols: list) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace('%', ''), errors='coerce').fillna(0)
    return df

def recalculate_kpis(df: pd.DataFrame) -> pd.DataFrame:
    num_cols = ['Spend', 'Results', 'Impressions', 'Reach', 'Clicks', 'CTR',
                'CPC', 'CPM', 'Frequency', 'Conversion Rate', 'Purchases',
                'ROAS', '6s Views', '15s Views', 'Hook Rate', 'Hold Rate',
                'Landing Page Views', 'Cost / Result', 'Budget']
    df = ensure_numeric(df, num_cols)
    df['CTR'] = np.where(df['Impressions'] > 0, df['Clicks'] / df['Impressions'] * 100, df['CTR'])
    df['CPC'] = np.where(df['Clicks'] > 0, df['Spend'] / df['Clicks'], df['CPC'])
    df['CPM'] = np.where(df['Impressions'] > 0, df['Spend'] / df['Impressions'] * 1000, df['CPM'])
    df['Frequency'] = np.where(df['Reach'] > 0, df['Impressions'] / df['Reach'], df['Frequency'])
    df['Conversion Rate'] = np.where(df['Clicks'] > 0, df['Results'] / df['Clicks'] * 100, df['Conversion Rate'])
    df['Cost / Result'] = np.where(df['Results'] > 0, df['Spend'] / df['Results'], df['Cost / Result'])
    df['Hook Rate'] = np.where(df['Impressions'] > 0, df['6s Views'] / df['Impressions'] * 100, df['Hook Rate'])
    df['Hold Rate'] = np.where(df['6s Views'] > 0, df['15s Views'] / df['6s Views'] * 100, df['Hold Rate'])
    return df

def compute_efficiency_score(df: pd.DataFrame) -> pd.DataFrame:
    def score_row(row):
        s = 0
        ctr = row.get('CTR', 0) or 0
        cvr = row.get('Conversion Rate', 0) or 0
        freq = row.get('Frequency', 0) or 0
        results = row.get('Results', 0) or 0
        cpr = row.get('Cost / Result', 0) or 0
        spend = row.get('Spend', 0) or 0
        if ctr >= 3: s += 25
        elif ctr >= 1.5: s += 15
        elif ctr >= 0.5: s += 8
        if cvr >= 10: s += 25
        elif cvr >= 4: s += 15
        elif cvr >= 1: s += 8
        if freq <= 2: s += 20
        elif freq <= 3.5: s += 12
        elif freq <= 5: s += 6
        if results > 0: s += 20
        elif spend > 0: s -= 10
        if cpr > 0 and spend > 0:
            ratio = cpr / spend
            if ratio < 0.05: s += 10
            elif ratio < 0.2: s += 5
        return max(0, min(100, s))

    df['Efficiency Score'] = df.apply(score_row, axis=1)
    return df

def process_file(uploaded_file) -> dict:
    name = uploaded_file.name
    ext = name.rsplit('.', 1)[-1].lower()
    try:
        if ext == 'csv':
            df = pd.read_csv(uploaded_file, encoding='utf-8-sig')
        else:
            df = pd.read_excel(uploaded_file)
    except Exception as e:
        return {'error': str(e), 'name': name}

    original_rows = len(df)
    platform = detect_platform(df)
    level = detect_report_level(df)
    df, removed = remove_summary_rows(df)
    df = normalize_columns(df, platform)

    # Add missing standard columns
    for col in ['Platform', 'Report Level', 'Result Type', 'Campaign', 'Ad Set / Group',
                'Ad', 'Date', 'Delivery', 'Spend', 'Results', 'Cost / Result', 'Impressions',
                'Reach', 'Frequency', 'Clicks', 'CTR', 'CPC', 'CPM', 'Landing Page Views',
                'Conversion Rate', 'Purchases', 'ROAS', '6s Views', '15s Views',
                'Hook Rate', 'Hold Rate', 'Budget', 'Efficiency Score']:
        if col not in df.columns:
            df[col] = np.nan

    df['Platform'] = platform
    df['Report Level'] = level
    df['Source File'] = name
    df = recalculate_kpis(df)
    df = compute_efficiency_score(df)

    return {
        'name': name, 'platform': platform, 'level': level,
        'original_rows': original_rows, 'processed_rows': len(df),
        'summary_removed': removed, 'df': df, 'error': None,
        'columns_mapped': list(df.columns),
    }

def combine_files(results: list) -> pd.DataFrame:
    dfs = [r['df'] for r in results if r.get('df') is not None]
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, ignore_index=True)

# ─── CHART HELPERS ─────────────────────────────────────────────────────────────
def fig_layout(fig, height=380):
    fig.update_layout(**PLOTLY_LAYOUT, height=height)
    return fig

def bar_chart(df, x, y, title='', color=None, orientation='v'):
    kwargs = dict(data_frame=df, x=x, y=y, title=title, color_discrete_sequence=CHART_COLORS)
    if color: kwargs['color'] = color
    if orientation == 'h':
        kwargs['x'], kwargs['y'] = y, x
        kwargs['orientation'] = 'h'
    fig = px.bar(**kwargs)
    fig.update_traces(marker_line_width=0)
    return fig_layout(fig)

def line_chart(df, x, y_cols, title=''):
    fig = go.Figure()
    for i, y in enumerate(y_cols):
        if y in df.columns:
            fig.add_trace(go.Scatter(
                x=df[x], y=df[y], name=y, mode='lines+markers',
                line=dict(color=CHART_COLORS[i % len(CHART_COLORS)], width=2.5),
                marker=dict(size=4),
            ))
    fig.update_layout(**PLOTLY_LAYOUT, height=340, title=title)
    return fig

def scatter_chart(df, x, y, size=None, color=None, title='', hover=''):
    kwargs = dict(data_frame=df, x=x, y=y, title=title, color_discrete_sequence=CHART_COLORS)
    if size and size in df.columns: kwargs['size'] = size
    if color and color in df.columns: kwargs['color'] = color
    if hover and hover in df.columns: kwargs['hover_name'] = hover
    fig = px.scatter(**kwargs)
    return fig_layout(fig)

def donut_chart(df, names, values, title=''):
    fig = px.pie(df, names=names, values=values, hole=0.6, title=title,
                 color_discrete_sequence=CHART_COLORS)
    fig.update_traces(textinfo='percent+label', textfont_size=11)
    return fig_layout(fig, 320)

# ─── FORMATTING ────────────────────────────────────────────────────────────────
def fmt_num(n, prefix='', suffix='', dec=0):
    if pd.isna(n) or n == 0:
        return '—'
    if n >= 1_000_000:
        return f"{prefix}{n/1_000_000:.1f}M{suffix}"
    if n >= 1_000:
        return f"{prefix}{n/1_000:.1f}K{suffix}"
    return f"{prefix}{n:,.{dec}f}{suffix}"

def fmt_spend(n): return fmt_num(n, prefix='EGP ', dec=0)
def fmt_pct(n): return f"{n:.1f}%" if not pd.isna(n) and n != 0 else '—'
def fmt_cpr(n): return fmt_num(n, prefix='EGP ', dec=2)

# ─── KPI CARD HTML ─────────────────────────────────────────────────────────────
def kpi_card(icon, label, value, delta=None, delta_neg=False):
    delta_html = ''
    if delta:
        cls = 'neg' if delta_neg else ''
        arrow = '↓' if delta_neg else '↑'
        delta_html = f'<div class="kpi-delta {cls}">{arrow} {delta}</div>'
    return f"""
    <div class="kpi-card">
        <span class="kpi-icon">{icon}</span>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

def kpi_grid(cards_html):
    inner = ''.join(cards_html)
    return f'<div class="kpi-grid">{inner}</div>'

# ─── RECOMMENDATIONS ENGINE ────────────────────────────────────────────────────
def generate_recommendations(df: pd.DataFrame) -> list:
    recs = []
    if df.empty: return recs

    camp_grp = df.groupby('Campaign').agg(
        Spend=('Spend', 'sum'), Results=('Results', 'sum'),
        CTR=('CTR', 'mean'), Frequency=('Frequency', 'mean'),
        CPR=('Cost / Result', 'mean')
    ).reset_index()

    median_cpr = camp_grp[camp_grp['CPR'] > 0]['CPR'].median() if not camp_grp.empty else 0

    for _, row in camp_grp.iterrows():
        name = row['Campaign']
        spend = row['Spend']
        results = row['Results']
        ctr = row['CTR']
        freq = row['Frequency']
        cpr = row['CPR']

        if spend > 500 and results == 0:
            recs.append(dict(priority='critical', icon='🚨', title=f'Pause: {name}',
                explanation=f'Spent {fmt_spend(spend)} with zero results. Budget is being wasted.',
                action='⏸ Pause this campaign immediately and investigate targeting & creatives.'))

        if results > 0 and cpr > 0 and median_cpr > 0 and cpr < median_cpr * 0.7:
            recs.append(dict(priority='high', icon='📈', title=f'Scale Winner: {name}',
                explanation=f'CPR of {fmt_cpr(cpr)} is well below the median ({fmt_cpr(median_cpr)}). Strong performance.',
                action='🚀 Increase daily budget by 20–30%. Duplicate to new audiences.'))

        if results > 0 and cpr > 0 and median_cpr > 0 and cpr > median_cpr * 1.5:
            recs.append(dict(priority='high', icon='⚙️', title=f'Optimize: {name}',
                explanation=f'CPR of {fmt_cpr(cpr)} is significantly above median. Inefficient spend.',
                action='🔧 Review targeting, creatives, and landing page. Test lower bids.'))

        if ctr < 0.8 and spend > 200:
            recs.append(dict(priority='medium', icon='🎨', title=f'Refresh Creatives: {name}',
                explanation=f'CTR of {fmt_pct(ctr)} indicates the ad is not capturing attention.',
                action='🎯 Test new ad formats, headlines, or visuals. A/B test 3 variants.'))

        if freq > 4.5 and ctr < 1.5:
            recs.append(dict(priority='medium', icon='😴', title=f'Ad Fatigue: {name}',
                explanation=f'Frequency {freq:.1f}x with low CTR. Audience has seen this ad too many times.',
                action='🔄 Rotate fresh creatives. Expand targeting to reduce frequency.'))

    if 'Ad' in df.columns:
        ad_grp = df.groupby('Ad').agg(
            Spend=('Spend', 'sum'), Results=('Results', 'sum'),
            CTR=('CTR', 'mean')
        ).reset_index()
        winners = ad_grp[(ad_grp['Results'] > 0)].nlargest(3, 'Results')
        for _, row in winners.iterrows():
            recs.append(dict(priority='low', icon='🏆', title=f'Duplicate Winning Ad: {row["Ad"]}',
                explanation=f'{int(row["Results"])} results with CTR {fmt_pct(row["CTR"])}. Top performer.',
                action='📋 Duplicate to other ad sets. Use as benchmark for future creatives.'))

    return recs[:20]

# ─── EXPORT ────────────────────────────────────────────────────────────────────
def build_excel_export(df: pd.DataFrame, file_log: list, recs: list) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Clean Data', index=False)
        if 'Platform' in df.columns:
            plat_sum = df.groupby('Platform').agg(
                Spend=('Spend', 'sum'), Results=('Results', 'sum'),
                Impressions=('Impressions', 'sum'), Clicks=('Clicks', 'sum')
            ).reset_index()
            plat_sum.to_excel(writer, sheet_name='Platform Summary', index=False)
        if 'Campaign' in df.columns:
            camp_sum = df.groupby(['Platform', 'Campaign']).agg(
                Spend=('Spend', 'sum'), Results=('Results', 'sum'),
                CTR=('CTR', 'mean'), CPM=('CPM', 'mean'),
            ).reset_index()
            camp_sum.to_excel(writer, sheet_name='Campaign Summary', index=False)
        if 'Ad Set / Group' in df.columns:
            as_sum = df.groupby(['Platform', 'Campaign', 'Ad Set / Group']).agg(
                Spend=('Spend', 'sum'), Results=('Results', 'sum'),
            ).reset_index()
            as_sum.to_excel(writer, sheet_name='Ad Set Summary', index=False)
        if 'Ad' in df.columns:
            ad_sum = df.groupby(['Platform', 'Campaign', 'Ad']).agg(
                Spend=('Spend', 'sum'), Results=('Results', 'sum'),
                CTR=('CTR', 'mean'),
            ).reset_index()
            ad_sum.to_excel(writer, sheet_name='Ad Summary', index=False)
        if recs:
            rec_df = pd.DataFrame(recs)
            rec_df.to_excel(writer, sheet_name='Recommended Actions', index=False)
        if file_log:
            log_df = pd.DataFrame(file_log)
            log_df.to_excel(writer, sheet_name='Files Log', index=False)
    return output.getvalue()

# ─── UI COMPONENTS ─────────────────────────────────────────────────────────────
def render_hero(df: pd.DataFrame, is_demo: bool):
    total_spend = df['Spend'].sum()
    total_results = df['Results'].sum()
    platforms = df['Platform'].nunique() if 'Platform' in df.columns else 0
    campaigns = df['Campaign'].nunique() if 'Campaign' in df.columns else 0

    demo_badge = ' · Demo Data' if is_demo else ''
    st.markdown(f"""
    <div class="hero">
        <div class="hero-badge">🎯 AI Ads Intelligence{demo_badge}</div>
        <h1 class="hero-title">ROAYA Ads Intelligence</h1>
        <p class="hero-subtitle">Premium advertising analytics · Multi-platform · Real-time insights</p>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-value">{fmt_spend(total_spend)}</div>
                <div class="hero-stat-label">Total Spend</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">{fmt_num(total_results)}</div>
                <div class="hero-stat-label">Total Results</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">{platforms}</div>
                <div class="hero-stat-label">Platforms</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">{campaigns}</div>
                <div class="hero-stat-label">Campaigns</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_overview(df: pd.DataFrame):
    total_spend = df['Spend'].sum()
    total_results = df['Results'].sum()
    total_impressions = df['Impressions'].sum()
    total_reach = df['Reach'].sum()
    total_clicks = df['Clicks'].sum()
    avg_ctr = df['CTR'].mean()
    avg_cpc = df['CPC'].replace(0, np.nan).mean()
    avg_cpm = df['CPM'].replace(0, np.nan).mean()
    avg_cpr = (total_spend / total_results) if total_results > 0 else 0
    avg_cvr = df['Conversion Rate'].replace(0, np.nan).mean()
    avg_score = df['Efficiency Score'].mean()

    cards = [
        kpi_card('💰', 'Total Spend', fmt_spend(total_spend)),
        kpi_card('🎯', 'Total Results', fmt_num(total_results)),
        kpi_card('💵', 'Cost / Result', fmt_cpr(avg_cpr)),
        kpi_card('👁️', 'Impressions', fmt_num(total_impressions)),
        kpi_card('👥', 'Reach', fmt_num(total_reach)),
        kpi_card('🖱️', 'Clicks', fmt_num(total_clicks)),
        kpi_card('📊', 'CTR', fmt_pct(avg_ctr)),
        kpi_card('💲', 'CPC', fmt_cpr(avg_cpc)),
        kpi_card('📡', 'CPM', fmt_cpr(avg_cpm)),
        kpi_card('🔄', 'Conv. Rate', fmt_pct(avg_cvr)),
    ]
    st.markdown(kpi_grid(cards), unsafe_allow_html=True)

    # Health Score
    score_pct = int(avg_score)
    score_color = '#059669' if score_pct >= 70 else '#D97706' if score_pct >= 40 else '#DC2626'
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        st.markdown(f"""
        <div class="card" style="text-align:center">
            <div class="kpi-label" style="margin-bottom:1rem">Performance Health Score</div>
            <div style="font-size:3.5rem;font-weight:800;color:{score_color};letter-spacing:-0.05em">{score_pct}</div>
            <div style="color:var(--text-secondary);font-size:0.8rem;margin-bottom:0.75rem">out of 100</div>
            <div class="health-bar-wrap"><div class="health-bar" style="width:{score_pct}%;background:{score_color}"></div></div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        if 'Platform' in df.columns:
            plat = df.groupby('Platform')['Spend'].sum().reset_index()
            fig = donut_chart(plat, 'Platform', 'Spend', 'Spend by Platform')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with c3:
        if 'Platform' in df.columns:
            plat_r = df.groupby('Platform')['Results'].sum().reset_index()
            fig2 = donut_chart(plat_r, 'Platform', 'Results', 'Results Share')
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    # Top Campaigns
    if 'Campaign' in df.columns:
        st.markdown('<div class="section-header"><span class="section-title">Top Campaigns</span><span class="section-badge">by Spend</span></div>', unsafe_allow_html=True)
        camp = df.groupby(['Platform', 'Campaign']).agg(
            Spend=('Spend', 'sum'), Results=('Results', 'sum'),
            CTR=('CTR', 'mean'), CPR=('Cost / Result', 'mean')
        ).reset_index().nlargest(10, 'Spend')
        camp['Spend'] = camp['Spend'].map(lambda x: f"EGP {x:,.0f}")
        camp['CTR'] = camp['CTR'].map(lambda x: f"{x:.2f}%")
        camp['CPR'] = camp['CPR'].map(lambda x: f"EGP {x:,.2f}" if x > 0 else '—')
        st.dataframe(camp, use_container_width=True, hide_index=True)

def render_platform_comparison(df: pd.DataFrame):
    if 'Platform' not in df.columns or df['Platform'].nunique() < 1:
        st.info("No platform data available.")
        return

    plat = df.groupby('Platform').agg(
        Spend=('Spend', 'sum'), Results=('Results', 'sum'),
        Impressions=('Impressions', 'sum'), Clicks=('Clicks', 'sum'),
        CTR=('CTR', 'mean'), CPC=('CPC', 'mean'),
        CPM=('CPM', 'mean'), CVR=('Conversion Rate', 'mean'),
        Score=('Efficiency Score', 'mean'),
    ).reset_index()
    plat['CPR'] = plat.apply(lambda r: r['Spend']/r['Results'] if r['Results'] > 0 else 0, axis=1)

    metrics = ['Spend', 'Results', 'CTR', 'CPM', 'CPC', 'CVR']
    cols = st.columns(len(df['Platform'].unique()))
    for i, (_, row) in enumerate(plat.iterrows()):
        with cols[i]:
            icon = '📘' if 'Meta' in row['Platform'] else '🎵'
            st.markdown(f"""
            <div class="card" style="text-align:center;border-top:4px solid {CHART_COLORS[i]}">
                <div style="font-size:2rem;margin-bottom:0.5rem">{icon}</div>
                <div style="font-weight:800;font-size:1.1rem;margin-bottom:1.25rem">{row['Platform']}</div>
                {"".join([f'<div style="display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid var(--border)"><span style="color:var(--text-secondary);font-size:0.82rem">{m}</span><span style="font-weight:700;font-size:0.9rem">{fmt_spend(row[m]) if m=="Spend" else fmt_pct(row[m]) if m in ["CTR","CVR"] else fmt_num(row[m])}</span></div>' for m in metrics])}
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div style="height:1.5rem"></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        fig = bar_chart(plat, 'Platform', 'Spend', 'Spend by Platform')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        fig2 = bar_chart(plat, 'Platform', 'Results', 'Results by Platform')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    c3, c4 = st.columns(2)
    with c3:
        fig3 = bar_chart(plat, 'Platform', 'CTR', 'Avg CTR by Platform')
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
    with c4:
        fig4 = bar_chart(plat, 'Platform', 'CPM', 'Avg CPM by Platform')
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

def render_campaigns(df: pd.DataFrame):
    if 'Campaign' not in df.columns:
        st.info("No campaign data detected.")
        return

    camp = df.groupby(['Platform', 'Campaign']).agg(
        Spend=('Spend', 'sum'), Results=('Results', 'sum'),
        Impressions=('Impressions', 'sum'), Clicks=('Clicks', 'sum'),
        CTR=('CTR', 'mean'), CPM=('CPM', 'mean'), CPC=('CPC', 'mean'),
        CPR=('Cost / Result', 'mean'), Score=('Efficiency Score', 'mean'),
    ).reset_index()

    platforms = ['All'] + list(df['Platform'].unique())
    sel_plat = st.selectbox('Filter by Platform', platforms, key='camp_plat')
    view = camp if sel_plat == 'All' else camp[camp['Platform'] == sel_plat]

    st.dataframe(view.sort_values('Spend', ascending=False).style.format({
        'Spend': 'EGP {:,.0f}', 'Results': '{:,.0f}', 'Impressions': '{:,.0f}',
        'Clicks': '{:,.0f}', 'CTR': '{:.2f}%', 'CPM': 'EGP {:.2f}',
        'CPC': 'EGP {:.2f}', 'CPR': 'EGP {:.2f}', 'Score': '{:.0f}',
    }), use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        top_spend = view.nlargest(10, 'Spend')
        fig = bar_chart(top_spend, 'Campaign', 'Spend', 'Top 10 Campaigns by Spend', orientation='h')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        top_res = view.nlargest(10, 'Results')
        fig2 = bar_chart(top_res, 'Campaign', 'Results', 'Top 10 Campaigns by Results', orientation='h')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

    sc = view[view['Results'] > 0]
    if not sc.empty:
        fig3 = scatter_chart(sc, 'Spend', 'Results', size='Results', color='Platform',
                             title='Spend vs Results', hover='Campaign')
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

def render_adsets(df: pd.DataFrame):
    if 'Ad Set / Group' not in df.columns:
        st.info("No ad set / ad group data detected.")
        return

    grp_cols = [c for c in ['Platform', 'Campaign', 'Ad Set / Group'] if c in df.columns]
    as_df = df.groupby(grp_cols).agg(
        Spend=('Spend', 'sum'), Results=('Results', 'sum'),
        CTR=('CTR', 'mean'), CPR=('Cost / Result', 'mean'),
        Frequency=('Frequency', 'mean'), Score=('Efficiency Score', 'mean'),
    ).reset_index()

    st.dataframe(as_df.sort_values('Spend', ascending=False).style.format({
        'Spend': 'EGP {:,.0f}', 'Results': '{:,.0f}', 'CTR': '{:.2f}%',
        'CPR': 'EGP {:.2f}', 'Frequency': '{:.2f}', 'Score': '{:.0f}',
    }), use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    valid = as_df[as_df['CPR'] > 0]
    with c1:
        top_cpr = valid.nsmallest(10, 'CPR')
        fig = bar_chart(top_cpr, 'Ad Set / Group', 'CPR', 'Best Ad Sets by Cost / Result', orientation='h')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        top_spend = as_df.nlargest(10, 'Spend')
        fig2 = bar_chart(top_spend, 'Ad Set / Group', 'Spend', 'Highest Spend Ad Sets', orientation='h')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

def render_ads(df: pd.DataFrame):
    if 'Ad' not in df.columns:
        st.info("No ad-level data detected.")
        return

    grp_cols = [c for c in ['Platform', 'Campaign', 'Ad'] if c in df.columns]
    ad_df = df.groupby(grp_cols).agg(
        Spend=('Spend', 'sum'), Results=('Results', 'sum'),
        CTR=('CTR', 'mean'), CPR=('Cost / Result', 'mean'),
        Hook=('Hook Rate', 'mean'), Score=('Efficiency Score', 'mean'),
    ).reset_index()

    st.dataframe(ad_df.sort_values('Results', ascending=False).style.format({
        'Spend': 'EGP {:,.0f}', 'Results': '{:,.0f}', 'CTR': '{:.2f}%',
        'CPR': 'EGP {:.2f}', 'Hook': '{:.1f}%', 'Score': '{:.0f}',
    }), use_container_width=True, hide_index=True)

    c1, c2 = st.columns(2)
    with c1:
        top_r = ad_df.nlargest(10, 'Results')
        fig = bar_chart(top_r, 'Ad', 'Results', 'Best Ads by Results', orientation='h')
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    with c2:
        valid = ad_df[ad_df['CPR'] > 0]
        if not valid.empty:
            top_cpr = valid.nsmallest(10, 'CPR')
            fig2 = bar_chart(top_cpr, 'Ad', 'CPR', 'Best Ads by Cost / Result', orientation='h')
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

def render_daily(df: pd.DataFrame):
    if 'Date' not in df.columns or df['Date'].isna().all():
        st.info("No date column detected.")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    daily = df.groupby('Date').agg(
        Spend=('Spend', 'sum'), Results=('Results', 'sum'),
        CTR=('CTR', 'mean'), CPR=('Cost / Result', 'mean'),
        Impressions=('Impressions', 'sum'), Clicks=('Clicks', 'sum'),
    ).reset_index().sort_values('Date')
    daily['CPR_calc'] = daily.apply(lambda r: r['Spend']/r['Results'] if r['Results'] > 0 else None, axis=1)

    fig1 = make_subplots(specs=[[{'secondary_y': True}]])
    fig1.add_trace(go.Bar(x=daily['Date'], y=daily['Spend'], name='Spend', marker_color=CHART_COLORS[0]), secondary_y=False)
    fig1.add_trace(go.Scatter(x=daily['Date'], y=daily['Results'], name='Results', mode='lines+markers',
                              line=dict(color=CHART_COLORS[1], width=2.5)), secondary_y=True)
    fig1.update_layout(**PLOTLY_LAYOUT, height=340, title='Daily Spend & Results')
    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})

    c1, c2 = st.columns(2)
    with c1:
        fig2 = line_chart(daily, 'Date', ['CPR_calc'], 'Daily Cost / Result')
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
    with c2:
        fig3 = line_chart(daily, 'Date', ['CTR'], 'Daily CTR (%)')
        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

    if 'Platform' in df.columns and df['Platform'].nunique() > 1:
        daily_plat = df.groupby(['Date', 'Platform'])['Spend'].sum().reset_index()
        fig4 = px.line(daily_plat, x='Date', y='Spend', color='Platform',
                       title='Daily Spend by Platform', color_discrete_sequence=CHART_COLORS)
        fig4.update_layout(**PLOTLY_LAYOUT, height=320)
        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})

def render_creative(df: pd.DataFrame):
    has_video = df['6s Views'].sum() > 0 or df['15s Views'].sum() > 0
    if not has_video:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">🎬</div>
            <div class="empty-title">No Video Metrics Available</div>
            <div class="empty-desc">Upload a report containing 6-second and 15-second view data to unlock creative analysis.</div>
        </div>
        """, unsafe_allow_html=True)
        return

    avg_hook = df['Hook Rate'].replace(0, np.nan).mean()
    avg_hold = df['Hold Rate'].replace(0, np.nan).mean()
    total_6s = df['6s Views'].sum()
    total_15s = df['15s Views'].sum()

    cards = [
        kpi_card('🪝', 'Avg Hook Rate', fmt_pct(avg_hook)),
        kpi_card('⏱️', 'Avg Hold Rate', fmt_pct(avg_hold)),
        kpi_card('▶️', 'Total 6s Views', fmt_num(total_6s)),
        kpi_card('🎞️', 'Total 15s Views', fmt_num(total_15s)),
    ]
    st.markdown(kpi_grid(cards), unsafe_allow_html=True)

    if 'Ad' in df.columns:
        ad_video = df.groupby('Ad').agg(
            Hook=('Hook Rate', 'mean'), Hold=('Hold Rate', 'mean'),
            Views6=('6s Views', 'sum'), Views15=('15s Views', 'sum'),
            Spend=('Spend', 'sum'), Results=('Results', 'sum'),
        ).reset_index()
        ad_video = ad_video[ad_video['Views6'] > 0].sort_values('Hook', ascending=False)

        c1, c2 = st.columns(2)
        with c1:
            top_hook = ad_video.nlargest(10, 'Hook')
            fig = bar_chart(top_hook, 'Ad', 'Hook', 'Top Ads by Hook Rate (%)', orientation='h')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        with c2:
            top_hold = ad_video.nlargest(10, 'Hold')
            fig2 = bar_chart(top_hold, 'Ad', 'Hold', 'Top Ads by Hold Rate (%)', orientation='h')
            st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})

        if not ad_video.empty:
            fig3 = scatter_chart(ad_video[ad_video['Views6'] > 0], 'Hook', 'Hold',
                                 size='Views6', title='Hook vs Hold Rate', hover='Ad')
            st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})

        st.markdown('<div class="section-header"><span class="section-title">Creative Performance Table</span></div>', unsafe_allow_html=True)
        st.dataframe(ad_video.style.format({
            'Hook': '{:.1f}%', 'Hold': '{:.1f}%',
            'Views6': '{:,.0f}', 'Views15': '{:,.0f}',
            'Spend': 'EGP {:,.0f}', 'Results': '{:,.0f}',
        }), use_container_width=True, hide_index=True)

def render_recommendations(df: pd.DataFrame):
    recs = generate_recommendations(df)
    if not recs:
        st.info("No recommendations generated. Upload more data for insights.")
        return

    priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
    recs_sorted = sorted(recs, key=lambda r: priority_order.get(r['priority'], 99))

    counts = {}
    for r in recs_sorted:
        counts[r['priority']] = counts.get(r['priority'], 0) + 1

    cards_h = []
    for p, label, color in [('critical','Critical','#DC2626'),('high','High','#D97706'),('medium','Medium','#1A56DB'),('low','Low','#059669')]:
        cards_h.append(f"""
        <div class="kpi-card" style="border-top-color:{color}">
            <div class="kpi-label">{label} Priority</div>
            <div class="kpi-value">{counts.get(p, 0)}</div>
        </div>""")
    st.markdown(kpi_grid(cards_h), unsafe_allow_html=True)

    filter_pri = st.multiselect('Filter by Priority', ['critical', 'high', 'medium', 'low'],
                                 default=['critical', 'high', 'medium', 'low'], key='rec_filter')
    for r in recs_sorted:
        if r['priority'] not in filter_pri:
            continue
        st.markdown(f"""
        <div class="rec-card {r['priority']}">
            <div>
                <span class="rec-priority {r['priority']}">{r['priority'].upper()}</span>
            </div>
            <div class="rec-content">
                <div class="rec-title">{r['icon']} {r['title']}</div>
                <div class="rec-explanation">{r['explanation']}</div>
                <div class="rec-action">{r['action']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_data_quality(df: pd.DataFrame, file_log: list, is_demo: bool):
    if is_demo:
        st.info("📊 Currently showing demo data. Upload real files to see data quality report.")

    if file_log:
        st.markdown('<div class="section-header"><span class="section-title">Uploaded Files</span></div>', unsafe_allow_html=True)
        for f in file_log:
            if f.get('error'):
                st.error(f"❌ {f['name']}: {f['error']}")
                continue
            icon = '📊' if str(f['name']).endswith('.csv') else '📗'
            st.markdown(f"""
            <div class="file-log-item">
                <span class="file-log-icon">{icon}</span>
                <div>
                    <div class="file-log-name">{f['name']}</div>
                    <div class="file-log-meta">
                        Platform: <b>{f.get('platform','—')}</b> &nbsp;|&nbsp;
                        Level: <b>{f.get('level','—')}</b> &nbsp;|&nbsp;
                        Rows: <b>{f.get('processed_rows','—')}</b>
                        (orig: {f.get('original_rows','—')}, summary removed: {f.get('summary_removed',0)})
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-header"><span class="section-title">Data Preview</span></div>', unsafe_allow_html=True)
    st.dataframe(df.head(50), use_container_width=True, hide_index=True)

    st.markdown('<div class="section-header"><span class="section-title">Column Coverage</span></div>', unsafe_allow_html=True)
    standard = ['Platform','Report Level','Campaign','Ad Set / Group','Ad','Spend','Results',
                'Impressions','Reach','Clicks','CTR','CPC','CPM','Conversion Rate',
                '6s Views','15s Views','Hook Rate','Hold Rate','Efficiency Score']
    cov = []
    for col in standard:
        present = col in df.columns
        non_null = df[col].notna().sum() if present else 0
        pct = int(non_null / len(df) * 100) if present and len(df) > 0 else 0
        cov.append({'Column': col, 'Present': '✅' if present else '❌',
                    'Non-Null Rows': non_null, 'Coverage %': pct})
    st.dataframe(pd.DataFrame(cov), use_container_width=True, hide_index=True)

def render_export(df: pd.DataFrame, file_log: list):
    recs = generate_recommendations(df)
    excel_bytes = build_excel_export(df, file_log, recs)
    csv_bytes = df.to_csv(index=False).encode('utf-8-sig')

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="card" style="text-align:center">
            <div style="font-size:2.5rem;margin-bottom:1rem">📄</div>
            <div style="font-weight:700;margin-bottom:0.5rem">Clean CSV Export</div>
            <div style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:1.25rem">
                All normalized data in a single CSV file, UTF-8 encoded with BOM for Excel compatibility.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button('⬇️ Download CSV', csv_bytes, 'roaya_clean_data.csv', 'text/csv', use_container_width=True)
    with c2:
        st.markdown("""
        <div class="card" style="text-align:center">
            <div style="font-size:2.5rem;margin-bottom:1rem">📗</div>
            <div style="font-weight:700;margin-bottom:0.5rem">Full Excel Report</div>
            <div style="color:var(--text-secondary);font-size:0.85rem;margin-bottom:1.25rem">
                Multi-sheet Excel workbook: Clean Data, Platform Summary, Campaign, Ad Set, Ad, Recommendations, Log.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.download_button('⬇️ Download Excel', excel_bytes, 'roaya_full_report.xlsx',
                           'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', use_container_width=True)

    st.markdown("""
    <div class="card" style="margin-top:1.5rem">
        <div class="section-header"><span class="section-title">Export Contents</span></div>
        <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:1rem">
    """, unsafe_allow_html=True)
    sheets = [
        ('📋', 'Clean Data', 'All normalized rows'),
        ('📊', 'Platform Summary', 'Aggregated by platform'),
        ('🎯', 'Campaign Summary', 'Campaign-level metrics'),
        ('📂', 'Ad Set Summary', 'Ad set / group metrics'),
        ('🖼️', 'Ad Summary', 'Ad-level performance'),
        ('💡', 'Recommended Actions', 'AI-generated recommendations'),
        ('📁', 'Files Log', 'Upload metadata'),
    ]
    for icon, name, desc in sheets:
        st.markdown(f"""
        <div style="background:var(--background);border:1px solid var(--border);border-radius:var(--radius-sm);padding:12px">
            <div style="font-size:1.4rem;margin-bottom:6px">{icon}</div>
            <div style="font-weight:600;font-size:0.88rem">{name}</div>
            <div style="color:var(--text-secondary);font-size:0.75rem">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# ─── SIDEBAR ───────────────────────────────────────────────────────────────────
def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-logo">
            <div class="sidebar-logo-icon">🎯</div>
            <div>
                <div class="sidebar-logo-text">ROAYA ADS</div>
                <div class="sidebar-logo-sub">Intelligence Dashboard</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section-label">Upload Reports</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader(
            '', type=['csv', 'xlsx'],
            accept_multiple_files=True,
            help='Upload Meta Ads or TikTok Ads exported reports (CSV or Excel)'
        )

        st.markdown('<div class="sidebar-section-label">Platform Filter</div>', unsafe_allow_html=True)
        plat_filter = st.multiselect('', ['Meta Ads', 'TikTok Ads'], default=['Meta Ads', 'TikTok Ads'], key='plat_filter', label_visibility='collapsed')

        st.markdown('<div class="sidebar-section-label">Supported Formats</div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.78rem;opacity:0.6;line-height:2">
            📘 Meta Ads Manager export<br>
            🎵 TikTok Ads Manager export<br>
            📄 CSV / XLSX<br>
            📊 Multiple files at once
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div style="height:1rem"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div style="font-size:0.72rem;opacity:0.35;text-align:center;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.08)">
            ROAYA Ads Intelligence v1.0<br>Powered by Python + Streamlit
        </div>
        """, unsafe_allow_html=True)

    return uploaded, plat_filter

# ─── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    uploaded, plat_filter = render_sidebar()

    is_demo = False
    file_log = []

    if not uploaded:
        is_demo = True
        df = generate_demo_data()
        file_log = [
            {'name': 'demo_meta.csv', 'platform': 'Meta Ads', 'level': 'Ad Level',
             'original_rows': 480, 'processed_rows': 480, 'summary_removed': 0},
            {'name': 'demo_tiktok.csv', 'platform': 'TikTok Ads', 'level': 'Ad Level',
             'original_rows': 360, 'processed_rows': 360, 'summary_removed': 0},
        ]
        st.info("🎭 **Demo Mode** — No files uploaded. Showing realistic sample data. Upload your own reports via the sidebar.")
    else:
        results = []
        for f in uploaded:
            r = process_file(f)
            results.append(r)
            file_log.append({k: v for k, v in r.items() if k != 'df'})
        df = combine_files(results)
        if df.empty:
            st.error("No valid data could be extracted from uploaded files.")
            return

    # Apply platform filter
    if 'Platform' in df.columns and plat_filter:
        df = df[df['Platform'].isin(plat_filter)]

    if df.empty:
        st.warning("No data matches the current platform filter.")
        return

    render_hero(df, is_demo)

    tabs = st.tabs([
        '📊 Overview', '⚖️ Platform Comparison', '🚀 Campaigns',
        '📂 Ad Sets / Groups', '🖼️ Ads', '📅 Daily Trends',
        '🎬 Creative Analysis', '💡 Recommendations', '🔍 Data Quality', '📥 Export'
    ])

    with tabs[0]: render_overview(df)
    with tabs[1]: render_platform_comparison(df)
    with tabs[2]: render_campaigns(df)
    with tabs[3]: render_adsets(df)
    with tabs[4]: render_ads(df)
    with tabs[5]: render_daily(df)
    with tabs[6]: render_creative(df)
    with tabs[7]: render_recommendations(df)
    with tabs[8]: render_data_quality(df, file_log, is_demo)
    with tabs[9]: render_export(df, file_log)

if __name__ == '__main__':
    main()
