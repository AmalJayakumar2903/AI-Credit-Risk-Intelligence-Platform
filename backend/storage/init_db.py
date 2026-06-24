from backend.storage.models import Base
from backend.storage.postgres import engine


Base.metadata.create_all(
    bind=engine
)

print(
    "Tables created."
)