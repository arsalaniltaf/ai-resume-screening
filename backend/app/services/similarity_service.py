from typing import List
from fastapi import UploadFile
from app.services.parser_service import ResumeParser
from app.services.embedding_service import EmbeddingService
import numpy as np


class SimilarityService:

    @staticmethod
    async def process_ranking(
        job_description: str,
        resume_files: List[UploadFile]
    ):
        # 1️⃣ Extract resume texts
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

        # 5️⃣ Explainability
        SimilarityService.add_keyword_explanations(
            ranked_results,
            job_description,
            resume_texts
        )

        return ranked_results


    @staticmethod
    def compute_similarity(job_embedding, resume_embeddings):
        scores = np.dot(resume_embeddings, job_embedding)
        indices = np.argsort(scores)[::-1]
        return scores, indices


    @staticmethod
    def rank_resumes(filenames, scores, indices):
        return [
            {
                "filename": filenames[i],
                "score": float(scores[i])
            }
            for i in indices
        ]


    @staticmethod
    def add_keyword_explanations(ranked_results, job_description, resume_texts):
        job_words = set(job_description.lower().split())
        job_words = {word for word in job_words if len(word) > 3}

        for i, result in enumerate(ranked_results):
            resume_words = set(resume_texts[i].lower().split())
            matched_keywords = list(job_words.intersection(resume_words))
            result["matched_keywords"] = matched_keywords[:10]
