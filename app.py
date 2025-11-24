from fastapi import FastAPI
from pydantic import BaseModel

from ingestion.ingest_service import ingest_repo_service
from generation.generate_service import generate_service

app = FastAPI()

class IngestRequest(BaseModel):
    repo_url: str


class GenerateRequest(BaseModel):
    prompt: str
    repo_url: str | None = None


@app.post("/ingest")
def ingest_api(req: IngestRequest):
    return ingest_repo_service(req.repo_url)


@app.post("/generate_tests")
def generate_api(req: GenerateRequest):
    return generate_service(req.prompt, req.repo_url)
