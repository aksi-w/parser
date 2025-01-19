# titular.py
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Titular(Base):
    __tablename__ = 'titulars'

    profile = Column(String, primary_key=True)
    beginning_year = Column(Integer, primary_key=True)
    fgos = Column(String, primary_key=True)
    program = Column(String)

    def __repr__(self):
        return f"{self.profile}-{self.beginning_year}-{self.fgos}"