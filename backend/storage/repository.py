from backend.storage.postgres import SessionLocal
from backend.storage.models import AnalysisRun


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


def get_all_analysis_runs():

    db = SessionLocal()

    try:

        return (
            db.query(AnalysisRun)
            .order_by(
                AnalysisRun.created_at.desc()
            )
            .all()
        )

    finally:

        db.close()


def get_analysis_run(run_id):

    db = SessionLocal()

    try:

        return (
            db.query(AnalysisRun)
            .filter(
                AnalysisRun.id == run_id
            )
            .first()
        )

    finally:

        db.close()