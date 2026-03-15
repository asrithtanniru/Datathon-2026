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

    try:
        result = pipeline.process_image(destination, destination.name)
    except ValueError as e:
        if destination.exists():
            destination.unlink()
        
        error_msg = str(e)
        if error_msg.startswith("unknown_image_irrelevant"):
            score = error_msg.split("|")[1]
            raise HTTPException(
                status_code=400,
                detail=f"Irrelevant image detected (score: {score}). We only accept valid real estate room images."
            )
        elif error_msg.startswith("duplicate_image_fraud"):
            score = error_msg.split("|")[1]
            raise HTTPException(
                status_code=409,
                detail=f"You have uploaded the same image. Don't try to fraud, we have a detection system! (Similarity: {score})"
            )
        elif error_msg.startswith("unsupported_room_type"):
            raise HTTPException(
                status_code=400,
                detail="This image is not yet supported. Our system only supports standard indoor rooms."
            )
        else:
            raise HTTPException(status_code=500, detail=str(e))

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
