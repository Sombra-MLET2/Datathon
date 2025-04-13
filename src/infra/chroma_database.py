from typing import List

import chromadb
from chromadb import EmbeddingFunction
from sentence_transformers import SentenceTransformer

from src.infra.configs import logger

logger.info("Loading Hugging Face multilingual embedding model")
model_transformer = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')


class MultiLingualMLM12(EmbeddingFunction):
    def __init__(self, model):
        self.model = model

    def __call__(self, input: List[str]) -> List[List[float]]:
        return self.model.embed(input)

chroma_client = chromadb.PersistentClient("./data/chroma_storage")

embedding_function = MultiLingualMLM12(model=model_transformer)

logger.info("Loading candidates collection")
candidates_collection = chroma_client.get_or_create_collection(
    name="candidates",
    embedding_function=embedding_function
)

logger.info("✅ Documents / embeddings are ready to use.")
