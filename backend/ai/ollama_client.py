from ollama import chat


MODEL_NAME = "gemma3:4b"


def generate_response(prompt):

    response = chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]