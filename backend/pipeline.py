import logging
import time
from pathlib import Path

from .classifier import RoomClassifier
from .config import DUPLICATE_SIMILARITY_THRESHOLD
from .duplicate_detector import is_duplicate_score
from .embedding import generate_embedding, generate_text_embedding
from .metadata_extractor import MetadataExtractor
from .vector_store import VectorStore
from .database import insert_listing, get_listings_by_faiss_ids, get_all_listings

logger = logging.getLogger(__name__)


class AIPipeline:
    def __init__(self) -> None:
        self.classifier = RoomClassifier()
        self.metadata_extractor = MetadataExtractor()
        self.vector_store = VectorStore()

    def process_image(self, image_path: Path, filename: str, broker_data: dict = None) -> dict:
        logger.info("Starting pipeline for %s", filename)
        if broker_data is None:
            broker_data = {}

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
        faiss_id = self.vector_store.add_embedding(
            embedding=embedding,
            metadata={
                "filename": filename,
                "room_type": room_type,
                "confidence": confidence,
                "metadata": metadata,
            },
        )
        logger.info("Stored embedding for %s with faiss_id %s", filename, faiss_id)

        # Merge UI logic & AI metadata into SQLite
        record_data = {
            "faiss_id": faiss_id,
            "title": broker_data.get("title", ""),
            "location": broker_data.get("location", ""),
            "price": broker_data.get("price", 0.0),
            "category": broker_data.get("category", ""),
            "bedrooms": broker_data.get("bedrooms", 0),
            "guests": broker_data.get("guests", 0),
            "image_filename": filename,
            "ai_room_type": metadata.get("room_type", ""),
            "ai_design_style": metadata.get("design_style", ""),
            "ai_lighting": metadata.get("lighting", ""),
            "ai_features": metadata.get("features", []),
            "ai_objects": metadata.get("objects", [])
        }
        
        sqlite_id = insert_listing(record_data)
        logger.info("Stored SQLite listing for %s with id %s", filename, sqlite_id)

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

        if not matches:
            return {"query": query, "results": []}

        # Merge FAISS scores into SQLite listings
        faiss_ids = [m["id"] for m in matches]
        listings = get_listings_by_faiss_ids(faiss_ids)

        results = []
        for match in matches:
            # Find the corresponding sqlite listing
            listing = next((l for l in listings if l["faiss_id"] == match["id"]), None)
            if listing:
                # Add score so frontend can show match percentage if desired
                listing["score"] = match["score"]
                # Create the full image URL assuming standard mount locally
                listing["imageUrl"] = f"http://127.0.0.1:8000/uploads/{listing['image_filename']}"
                results.append(listing)

        return {
            "query": query,
            "results": results,
        }

    def get_all_listings(self) -> dict:
        listings = get_all_listings()
        for listing in listings:
            listing["imageUrl"] = f"http://127.0.0.1:8000/uploads/{listing['image_filename']}"
        return {"listings": listings}

    def vector_stats(self) -> dict:
        return self.vector_store.get_stats()

    def vector_records(self, limit: int = 10) -> dict:
        return {
            "records": self.vector_store.get_records(limit=limit),
        }
