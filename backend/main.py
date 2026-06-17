import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from database import create_db_and_tables, get_session
from models import Grade
from schemas import GradeCreate, GradeUpdate, GradeResponse, StudyTipsRequest


# ── Startup ──────────────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="GradePulse API",
    description="Student Grade Tracker — Adnan Raza (Roll No. 0267)",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helpers ───────────────────────────────────────────────────────────────────

GRADE_SCALE = [
    (90, "A+"), (80, "A"), (70, "B"), (60, "C"), (50, "D"), (0, "F")
]

def compute(marks: float, total: float):
    pct = round((marks / total) * 100, 2) if total > 0 else 0.0
    letter = next(g for threshold, g in GRADE_SCALE if pct >= threshold)
    return pct, letter


# ── 1. POST /grades ───────────────────────────────────────────────────────────

@app.post("/grades", response_model=GradeResponse, tags=["Grades"])
def create_grade(payload: GradeCreate, session: Session = Depends(get_session)):
    if payload.marks_obtained > payload.total_marks:
        raise HTTPException(status_code=400, detail="marks_obtained cannot exceed total_marks")
    pct, letter = compute(payload.marks_obtained, payload.total_marks)
    grade = Grade(**payload.model_dump(), percentage=pct, grade_letter=letter)
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade


# ── 2. GET /grades ────────────────────────────────────────────────────────────

@app.get("/grades", response_model=list[GradeResponse], tags=["Grades"])
def list_grades(semester: Optional[str] = None, session: Session = Depends(get_session)):
    query = select(Grade)
    if semester:
        query = query.where(Grade.semester == semester)
    return session.exec(query).all()


# ── 3. GET /grades/{id} ───────────────────────────────────────────────────────

@app.get("/grades/{grade_id}", response_model=GradeResponse, tags=["Grades"])
def get_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    return grade


# ── 4. PUT /grades/{id} ───────────────────────────────────────────────────────

@app.put("/grades/{grade_id}", response_model=GradeResponse, tags=["Grades"])
def update_grade(grade_id: int, payload: GradeUpdate, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    for key, value in payload.model_dump(exclude_none=True).items():
        setattr(grade, key, value)
    grade.percentage, grade.grade_letter = compute(grade.marks_obtained, grade.total_marks)
    session.add(grade)
    session.commit()
    session.refresh(grade)
    return grade


# ── 5. DELETE /grades/{id} ────────────────────────────────────────────────────

@app.delete("/grades/{grade_id}", tags=["Grades"])
def delete_grade(grade_id: int, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")
    session.delete(grade)
    session.commit()
    return {"message": "Deleted successfully"}


# ── 6. POST /grades/{id}/study-tips  ← Required AI endpoint ──────────────────

@app.post("/grades/{grade_id}/study-tips", tags=["AI"])
def study_tips(grade_id: int, payload: StudyTipsRequest, session: Session = Depends(get_session)):
    grade = session.get(Grade, grade_id)
    if not grade:
        raise HTTPException(status_code=404, detail="Grade not found")

    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model="llama-3.3-70b-versatile", temperature=0.7)

    prompt = ChatPromptTemplate.from_template(
        """You are an academic coach. A student needs help.

Student: {name}
Subject: {subject}
Score: {marks}/{total} = {pct}% ({grade})
Extra context: {context}

Give 5 specific, actionable study tips for this subject and score level.
Format each tip as:
**Tip [number] — [Short Title]**: [2-3 sentence advice]

End with one motivational sentence."""
    )

    chain = prompt | llm | StrOutputParser()
    tips = chain.invoke({
        "name": grade.student_name,
        "subject": grade.subject,
        "marks": grade.marks_obtained,
        "total": grade.total_marks,
        "pct": grade.percentage,
        "grade": grade.grade_letter,
        "context": payload.additional_context or "None",
    })

    return {
        "student": grade.student_name,
        "subject": grade.subject,
        "percentage": grade.percentage,
        "grade": grade.grade_letter,
        "tips": tips,
    }


# ── Bonus: GET /grades/student/{roll_number} ──────────────────────────────────

@app.get("/grades/student/{roll_number}", response_model=list[GradeResponse], tags=["Bonus"])
def student_by_roll(roll_number: str, session: Session = Depends(get_session)):
    grades = session.exec(select(Grade).where(Grade.roll_number == roll_number)).all()
    if not grades:
        raise HTTPException(status_code=404, detail=f"No records for roll number {roll_number}")
    return grades


# ── Health check ──────────────────────────────────────────────────────────────

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}
