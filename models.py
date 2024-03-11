from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    pdf = Column(String)
    status = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
