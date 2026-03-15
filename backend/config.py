from pathlib import Path

import torch

# Project root: real_estate_ai/
BASE_DIR = Path(__file__).resolve().parent.parent
DATASET_DIR = BASE_DIR / "dataset"
MODELS_DIR = BASE_DIR / "models"
UPLOADS_DIR = BASE_DIR / "uploads"
VECTOR_DB_DIR = BASE_DIR / "vector_db"

CLASSIFIER_PATH = MODELS_DIR / "final-model.pth"
FAISS_INDEX_PATH = VECTOR_DB_DIR / "faiss.index"
FAISS_METADATA_PATH = VECTOR_DB_DIR / "faiss_metadata.json"

# Fallback label order when no class_to_idx metadata is found in checkpoint.
DEFAULT_CLASSES = ["Bathroom", "Bedroom", "Dinning", "Kitchen", "Livingroom"]

# Model versioning and inference thresholds.
MODEL_VERSION = "resnet50_v3_2026-03-14"
EMBEDDING_MODEL_VERSION = "clip_vit_b32_openai"
UNKNOWN_CONFIDENCE_THRESHOLD = 0.6
DUPLICATE_SIMILARITY_THRESHOLD = 0.92

# CLIP embedding dimensions for ViT-B-32.
CLIP_EMBEDDING_DIM = 512

# Apple Silicon friendly device selection.
device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
