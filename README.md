
# Vision Estate- A Real Estate AI Platform

A hackathon prototype for AI-powered real estate image analysis, featuring room classification, metadata extraction, duplicate detection, semantic search, and a modern web interface.

---

## Objectives

- **Automate room classification** from real estate images using deep learning.
- **Extract rich metadata** (room type, design style, features, objects) from images using LLMs and heuristics.
- **Enable semantic search** for property images based on text queries.
- **Detect duplicates** to ensure unique listings.
- **Provide a modern web interface** for browsing and searching properties.

---

## How the Project Works

### 1. User Interaction
- Users can upload property images or perform semantic searches via the web frontend.

### 2. Backend Processing
- The backend (Python FastAPI) receives requests and processes them as follows:

#### **Image Upload Flow**
1. **Classify Image:** Uses a fine-tuned ResNet50 model to predict room type.
2. **Confidence Check:** If confidence is low, fallback to 'unknown'.
3. **Metadata Extraction:** Uses LLMs (OpenAI/Gemini) or heuristics to extract metadata.
4. **Generate Embedding:** CLIP (ViT-B-32) model generates image/text embeddings.
5. **Vector Search:** FAISS vector DB is searched for similar images.
6. **Duplicate Detection:** Checks for duplicates based on similarity score.
7. **Store Embedding:** Saves embedding and metadata for future search.
8. **Return Result:** Sends analysis result to frontend.

#### **Semantic Search Flow**
1. **Generate Query Embedding:** CLIP model converts text query to embedding.
2. **Vector Search:** FAISS DB is searched for top matches.
3. **Return Matches:** Sends results to frontend.

### 3. Frontend Display
- The Next.js web app displays analysis results, search matches, and property listings.

---


## Flowchart (ASCII)

```
      +-----------------------------+
      | User uploads image/searches |
      +-----------------------------+
            |
            v
      +-----------------------------+
      | Backend API receives request |
      +-----------------------------+
            |
            v
      +-----------------------------+
      |      Request type?           |
      +-----------------------------+
      /                 \
     /                   \
   [Upload]                  [Search]
   |                         |
   v                         v
 +-------------------+   +-------------------+
 | Classify image    |   | Generate query    |
 +-------------------+   | embedding         |
   |               |   +-------------------+
   v               |           |
 +-------------------+           v
 | Confidence check  |   +-------------------+
 +-------------------+   | Search vector DB  |
   |               |   +-------------------+
   v               |           |
 +-------------------+           v
 | Extract metadata  |   +-------------------+
 +-------------------+   | Return top matches|
   |               |   +-------------------+
   v               |           |
 +-------------------+           |
 | Generate embedding|           |
 +-------------------+           |
   |               |           |
   v               |           |
 +-------------------+           |
 | Search vector DB  |           |
 +-------------------+           |
   |               |           |
   v               |           |
 +-------------------+           |
 | Duplicate detect  |           |
 +-------------------+           |
   |               |           |
   v               |           |
 +-------------------+           |
 | Store embedding   |           |
 +-------------------+           |
   |               |           |
   v               |           |
 +-------------------+           |
 | Return result     |<----------+
 +-------------------+
   |
   v
 +-------------------+
 | Frontend displays |
 | result           |
 +-------------------+
```

---

## Project Structure

```
backend/         # Python FastAPI backend for image analysis and search
training/        # Scripts for dataset prep and model training
models/          # Model checkpoints and notebooks
scripts/         # Shell scripts for setup, training, and API management
web-app/         # Next.js frontend for property listings and search
requirements.txt # Python dependencies
README.md        # Project documentation
```

---

## Setup

### Backend

1. **Create a virtual environment (recommended):**
  ```bash
  cd backend
  ./../scripts/setup.sh
  ```
  Or manually:
  ```bash
  pip install -r ../requirements.txt
  ```

2. **API Key Setup (Optional):**
  - Copy `.env.example` to `.env` and set keys for OpenAI/Gemini.
  - `METADATA_PROVIDER` options: `auto`, `gemini`, `openai`.

3. **Data Preparation:**
  - Add images to `raw_images/` or run:
    ```bash
    ./../scripts/download_subset.sh 120
    ./../scripts/prepare_dataset.sh
    ```

4. **Train Classifier:**
  ```bash
  ./../scripts/train.sh 4 8
  ```
  - Output: `models/room_classifier.pth`

5. **Run API:**
  ```bash
  ./../scripts/start_api.sh
  ```

### Web Frontend

1. **Install dependencies:**
  ```bash
  cd web-app
  npm install
  ```

2. **Start development server:**
  ```bash
  npm run dev
  ```
  - Open [http://localhost:3000](http://localhost:3000)

---

## API Endpoints

- **Health:** `GET /health`
- **Upload & Analyze:** `POST /upload` (multipart image)
- **Semantic Search:** `POST /search` (JSON query)
- **Vector DB Stats:** `GET /vector/stats`, `POST /vector/records`

---

## Example Usage

- Upload image:
  ```bash
  curl -X POST -F "file=@test.jpg" http://127.0.0.1:8000/upload
  ```
- Semantic search:
  ```bash
  curl -X POST http://127.0.0.1:8000/search -H "Content-Type: application/json" -d '{"query": "bright bedroom with balcony", "top_k": 3}'
  ```

---

## Development Workflow

- Branch strategy: `main` (stable), `dev` (integration), `feature/*` (individual features).
- Push only code/scripts, not datasets, uploads, models, or vector DB.

---

## Team Guidelines

1. Clone repo.
2. Install dependencies.
3. Set up `.env` if needed.
4. Run backend and web-app.

---

## License

This project is for hackathon/demo purposes.

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


