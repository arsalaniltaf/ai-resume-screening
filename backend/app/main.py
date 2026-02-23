from fastapi import FastAPI
from app.api.routes import router
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI(
    title="AI Resume Screening API",
    description="Ranks resumes based on job description using semantic similarity",
    version="1.0"
)

app.include_router(router)
