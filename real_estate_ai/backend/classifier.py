import time
import uuid
from pathlib import Path
from typing import Any, List

import torch
from PIL import Image
from torchvision import models, transforms

from .config import (
    CLASSIFIER_PATH,
    DEFAULT_CLASSES,
    DUPLICATE_SIMILARITY_THRESHOLD,
    EMBEDDING_MODEL_VERSION,
    MODEL_VERSION,
    UNKNOWN_CONFIDENCE_THRESHOLD,
    device,
)


class RoomClassifier:
    def __init__(self, model_path: Path = CLASSIFIER_PATH) -> None:
        self.model_path = model_path
        self.model, self.classes = self._load_model()
        self.transform = transforms.Compose(
            [
                transforms.Resize((224, 224)),
                transforms.ToTensor(),
            ]
        )

    def _load_model(self) -> tuple[torch.nn.Module, List[str]]:
        if not self.model_path.exists():
            raise FileNotFoundError(
                f"Classifier weights not found at {self.model_path}. Run training/train_classifier.py first."
            )

        checkpoint = torch.load(self.model_path, map_location=device)

        if isinstance(checkpoint, dict) and "class_to_idx" in checkpoint:
            class_to_idx = checkpoint["class_to_idx"]
            classes = [None] * len(class_to_idx)
            for class_name, class_idx in class_to_idx.items():
                classes[class_idx] = class_name
            state_dict = checkpoint["state_dict"]
        else:
            classes = DEFAULT_CLASSES
            state_dict = checkpoint

        model = models.resnet50(weights=None)
        model.fc = torch.nn.Linear(model.fc.in_features, len(classes))
        model.load_state_dict(state_dict)
        model.to(device)
        model.eval()

        return model, classes

    def classify_image(self, image_path: Path) -> dict[str, Any]:
        request_id = str(uuid.uuid4())
        start_total = time.time()

        # Classification stage timing
        start_cls = time.time()
        
        image = Image.open(image_path).convert("RGB")
        image_tensor = self.transform(image).unsqueeze(0).to(device)

        with torch.no_grad():
            logits = self.model(image_tensor)
            probabilities = torch.softmax(logits, dim=1)

        latency_cls = (time.time() - start_cls) * 1000

        confidence, predicted = torch.max(probabilities, 1)
        confidence = confidence.item()
        predicted_idx = predicted.item()

        room_type = self.classes[predicted_idx]

        # Top-3 predictions
        top_k = min(3, len(self.classes))
        top_probs, top_indices = torch.topk(probabilities, k=top_k, dim=1)

        top_predictions = [
            {
                "room_type": self.classes[idx.item()],
                "confidence": prob.item(),
            }
            for prob, idx in zip(top_probs[0], top_indices[0])
        ]

        is_unknown = confidence < UNKNOWN_CONFIDENCE_THRESHOLD

        latency_total = (time.time() - start_total) * 1000

        return {
            "request_id": request_id,
            "prediction": {
                "room_type": room_type,
                "confidence": confidence,
                "top_predictions": top_predictions,
                "is_unknown": is_unknown,
            },
            "model_info": {
                "model_version": MODEL_VERSION,
                "embedding_model_version": EMBEDDING_MODEL_VERSION,
                "metadata_provider": "gemini",
            },
            "latency": {
                "latency_ms_total": latency_total,
                "latency_ms_classification": latency_cls,
            },
            "thresholds_used": {
                "unknown_threshold": UNKNOWN_CONFIDENCE_THRESHOLD,
                "duplicate_threshold": DUPLICATE_SIMILARITY_THRESHOLD,
            },
            "input_info": {
                "image_size": list(image_tensor.shape),
                "mime_type": "image/jpeg",
            },
        }
