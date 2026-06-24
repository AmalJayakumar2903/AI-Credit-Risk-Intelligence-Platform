from backend.storage.postgres import engine

with engine.connect() as conn:
    print(
        "Connected to PostgreSQL."
    )