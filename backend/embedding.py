from functools import lru_cache
import os
from pathlib import Path

import numpy as np

# Hackathon-safe workaround for OpenMP duplicate runtime aborts on macOS.
os.environ.setdefault("KMP_DUPLICATE_LIB_OK", "TRUE")

import open_clip
import torch
from PIL import Image

from .config import device


@lru_cache(maxsize=1)
def _load_clip_model():
    model, _, preprocess = open_clip.create_model_and_transforms("ViT-B-32", pretrained="openai")
    tokenizer = open_clip.get_tokenizer("ViT-B-32")
    model = model.to(device)
    model.eval()
    return model, preprocess, tokenizer


def generate_embedding(image_path: Path) -> np.ndarray:
    model, preprocess, _ = _load_clip_model()

    image = Image.open(image_path).convert("RGB")
    image_tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        features = model.encode_image(image_tensor)
        features = features / features.norm(dim=-1, keepdim=True)

    embedding = features.squeeze(0).cpu().numpy().astype(np.float32)
    return embedding


def generate_text_embedding(text: str) -> np.ndarray:
    model, _, tokenizer = _load_clip_model()

    tokens = tokenizer([text]).to(device)

    with torch.no_grad():
        features = model.encode_text(tokens)
        features = features / features.norm(dim=-1, keepdim=True)

    embedding = features.squeeze(0).cpu().numpy().astype(np.float32)
    return embedding
