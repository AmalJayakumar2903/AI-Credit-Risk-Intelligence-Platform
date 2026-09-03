import chromadb
from chromadb.utils.embedding_functions import OllamaEmbeddingFunction


client = chromadb.PersistentClient(
    path="data/chroma"
)


embedding_function = OllamaEmbeddingFunction(
    model_name="nomic-embed-text",
    url="http://localhost:11434"
)


documents_collection = client.get_or_create_collection(
    name="credit_documents",
    embedding_function=embedding_function
)