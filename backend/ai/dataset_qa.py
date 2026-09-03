from backend.storage.repository import get_analysis_by_id

from backend.ai.dataset_context import (
    build_dataset_context
)

from backend.ai.ollama_client import (
    generate_response
)


def answer_dataset_question(
    analysis_id,
    query
):

    run = get_analysis_by_id(
        analysis_id
    )

    if not run:

        return {
            "error":
                "Analysis not found"
        }

    context = build_dataset_context(
        run
    )

    prompt = f"""
You are a credit risk analyst.

Answer the user's question using only
the dataset analysis provided below.

Dataset analysis:
{context}

User question:
{query}

Rules:

- Use only the provided analysis.
- Do not invent statistics.
- Do not assume values that are not provided.
- If the analysis does not contain enough
  information to answer the question,
  clearly say that the information is not
  available.

Give a concise professional answer.
"""

    response = generate_response(
        prompt
    )

    return {
        "analysis_id":
            analysis_id,

        "dataset":
            run.dataset_name,

        "question":
            query,

        "answer":
            response
    }