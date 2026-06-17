import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from assets.styles import CSS
from utils.api_client import health

st.set_page_config(
    page_title="GradePulse",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS, unsafe_allow_html=True)

from views import dashboard, grades, ai_tips

PAGES = [
    ("📊", "Dashboard",    dashboard),
    ("📝", "Grades",       grades),
    ("🤖", "AI Tips",      ai_tips),
]

with st.sidebar:
    st.markdown('<div class="brand">🎓 GradePulse</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">STUDENT GRADE TRACKER</div>', unsafe_allow_html=True)

    online = health()
    dot = "dot-on" if online else "dot-off"
    txt = "API Connected" if online else "API Offline — check API_BASE_URL"
    st.markdown(
        f'<div style="text-align:center;font-size:.78rem;color:#7A90A8;margin-bottom:18px">'
        f'<span class="{dot}"></span>{txt}</div>',
        unsafe_allow_html=True,
    )

    if "page" not in st.session_state:
        st.session_state["page"] = "Dashboard"

    for icon, label, _ in PAGES:
        if st.button(f"{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            st.session_state["page"] = label
            st.rerun()

    st.markdown("<br>" * 4, unsafe_allow_html=True)
    st.markdown(
        '<div style="text-align:center;font-size:.68rem;color:#7A90A8">'
        'Adnan Raza · Roll No. 0267<br>Level 2 · Project 8</div>',
        unsafe_allow_html=True,
    )

active = st.session_state.get("page", "Dashboard")
module = next((m for _, lbl, m in PAGES if lbl == active), dashboard)

st.markdown('<div style="padding:28px 36px">', unsafe_allow_html=True)
module.render()
st.markdown('</div>', unsafe_allow_html=True)
