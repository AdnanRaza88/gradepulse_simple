import streamlit as st
from utils.api_client import list_grades, get_tips


def render():
    st.markdown('<div class="ptitle">🤖 AI Study Tips</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Personalized advice powered by Groq LLM + LangChain</div>', unsafe_allow_html=True)

    try:
        grades = list_grades()
    except Exception as e:
        st.markdown(f'<div class="err">Could not load grades: {e}</div>', unsafe_allow_html=True)
        return

    if not grades:
        st.markdown('<div class="card-inset">No grade records found. Add grades first.</div>', unsafe_allow_html=True)
        return

    st.markdown('<div class="card">', unsafe_allow_html=True)

    options = {f"{g['student_name']} — {g['subject']} ({g['percentage']}%)": g["id"] for g in grades}
    selected_label = st.selectbox("Select a grade record", list(options.keys()), key="tip_sel")
    selected_id = options[selected_label]
    sel = next(g for g in grades if g["id"] == selected_id)

    c1, c2, c3 = st.columns(3)
    c1.metric("Student", sel["student_name"])
    c2.metric("Subject", sel["subject"])
    c3.metric("Score", f"{sel['percentage']}% ({sel['grade_letter']})")

    context = st.text_area("Any extra context? (optional)",
        placeholder="e.g. Exam in 2 weeks, weak in calculus, study 3 hrs daily...",
        height=80, key="tip_ctx")

    if st.button("Generate Study Tips", key="btn_tips"):
        with st.spinner("Groq LLM thinking..."):
            try:
                result = get_tips(selected_id, context)
                st.session_state["_tips"] = result.get("tips", "")
                st.session_state["_tips_lbl"] = f"{sel['student_name']} — {sel['subject']}"
            except Exception as e:
                st.markdown(f'<div class="err">AI failed: {e}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if "_tips" in st.session_state:
        st.markdown('<div class="ai-box">', unsafe_allow_html=True)
        st.markdown(f"### 📚 {st.session_state['_tips_lbl']}")
        st.divider()
        st.markdown(st.session_state["_tips"])
        st.markdown('</div>', unsafe_allow_html=True)
