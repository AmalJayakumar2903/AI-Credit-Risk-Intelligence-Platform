from backend.storage.postgres import (
    SessionLocal
)

from backend.storage.models import (
    AnalysisRun
)


def save_analysis_run(data):

    db = SessionLocal()

    try:

        run = AnalysisRun(
            dataset_name=data["dataset_name"],
            dataset_type=data["dataset_type"],
            confidence=data["confidence"],
            total_loans=data["total_loans"],
            chargeoff_rate=data["chargeoff_rate"],
            top_risk_grade=data["top_risk_grade"]
        )

        db.add(run)

        db.commit()

        db.refresh(run)

        return run.id

    finally:

        db.close()