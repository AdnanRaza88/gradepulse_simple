import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.api_client import list_grades


def badge(letter):
    css = "ga" if letter in ("A","A+") else "gb_" if letter.startswith("B") else "gc" if letter.startswith("C") else "gf"
    return f'<span class="gb {css}">{letter}</span>'


def render():
    st.markdown('<div class="ptitle">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Overall student performance overview</div>', unsafe_allow_html=True)

    try:
        grades = list_grades()
    except Exception as e:
        st.markdown(f'<div class="err">Could not load data: {e}</div>', unsafe_allow_html=True)
        return

    if not grades:
        st.markdown('<div class="card-inset">No records yet — add some grades to get started.</div>', unsafe_allow_html=True)
        return

    df = pd.DataFrame(grades)

    c1, c2, c3, c4 = st.columns(4)
    stats = [
        (len(df), "Total Records"),
        (df["student_name"].nunique(), "Students"),
        (f"{df['percentage'].mean():.1f}%", "Avg Score"),
        (df[df["grade_letter"] == "F"].shape[0], "Failing"),
    ]
    for col, (val, lbl) in zip([c1,c2,c3,c4], stats):
        with col:
            st.markdown(f'<div class="stat"><div class="stat-num">{val}</div><div class="stat-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        gc = df["grade_letter"].value_counts().reset_index()
        gc.columns = ["Grade", "Count"]
        colors = {"A+":"#38C97A","A":"#4EC98A","B":"#4A7FE5","C":"#F5A623","D":"#E07B5D","F":"#E05D5D"}
        fig = go.Figure(go.Bar(
            x=gc["Grade"], y=gc["Count"],
            marker_color=[colors.get(g,"#8FA3BF") for g in gc["Grade"]],
            text=gc["Count"], textposition="outside",
        ))
        fig.update_layout(title="Grade Distribution", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(family="Inter",color="#2D3748"), height=280, margin=dict(t=40,b=10,l=0,r=0),
                          xaxis=dict(showgrid=False), yaxis=dict(showgrid=True,gridcolor="#D1DCF0"))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        top = df.groupby("student_name")["percentage"].mean().round(1).sort_values(ascending=False).head(5).reset_index()
        top.columns = ["Student","Avg %"]
        fig2 = go.Figure(go.Bar(
            x=top["Avg %"], y=top["Student"], orientation="h",
            marker_color="#4A7FE5", text=top["Avg %"].astype(str)+"%", textposition="outside",
        ))
        fig2.update_layout(title="Top 5 Students", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                           font=dict(family="Inter",color="#2D3748"), height=280, margin=dict(t=40,b=10,l=0,r=0),
                           xaxis=dict(range=[0,110],showgrid=True,gridcolor="#D1DCF0"), yaxis=dict(showgrid=False))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
