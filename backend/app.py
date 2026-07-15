from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

import shutil

from backend.ingestion.excel_loader import load_file
from backend.pipeline import run_analysis
from backend.storage.repository import (
    save_analysis_run,
    get_all_analysis_runs
)

app = FastAPI()


@app.get("/")
def home():

    return {
        "status": "running",
        "application": "CredRiskAnalyzer"
    }


@app.post("/analyze")
async def analyze_file(
    file: UploadFile = File(...)
):

    temp_path = (
        f"data/raw/{file.filename}"
    )

    with open(
        temp_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    df = load_file(
        temp_path,
        nrows=2000
    )

    result = run_analysis(df)

    analysis_id = save_analysis_run({

        "dataset_name":
            file.filename,

        "dataset_type":
            result["classification"]["dataset_type"],

        "confidence":
            result["classification"]["confidence"],

        "total_loans":
            result["portfolio"]["total_loans"],

        "chargeoff_rate":
            result["risk"]["chargeoff_rate"],

        "top_risk_grade":
            result["risk_drivers"]["top_grade"]["grade"]

    })

    return {

        "analysis_id":
            analysis_id,

        "portfolio":
            result["portfolio"],

        "risk":
            result["risk"],

        "segmentation":
            result["segmentation"],

        "recommendations":
            result["recommendations"],

        "insight":
            result["insight"]

    }


@app.post("/profile")
async def profile_file(
    file: UploadFile = File(...)
):

    temp_path = (
        f"data/raw/{file.filename}"
    )

    with open(
        temp_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    df = load_file(
        temp_path,
        nrows=2000
    )

    result = run_analysis(df)

    return {

        "classification":
            result["classification"],

        "profile":
            result["profile"],

        "validation":
            result["validation"],

        "cleaning_report":
            result["cleaning_report"]

    }

@app.get("/history")
def history():

    runs = get_all_analysis_runs()

    return [

        {
            "id":
                run.id,

            "dataset_name":
                run.dataset_name,

            "dataset_type":
                run.dataset_type,

            "confidence":
                run.confidence,

            "total_loans":
                run.total_loans,

            "chargeoff_rate":
                run.chargeoff_rate,

            "top_risk_grade":
                run.top_risk_grade,

            "created_at":
                run.created_at
        }

        for run in runs
    ]