import streamlit as st
import pandas as pd
from utils.api_client import list_grades, create_grade, update_grade, delete_grade, student_grades


def render():
    st.markdown('<div class="ptitle">📝 Grade Records</div>', unsafe_allow_html=True)
    st.markdown('<div class="psub">Add, view, edit and delete grade entries</div>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["All Records", "Add Grade", "Student Lookup"])

    with tab1:
        try:
            grades = list_grades()
        except Exception as e:
            st.markdown(f'<div class="err">Error: {e}</div>', unsafe_allow_html=True)
            return

        if not grades:
            st.markdown('<div class="card-inset">No records found.</div>', unsafe_allow_html=True)
        else:
            df = pd.DataFrame(grades)[["id","student_name","roll_number","subject","marks_obtained","total_marks","percentage","grade_letter","semester","date"]]
            df.columns = ["ID","Student","Roll","Subject","Marks","Total","Pct%","Grade","Semester","Date"]
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown("**Edit / Delete**")
            sel_id = st.selectbox("Select record ID", [g["id"] for g in grades], key="sel_id")
            sel = next((g for g in grades if g["id"] == sel_id), None)
            if sel:
                with st.expander("Edit record"):
                    c1, c2 = st.columns(2)
                    with c1:
                        nm = st.number_input("Marks Obtained", value=float(sel["marks_obtained"]), key="e_m")
                        nt = st.number_input("Total Marks", value=float(sel["total_marks"]), key="e_t")
                    with c2:
                        ns = st.text_input("Subject", value=sel["subject"], key="e_s")
                        nd = st.text_input("Date", value=sel["date"], key="e_d")
                    ca, cb = st.columns(2)
                    with ca:
                        if st.button("Save", key="btn_save"):
                            try:
                                update_grade(sel_id, {"marks_obtained":nm,"total_marks":nt,"subject":ns,"date":nd})
                                st.markdown('<div class="ok">Updated successfully.</div>', unsafe_allow_html=True)
                                st.rerun()
                            except Exception as e:
                                st.markdown(f'<div class="err">{e}</div>', unsafe_allow_html=True)
                    with cb:
                        if st.button("Delete", key="btn_del"):
                            st.session_state["_del"] = sel_id
                        if st.session_state.get("_del") == sel_id:
                            st.warning("Confirm delete?")
                            if st.button("Yes, Delete", key="btn_del_yes"):
                                try:
                                    delete_grade(sel_id)
                                    st.session_state.pop("_del", None)
                                    st.rerun()
                                except Exception as e:
                                    st.markdown(f'<div class="err">{e}</div>', unsafe_allow_html=True)

    with tab2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            name  = st.text_input("Student Name", key="a_name")
            roll  = st.text_input("Roll Number", key="a_roll")
            subj  = st.text_input("Subject", key="a_subj")
        with c2:
            marks = st.number_input("Marks Obtained", min_value=0.0, key="a_marks")
            total = st.number_input("Total Marks", min_value=1.0, value=100.0, key="a_total")
            sem   = st.text_input("Semester", key="a_sem")
            date  = st.text_input("Date (YYYY-MM-DD)", key="a_date")

        if st.button("Add Record", key="btn_add"):
            if not all([name, roll, subj, sem, date]):
                st.markdown('<div class="err">Fill all fields.</div>', unsafe_allow_html=True)
            elif marks > total:
                st.markdown('<div class="err">Marks cannot exceed total.</div>', unsafe_allow_html=True)
            else:
                try:
                    r = create_grade({"student_name":name,"roll_number":roll,"subject":subj,
                                      "marks_obtained":marks,"total_marks":total,"semester":sem,"date":date})
                    st.markdown(f'<div class="ok">Added — {r["percentage"]}% ({r["grade_letter"]})</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.markdown(f'<div class="err">{e}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tab3:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        roll_in = st.text_input("Enter Roll Number", key="lu_roll")
        if st.button("Search", key="btn_lu"):
            try:
                data = student_grades(roll_in.strip())
                if isinstance(data, list) and data:
                    st.markdown(f"**{data[0]['student_name']}** — {len(data)} subjects")
                    for g in data:
                        pct = g["percentage"]
                        color = "#38C97A" if pct>=70 else "#F5A623" if pct>=50 else "#E05D5D"
                        st.markdown(
                            f'<div style="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #D1DCF0">'
                            f'<span><b>{g["subject"]}</b></span>'
                            f'<span style="color:{color};font-weight:700">{pct}%</span>'
                            f'</div>',
                            unsafe_allow_html=True
                        )
                else:
                    st.markdown('<div class="err">No records found.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="err">{e}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
