import logging
import time
from pathlib import Path

from .classifier import RoomClassifier
from .config import DUPLICATE_SIMILARITY_THRESHOLD
from .duplicate_detector import is_duplicate_score
from .embedding import generate_embedding, generate_text_embedding
from .metadata_extractor import MetadataExtractor
from .vector_store import VectorStore

logger = logging.getLogger(__name__)


class AIPipeline:
    def __init__(self) -> None:
        self.classifier = RoomClassifier()
        self.metadata_extractor = MetadataExtractor()
        self.vector_store = VectorStore()

    def process_image(self, image_path: Path, filename: str) -> dict:
        logger.info("Starting pipeline for %s", filename)

        # Run classification with built-in latency tracking
        classification_result = self.classifier.classify_image(image_path)
        request_id = classification_result["request_id"]
        prediction = classification_result["prediction"]
        model_info = classification_result["model_info"]
        latencies = classification_result["latency"]
        thresholds_used = classification_result["thresholds_used"]
        input_info = classification_result["input_info"]

        room_type = prediction["room_type"]
        confidence = prediction["confidence"]
        is_unknown = prediction["is_unknown"]
        top_predictions = prediction["top_predictions"]
        
        logger.info("Classification complete: %s (%.4f)", room_type, confidence)

        if is_unknown:
            raise ValueError(f"unknown_image_irrelevant|{confidence:.4f}")

        # Image embedding with timing
        start_embedding = time.time()
        embedding = generate_embedding(image_path)
        latencies["latency_ms_embedding"] = (time.time() - start_embedding) * 1000
        logger.info("Image embedding generated for %s", filename)

        # Duplicate check with timing
        start_vector_search = time.time()
        nearest = self.vector_store.search_embedding(embedding, top_k=1)
        top_score = nearest[0]["score"] if nearest else 0.0
        latencies["latency_ms_vector_search"] = (time.time() - start_vector_search) * 1000
        
        duplicate = is_duplicate_score(top_score, threshold=DUPLICATE_SIMILARITY_THRESHOLD)
        logger.info("Duplicate check score=%.4f duplicate=%s", top_score, duplicate)

        if duplicate:
            raise ValueError(f"duplicate_image_fraud|{top_score:.4f}")

        # Metadata extraction with timing
        start_metadata = time.time()
        metadata = self.metadata_extractor.extract_metadata(
            image_path=image_path, predicted_room_type=room_type
        )
        latencies["latency_ms_metadata"] = (time.time() - start_metadata) * 1000
        logger.info("Metadata extraction complete for %s", filename)

        # Check if the AI decided it was an unsupported room
        if metadata and str(metadata.get("room_type", "")).lower().startswith("other"):
            actual_type = metadata.get("room_type", "other")
            raise ValueError(f"unsupported_room_type|{actual_type}")

        # Store since not duplicate
        self.vector_store.add_embedding(
            embedding=embedding,
            metadata={
                "filename": filename,
                "room_type": room_type,
                "confidence": confidence,
                "metadata": metadata,
            },
        )
        logger.info("Stored embedding for %s", filename)

        return {
            "request_id": request_id,
            "filename": filename,
            "prediction": prediction,
            "model_info": model_info,
            "latency": latencies,
            "thresholds_used": thresholds_used,
            "input_info": input_info,
            "duplicate": duplicate,
            "similarity_score": top_score,
            "metadata": metadata,
            "top_predictions": top_predictions,
        }

    def search_by_text(self, query: str, top_k: int = 5) -> dict:
        logger.info("Running semantic search for query: %s", query)
        query_embedding = generate_text_embedding(query)
        matches = self.vector_store.search_embedding(query_embedding, top_k=top_k)

        results = []
        for match in matches:
            result = {
                "score": match["score"],
                **(match.get("metadata") or {}),
            }
            results.append(result)

        return {
            "query": query,
            "results": results,
        }

    def vector_stats(self) -> dict:
        return self.vector_store.get_stats()

    def vector_records(self, limit: int = 10) -> dict:
        return {
            "records": self.vector_store.get_records(limit=limit),
        }
