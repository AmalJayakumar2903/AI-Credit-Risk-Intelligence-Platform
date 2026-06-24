from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime
)

from datetime import datetime


class Base(DeclarativeBase):
    pass


class AnalysisRun(Base):

    __tablename__ = "analysis_runs"

    id = Column(
        Integer,
        primary_key=True
    )

    dataset_name = Column(
        String(255)
    )

    dataset_type = Column(
        String(100)
    )

    confidence = Column(
        Float
    )

    total_loans = Column(
        Integer
    )

    chargeoff_rate = Column(
        Float
    )

    top_risk_grade = Column(
        String(20)
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )