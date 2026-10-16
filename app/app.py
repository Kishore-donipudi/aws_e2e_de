# --- diagnostics bootstrap: install crash/exception logging before app code ---
import os as _diag_os
import sys as _diag_sys

_diag_file = globals().get("__file__")
if _diag_file:
    _diag_dir = _diag_os.path.dirname(_diag_os.path.abspath(_diag_file))
else:
    _diag_dir = _diag_os.getcwd()
if _diag_dir not in _diag_sys.path:
    _diag_sys.path.insert(0, _diag_dir)
import app_diagnostics  # noqa: E402

app_diagnostics.install_diagnostics()
# --- end diagnostics bootstrap ---

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Food Delivery Analytics", layout="wide")

# ---------- Page styling ----------
st.markdown(
    """
    <style>
        /* App background gradient */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        }
        /* Title styling */
        .dashboard-title {
            text-align: center;
            color: #f8fafc;
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
        }
        .dashboard-subtitle {
            text-align: center;
            color: #94a3b8;
            font-size: 1.05rem;
            margin-bottom: 1.2rem;
        }
        /* Iframe container */
        .iframe-container {
            background: #ffffff;
            border-radius: 14px;
            box-shadow: 0 12px 40px rgba(0,0,0,0.45);
            overflow: hidden;
            margin-top: 0.5rem;
        }
        /* KPI badges */
        .kpi-row {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            flex-wrap: wrap;
            margin-bottom: 1.5rem;
        }
        .kpi-badge {
            background: rgba(30,41,59,0.9);
            border: 1px solid rgba(148,163,184,0.3);
            border-radius: 10px;
            padding: 0.55rem 1.4rem;
            color: #e2e8f0;
            font-size: 0.95rem;
        }
        .kpi-badge strong { color: #38bdf8; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown('<div class="dashboard-title">🍔 Food Delivery Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="dashboard-subtitle">Real-time insights across orders, revenue, restaurants, agents & customers</div>', unsafe_allow_html=True)

# ---------- KPI summary badges ----------
st.markdown(
    '<div class="kpi-row">'
    '<span class="kpi-badge">Total Revenue: <strong>$5.82M</strong></span>'
    '<span class="kpi-badge">Total Orders: <strong>14.5K+</strong></span>'
    '<span class="kpi-badge">Restaurants: <strong>50+</strong></span>'
    '<span class="kpi-badge">Delivery Agents: <strong>351</strong></span>'
    '</div>',
    unsafe_allow_html=True,
)

# ---------- Embedded dashboard ----------
DASHBOARD_URL = "https://dbc-19cbe2d6-45e2.cloud.databricks.com/embed/dashboardsv3/01f1c9692c6e153ebbce9ac0ee4f4f41?o=7474650659417681"

st.markdown('<div class="iframe-container">', unsafe_allow_html=True)
components.iframe(src=DASHBOARD_URL, height=900, scrolling=True)
st.markdown('</div>', unsafe_allow_html=True)
