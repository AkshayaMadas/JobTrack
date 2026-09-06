from sqlalchemy import Column, Integer, String
from app.config.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String, nullable=False)
    position = Column(String, nullable=False)
    location = Column(String, nullable=False)
    status = Column(String, nullable=False)
    notes = Column(String, nullable=True)