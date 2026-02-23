from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import List
import logging

from app.services.ranking_service import RankingService
from app.models.schemas import RankingResponse

router = APIRouter()
logger = logging.getLogger(__name__)


# -----------------------------
# Health Check Endpoint
# -----------------------------
@router.get("/", tags=["Health"])
def health_check():
    """
    Health check endpoint to verify API status.
    """
    return {"status": "API running successfully"}


# -----------------------------
# Resume Ranking Endpoint
# -----------------------------
@router.post(
    "/rank",
    response_model=RankingResponse,
    tags=["Resume Ranking"]
)
async def rank_resumes(
    job_description: str = Form(..., description="Job description text"),
    resumes: List[UploadFile] = File(..., description="List of resume files")
):
    """
    Ranks uploaded resumes against the provided job description
    using semantic similarity and returns ranked results
    with explainability (matched keywords).
    """
    try:
        logger.info("Received ranking request")
        logger.info(f"Number of resumes uploaded: {len(resumes)}")

        results = await RankingService.rank_resumes(
            job_description=job_description,
            resume_files=resumes
        )

        logger.info("Ranking completed successfully")

        return {"rankings": results}

    except Exception as e:
        logger.exception("Ranking failed due to unexpected error")
        raise HTTPException(
            status_code=500,
            detail="Internal server error during ranking process"
        )
