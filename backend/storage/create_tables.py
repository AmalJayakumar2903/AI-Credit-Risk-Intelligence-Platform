from backend.storage.postgres import engine
from backend.storage.models import Base

Base.metadata.create_all(bind=engine)

print("Tables created.")