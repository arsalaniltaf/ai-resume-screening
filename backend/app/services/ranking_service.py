from typing import List
from fastapi import UploadFile
import logging

from app.services.parser_service import ResumeParser
from app.services.embedding_service import EmbeddingService
from app.services.similarity_service import SimilarityService

logger = logging.getLogger(__name__)


class RankingService:
    """
    Handles full ranking pipeline:
    - Parsing resumes
    - Generating embeddings
    - Computing similarity
    - Sorting results
    - Adding explainability
    """

    @staticmethod
    async def rank_resumes(
        job_description: str,
        resume_files: List[UploadFile]
    ):
        try:
            logger.info("Starting ranking pipeline")

            # 1️⃣ Parse resumes
            resume_texts = []
            filenames = []

            for resume in resume_files:
                text = await ResumeParser.extract_text(resume)
                resume_texts.append(text)
                filenames.append(resume.filename)

            # 2️⃣ Generate embeddings
            job_embedding = EmbeddingService.generate_embedding(job_description)
            resume_embeddings = EmbeddingService.generate_embeddings_batch(resume_texts)

            # 3️⃣ Compute similarity
            scores, indices = SimilarityService.compute_similarity(
                job_embedding,
                resume_embeddings
            )

            # 4️⃣ Rank resumes
            ranked_results = SimilarityService.rank_resumes(
                filenames,
                scores,
                indices
            )

            # 5️⃣ Add explainability
            RankingService._add_keyword_explanations(
                ranked_results,
                job_description,
                resume_texts
            )

            logger.info("Ranking pipeline completed successfully")

            return ranked_results

        except Exception as e:
            logger.exception("Ranking pipeline failed")
            raise e


    @staticmethod
    def _add_keyword_explanations(
        ranked_results,
        job_description,
        resume_texts
    ):
        job_words = set(job_description.lower().split())
        job_words = {word for word in job_words if len(word) > 3}

        for i, result in enumerate(ranked_results):
            resume_words = set(resume_texts[i].lower().split())
            matched_keywords = list(job_words.intersection(resume_words))
            result["matched_keywords"] = matched_keywords[:10]
