from backend.ai.ollama_client import generate_response


prompt = """
You are a credit risk analyst.

Explain charge-off rate in one simple sentence.
"""


response = generate_response(prompt)

print(response)