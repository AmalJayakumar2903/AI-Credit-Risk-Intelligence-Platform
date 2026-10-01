from fastapi import FastAPI
from fastapi import UploadFile
from fastapi import File

from pydantic import BaseModel

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

from backend.ai.rag import (
    answer_document_question
)

from backend.ai.dataset_qa import (
    answer_dataset_question
)


app = FastAPI()


class DocumentQuestion(BaseModel):
    query: str

class AIQuestion(BaseModel):
    query: str
    analysis_context: dict

class DatasetQuestion(BaseModel):

    analysis_id: int
    query: str

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
                f"{run1.top_risk_grade} -> "
                f"{run2.top_risk_grade}"

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


@app.post("/ai/document")
async def ai_document(
    question: DocumentQuestion
):

    result = answer_document_question(
        question.query
    )

    return result

@app.post("/ai/ask")
async def ai_ask(
    question: AIQuestion
):
    prompt = f"""
You are an AI credit risk analyst.

The user has already run a credit portfolio analysis.

Use ONLY the analysis results provided below to answer
the user's question.

Do not invent metrics or facts that are not present
in the analysis context.

If the available context is insufficient to answer,
clearly say that the available analysis does not contain
enough information.

Analysis results:
{question.analysis_context}

User question:
{question.query}

Give a concise, professional answer.
"""

    response = generate_response(prompt)

    return {
        "query": question.query,
        "answer": response
    }

@app.post("/ai/dataset")
async def ai_dataset(
    question: DatasetQuestion
):

    result = answer_dataset_question(
        question.analysis_id,
        question.query
    )

    return result