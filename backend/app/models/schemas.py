from pydantic import BaseModel, Field
from typing import List


class RankedResume(BaseModel):
    filename: str = Field(..., example="resume_john.pdf")
    score: float = Field(..., example=0.87)
    matched_keywords: List[str] = Field(
        default_factory=list,
        example=["python", "machine learning", "docker"]
    )


class RankingResponse(BaseModel):
    rankings: List[RankedResume]
