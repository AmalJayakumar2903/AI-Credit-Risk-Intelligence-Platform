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

        runs = (
            db.query(AnalysisRun)
            .order_by(
                AnalysisRun.created_at.desc()
            )
            .all()
        )

        return runs

    finally:

        db.close()


def get_analysis_by_id(analysis_id):

    db = SessionLocal()

    try:

        run = (
            db.query(AnalysisRun)
            .filter(
                AnalysisRun.id == analysis_id
            )
            .first()
        )

        return run

    finally:

        db.close()


def compare_runs(id1, id2):

    db = SessionLocal()

    try:

        run1 = (
            db.query(AnalysisRun)
            .filter(
                AnalysisRun.id == id1
            )
            .first()
        )

        run2 = (
            db.query(AnalysisRun)
            .filter(
                AnalysisRun.id == id2
            )
            .first()
        )

        return run1, run2

    finally:

        db.close()