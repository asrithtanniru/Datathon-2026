# Real Estate AI (Hackathon Prototype)

AI real estate image backend with room classification, metadata extraction, duplicate detection, and semantic search.

## Features

- Room classification using fine-tuned ResNet50
- Confidence score with unknown-class fallback (`confidence < 0.55 -> unknown`)
- CLIP (`ViT-B-32`) image and text embeddings via `open_clip_torch`
- Metadata extraction module (`backend/metadata_extractor.py`)
- FAISS vector database for embedding storage and nearest-neighbor search
- Duplicate detection from vector similarity (`score > 0.92`)
- Semantic search endpoint (`POST /search`)
- Apple Silicon support with PyTorch MPS fallback

## Project Structure

```text
real_estate_ai/
  backend/
    main.py
    classifier.py
    embedding.py
    metadata_extractor.py
    vector_store.py
    duplicate_detector.py
    pipeline.py
    config.py
  training/
    train_classifier.py
    prepare_dataset.py
    download_kaggle_subset.py
  models/
  dataset/
  raw_images/
  uploads/
  vector_db/
  scripts/
  .gitignore
  .env.example
  requirements.txt
  README.md
```

## Setup

Use virtual environment (recommended):

```bash
cd real_estate_ai
./scripts/setup.sh
```

Or manually:

```bash
cd real_estate_ai
pip install -r requirements.txt
```

## Optional API Key Setup

Copy `.env.example` to `.env` and set key:

```text
OPENAI_API_KEY=
GEMINI_API_KEY=
METADATA_PROVIDER=auto
```

Provider options:

- `METADATA_PROVIDER=auto`: try Gemini first (if key exists), then OpenAI
- `METADATA_PROVIDER=gemini`: use only Gemini
- `METADATA_PROVIDER=openai`: use only OpenAI

If neither provider key is set, metadata extraction uses a local heuristic fallback.

## Data Preparation

Option A: add your own images into `raw_images/` (flat naming: `bath_1.jpg`, `bedroom_2.jpg`, etc.)

Option B: auto-download balanced subset from Kaggle:

```bash
./scripts/download_subset.sh 120
```

Prepare dataset folders:

```bash
./scripts/prepare_dataset.sh
```

## Train Classifier

```bash
./scripts/train.sh 4 8
```

Output checkpoint:

`models/room_classifier.pth`

## Run API

```bash
./scripts/start_api.sh
```

## API Endpoints

### Health

```bash
curl -s http://127.0.0.1:8000/health
```

### Upload + Analyze

```bash
curl -s -X POST -F "file=@test.jpg" http://127.0.0.1:8000/upload
```

Example response:

```json
{
  "filename": "bedroom_0001.jpg",
  "room_type": "bedroom",
  "confidence": 0.87,
  "duplicate": false,
  "similarity_score": 0.41,
  "metadata": {
    "room_type": "bedroom",
    "design_style": "modern",
    "lighting": "natural",
    "spatial_layout": "spacious",
    "features": ["large window"],
    "objects": ["bed", "lamp"]
  },
  "top_predictions": [
    {"label": "bedroom", "confidence": 0.87},
    {"label": "living_room", "confidence": 0.08},
    {"label": "bathroom", "confidence": 0.03}
  ]
}
```

### Semantic Search

```bash
curl -s -X POST http://127.0.0.1:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "bright bedroom with balcony", "top_k": 3}'
```

Example response:

```json
{
  "query": "bright bedroom with balcony",
  "results": [
    {
      "score": 0.82,
      "filename": "bedroom_0010.jpg",
      "room_type": "bedroom",
      "confidence": 0.91,
      "metadata": {
        "design_style": "modern",
        "lighting": "bright",
        "spatial_layout": "spacious",
        "features": ["balcony", "large window"],
        "objects": ["bed", "wardrobe"]
      }
    }
  ]
}
```

### Vector DB Inspection (No Container Needed)

The vector DB is local FAISS + JSON metadata in `vector_db/`.

```bash
curl -s http://127.0.0.1:8000/vector/stats
curl -s -X POST http://127.0.0.1:8000/vector/records -H "Content-Type: application/json" -d '{"limit": 5}'
```

## Current Pipeline Order

`classify_image -> confidence/unknown -> extract_metadata -> generate_clip_embedding -> search_vector_db -> duplicate_detection -> store_embedding`

## Git Workflow (Team)

Branch strategy:

- `main`: stable demo version
- `dev`: integration branch
- `feature/*`: individual development

Example:

```bash
git checkout -b feature/metadata-agent
git add .
git commit -m "add metadata extraction agent"
git push origin feature/metadata-agent
```

Then open PR into `dev`; after testing, merge `dev` into `main`.

## Team Development Guidelines

1. Clone repository.
2. Install dependencies (`./scripts/setup.sh`).
3. Create `.env` for API keys if needed.
4. Run backend (`./scripts/start_api.sh`).

## What to Push

Push:

- `backend/`
- `training/`
- `requirements.txt`
- `README.md`

Do not push:

- `dataset/`
- `uploads/`
- `models/`
- `vector_db/`
