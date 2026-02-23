from sentence_transformers import SentenceTransformer
from app.core.config import settings
import numpy as np
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Handles loading the embedding model and generating embeddings.
    Uses singleton pattern to load model only once.
    """

    _model = None  # Singleton instance

    @classmethod
    def load_model(cls):
        if cls._model is None:
            logger.info("Loading SentenceTransformer model...")
            cls._model = SentenceTransformer(settings.MODEL_NAME)
            logger.info("Model loaded successfully.")
        return cls._model

    @classmethod
    def generate_embedding(cls, text: str) -> np.ndarray:
        """
        Generate normalized embedding for a single text.
        """
        model = cls.load_model()
        embedding = model.encode(
            text,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embedding

    @classmethod
    def generate_embeddings_batch(cls, texts: list[str]) -> np.ndarray:
        """
        Generate normalized embeddings for multiple texts.
        """
        model = cls.load_model()
        embeddings = model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        return embeddings
