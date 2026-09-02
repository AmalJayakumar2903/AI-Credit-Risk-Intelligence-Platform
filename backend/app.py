from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

import shutil

from backend.ingestion.excel_loader import load_file
from backend.pipeline import run_analysis

from backend.storage.repository import (
    save_analysis_run,
    get_all_analysis_runs,
    get_analysis_by_id,
    compare_runs
)

from backend.ai.ollama_client import (
    generate_response
)

from backend.ai.risk_explainer import (
    generate_risk_explanation
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

    ai_explanation = generate_risk_explanation(

        result["portfolio"],

        result["risk"],

        result["risk_drivers"],

        result["recommendations"]

    )

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
            result["insight"],

        "ai_explanation":
            ai_explanation

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


@app.get("/history/{analysis_id}")
def history_record(
    analysis_id: int
):

    run = get_analysis_by_id(
        analysis_id
    )

    if not run:

        return {

            "error":
                "Analysis not found"

        }

    return {

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


@app.get("/compare")
def compare(
    id1: int,
    id2: int
):

    run1, run2 = compare_runs(
        id1,
        id2
    )

    if not run1 or not run2:

        return {

            "error":
                "One or both analysis IDs not found"

        }

    return {

        "run_1": {

            "id":
                run1.id,

            "dataset_name":
                run1.dataset_name,

            "chargeoff_rate":
                run1.chargeoff_rate,

            "top_risk_grade":
                run1.top_risk_grade

        },

        "run_2": {

            "id":
                run2.id,

            "dataset_name":
                run2.dataset_name,

            "chargeoff_rate":
                run2.chargeoff_rate,

            "top_risk_grade":
                run2.top_risk_grade

        },

        "differences": {

            "chargeoff_rate_change":
                round(
                    run2.chargeoff_rate
                    -
                    run1.chargeoff_rate,
                    2
                ),

            "risk_grade_change":
                f"{run1.top_risk_grade} -> {run2.top_risk_grade}"

        }

    }


@app.post("/ai/test")
async def ai_test():

    prompt = """
    You are a credit risk analyst.

    Explain charge-off rate in one simple sentence.
    """

    response = generate_response(
        prompt
    )

    return {

        "model":
            "gemma3:4b",

        "response":
            response

    }