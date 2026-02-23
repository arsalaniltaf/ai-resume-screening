from sentence_transformers import SentenceTransformer
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class EmbeddingModel:
    _model = None

    @classmethod
    def load_model(cls):
        if cls._model is None:
            logger.info("Loading SentenceTransformer model...")
            cls._model = SentenceTransformer(settings.MODEL_NAME)
            logger.info("Model loaded successfully.")
        return cls._model
