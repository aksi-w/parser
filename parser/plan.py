# plan.py
from sqlalchemy import Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY

Base = declarative_base()

class Plan(Base):
    __tablename__ = 'plans'

    count_in_plan = Column(Boolean)
    index = Column(String, primary_key=True)
    name = Column(String)
    exam = Column(String)
    midterm = Column(String)
    kp = Column(String)
    coursework = Column(String)
    controlwork = Column(String)
    midterm_with_mark = Column(String)
    expert = Column(String)
    factual = Column(String)
    expert_hour = Column(String)
    plan = Column(String)
    controlwork_hour = Column(String)
    aud = Column(String)
    sr = Column(String)
    control = Column(String)
    preparation = Column(String)
    courses_semesters = Column(ARRAY(String))
    faculty_code = Column(String)
    faculty_name = Column(String)

    def __init__(
        self, count_in_plan=None, index=None, name=None, exam=None, midterm=None, kp=None, coursework=None,
        controlwork=None, midterm_with_mark=None, expert=None, factual=None, expert_hour=None, plan=None,
        controlwork_hour=None, aud=None, sr=None, control=None, preparation=None, courses_semesters=None,
        faculty_code=None, faculty_name=None
    ):
        self.count_in_plan = count_in_plan
        self.index = index
        self.name = name
        self.exam = exam
        self.midterm = midterm
        self.kp = kp
        self.coursework = coursework
        self.controlwork = controlwork
        self.midterm_with_mark = midterm_with_mark
        self.expert = expert
        self.factual = factual
        self.expert_hour = expert_hour
        self.plan = plan
        self.controlwork_hour = controlwork_hour
        self.aud = aud
        self.sr = sr
        self.control = control
        self.preparation = preparation
        self.courses_semesters = courses_semesters or []
        self.faculty_code = faculty_code
        self.faculty_name = faculty_name

    def __repr__(self):
        return f"Plan(index={self.index}, name={self.name}, faculty_name={self.faculty_name})"