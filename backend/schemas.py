from typing import Optional
from pydantic import BaseModel, Field


class GradeCreate(BaseModel):
    student_name: str = Field(min_length=1)
    roll_number: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    marks_obtained: float = Field(ge=0)
    total_marks: float = Field(gt=0)
    semester: str
    date: str


class GradeUpdate(BaseModel):
    student_name: Optional[str] = None
    roll_number: Optional[str] = None
    subject: Optional[str] = None
    marks_obtained: Optional[float] = None
    total_marks: Optional[float] = None
    semester: Optional[str] = None
    date: Optional[str] = None


class GradeResponse(BaseModel):
    id: int
    student_name: str
    roll_number: str
    subject: str
    marks_obtained: float
    total_marks: float
    semester: str
    date: str
    percentage: float
    grade_letter: str

    model_config = {"from_attributes": True}


class StudyTipsRequest(BaseModel):
    additional_context: Optional[str] = None
