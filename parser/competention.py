from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Competention(Base):
    __tablename__ = 'competentions'

    sub_index = Column(String)
    index = Column(String)
    description = Column(String, primary_key=True)
    type = Column(String)

    def __init__(self, sub_index=None, index=None, description=None, type=None):
        self.sub_index = sub_index
        self.index = index
        self.description = description
        self.type = type

    def __repr__(self):
        return f"Competention(sub_index={self.sub_index}, index={self.index}, description={self.description}, type={self.type})"