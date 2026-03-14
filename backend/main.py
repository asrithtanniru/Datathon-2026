import logging
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from .config import UPLOADS_DIR
from .pipeline import AIPipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="VisionEstate", version="0.1.0")

UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
pipeline = AIPipeline()


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


class VectorRecordsRequest(BaseModel):
    limit: int = 10


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)) -> dict:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Missing filename")

    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image uploads are supported")

    destination = Path(UPLOADS_DIR) / Path(file.filename).name
    file_bytes = await file.read()
    destination.write_bytes(file_bytes)
    logger.info("Saved upload: %s", destination.name)

    result = pipeline.process_image(destination, destination.name)

    return {
        "request_id": result["request_id"],
        "filename": result["filename"],
        "prediction": result["prediction"],
        "model_info": result["model_info"],
        "latency": result["latency"],
        "thresholds_used": result["thresholds_used"],
        "input_info": result["input_info"],
        "duplicate": result["duplicate"],
        "similarity_score": result["similarity_score"],
        "metadata": result["metadata"],
        "top_predictions": result["top_predictions"],
    }


@app.post("/search")
def semantic_search(payload: SearchRequest) -> dict:
    if not payload.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    return pipeline.search_by_text(query=payload.query.strip(), top_k=payload.top_k)


@app.get("/vector/stats")
def vector_stats() -> dict:
    return pipeline.vector_stats()


@app.post("/vector/records")
def vector_records(payload: VectorRecordsRequest) -> dict:
    return pipeline.vector_records(limit=payload.limit)
