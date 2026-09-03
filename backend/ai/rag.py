from backend.ai.document_retriever import search_documents
from backend.ai.ollama_client import generate_response


def answer_document_question(query):

    documents = search_documents(
        query,
        n_results=3
    )

    context = "\n\n".join(documents)

    prompt = f"""
You are a credit risk analyst.

Answer the user's question using only the provided document context.

Document context:
{context}

Question:
{query}

If the context does not contain enough information, say so.

Give a concise, professional answer.
"""

    response = generate_response(prompt)

    return {
        "question": query,
        "answer": response,
        "sources_used": len(documents)
    }