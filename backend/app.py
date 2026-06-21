from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

import shutil

from backend.ingestion.excel_loader import load_file
from backend.pipeline import run_analysis

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

    return {

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