# Vector API Router

This project implements a vector-based API router using Qdrant for vector storage and Google's Generative AI for embeddings.

## Setup

1. Set up virtual environment:

Option 1: Using setup script (recommended)
```bash
chmod +x setup.sh
./setup.sh
```

Option 2: Manual setup
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

2. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your Google API key to `.env`

3. Start Vector Storage (Qdrant):

Option 1: Using Docker Compose (recommended)
```bash
# Start Qdrant
docker-compose up -d

# Stop Qdrant
docker-compose down

# View logs
docker-compose logs -f
```

Option 2: Using Docker directly
```bash
docker run -p 6333:6333 qdrant/qdrant
```

4. Place your API specifications in the `api_specs` directory as YAML files.

## Usage

```python
from vector_store import VectorApiRouter

router = VectorApiRouter(api_specs_dir="api_specs")
matching_route = router.find_route("How do I create a new user?")
```

## Development

To deactivate the virtual environment when you're done:
```bash
deactivate
```

## Vector Storage Management

Qdrant is accessible at:
- REST API: http://localhost:6333
- GRPC: localhost:6334

The vector storage data is persisted in a Docker volume named `qdrant_storage`. 