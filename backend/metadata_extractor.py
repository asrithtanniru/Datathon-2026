import json
import importlib
import logging
import os
from pathlib import Path
from typing import Any

from PIL import Image
import requests

logger = logging.getLogger(__name__)

dotenv_module = importlib.util.find_spec("dotenv")
if dotenv_module:
    dotenv = importlib.import_module("dotenv")
    dotenv.load_dotenv()


class MetadataExtractor:
    def __init__(self) -> None:
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3-flash-preview")
        self.provider = (os.getenv("METADATA_PROVIDER") or "auto").strip().lower()

    def extract_metadata(self, image_path: Path, predicted_room_type: str) -> dict[str, Any]:
        provider_order = self._resolve_provider_order()

        for provider in provider_order:
            if provider == "gemini":
                metadata = self._extract_with_gemini(image_path=image_path, predicted_room_type=predicted_room_type)
                if metadata:
                    return metadata

            if provider == "openai":
                metadata = self._extract_with_openai(image_path=image_path, predicted_room_type=predicted_room_type)
                if metadata:
                    return metadata

        logger.info("No metadata provider succeeded; using heuristic metadata fallback")
        return self._heuristic_metadata(image_path=image_path, predicted_room_type=predicted_room_type)

    def _resolve_provider_order(self) -> list[str]:
        if self.provider in {"openai", "gemini"}:
            return [self.provider]

        # auto: prefer Gemini if configured, then OpenAI.
        provider_order: list[str] = []
        if self.gemini_api_key:
            provider_order.append("gemini")
        if self.openai_api_key:
            provider_order.append("openai")
        return provider_order

    def _extract_with_openai(self, image_path: Path, predicted_room_type: str) -> dict[str, Any] | None:
        if not self.openai_api_key:
            return None

        openai_spec = importlib.util.find_spec("openai")
        if not openai_spec:
            logger.warning("OpenAI package is not installed")
            return None

        openai_module = importlib.import_module("openai")
        OpenAI = getattr(openai_module, "OpenAI")

        client = OpenAI(api_key=self.openai_api_key)

        with image_path.open("rb") as f:
            image_bytes = f.read()

        prompt = (
            "Analyze this interior house image. Return valid JSON only with keys: "
            "room_type, design_style, lighting, spatial_layout, features, objects. "
            "Design style examples: modern, traditional, luxury, minimalist. "
            "Lighting examples: natural, artificial, dim, bright. "
            "Spatial layout examples: open plan, compact, spacious."
        )

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "input_text", "text": prompt},
                            {
                                "type": "input_image",
                                "image_url": f"data:image/jpeg;base64,{self._to_base64(image_bytes)}",
                            },
                        ],
                    }
                ],
            )
        except Exception as exc:
            logger.warning("OpenAI metadata API failed (%s)", exc)
            return None

        raw_text = (response.output_text or "").strip()
        if not raw_text:
            logger.warning("OpenAI metadata API returned empty text")
            return None

        parsed = self._parse_json_text(raw_text)
        if not parsed:
            logger.warning("OpenAI metadata API returned non-JSON output")
            return None

        return self._sanitize_metadata(parsed, predicted_room_type)

    def _extract_with_gemini(self, image_path: Path, predicted_room_type: str) -> dict[str, Any] | None:
        if not self.gemini_api_key:
            return None

        with image_path.open("rb") as f:
            image_bytes = f.read()

        prompt = (
            "Analyze this interior house image. Return valid JSON only with keys: "
            "room_type, design_style, lighting, spatial_layout, features, objects. "
            "Design style examples: modern, traditional, luxury, minimalist. "
            "Lighting examples: natural, artificial, dim, bright. "
            "Spatial layout examples: open plan, compact, spacious."
        )

        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.gemini_model}:generateContent"
        )

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": "image/jpeg",
                                "data": self._to_base64(image_bytes),
                            }
                        },
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.1,
                "response_mime_type": "application/json",
            },
        }

        try:
            response = requests.post(endpoint, params={"key": self.gemini_api_key}, json=payload, timeout=30)
        except Exception as exc:
            logger.warning("Gemini metadata API request failed (%s)", type(exc).__name__)
            return None

        if response.status_code >= 400:
            logger.warning("Gemini metadata API returned status %s", response.status_code)
            return None

        try:
            data = response.json()
        except Exception:
            logger.warning("Gemini metadata API returned non-JSON response")
            return None

        try:
            raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except (KeyError, IndexError, TypeError):
            logger.warning("Gemini metadata API returned unexpected shape")
            return None

        parsed = self._parse_json_text(raw_text)
        if not parsed:
            logger.warning("Gemini metadata API returned non-JSON output")
            return None

        return self._sanitize_metadata(parsed, predicted_room_type)

    def _heuristic_metadata(self, image_path: Path, predicted_room_type: str) -> dict[str, Any]:
        width, height = Image.open(image_path).convert("RGB").size
        spatial_layout = "spacious" if (width * height) > 900000 else "compact"

        return {
            "room_type": predicted_room_type,
            "design_style": "unknown",
            "lighting": "unknown",
            "spatial_layout": spatial_layout,
            "features": [],
            "objects": [],
        }

    @staticmethod
    def _sanitize_metadata(metadata: dict[str, Any], fallback_room_type: str) -> dict[str, Any]:
        return {
            "room_type": str(metadata.get("room_type") or fallback_room_type),
            "design_style": str(metadata.get("design_style") or "unknown"),
            "lighting": str(metadata.get("lighting") or "unknown"),
            "spatial_layout": str(metadata.get("spatial_layout") or "unknown"),
            "features": list(metadata.get("features") or []),
            "objects": list(metadata.get("objects") or []),
        }

    @staticmethod
    def _to_base64(data: bytes) -> str:
        import base64

        return base64.b64encode(data).decode("utf-8")

    @staticmethod
    def _parse_json_text(raw_text: str) -> dict[str, Any] | None:
        cleaned = raw_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
            cleaned = cleaned.strip()

        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            return None

        if not isinstance(parsed, dict):
            return None
        return parsed
