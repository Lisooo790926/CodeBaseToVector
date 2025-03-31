# Codebase MCP

A Python-based server for managing and interacting with codebase tools.

## Installation

The project uses `uv` for package management. To install dependencies:

```bash
uv venv
. .venv/bin/activate
uv sync
```

## Development

To run the server:

```bash
python -m codebase_mcp
```

## Docker

To build and run using Docker:

```bash
docker build -t codebase-mcp .
docker run -it codebase-mcp
```

## Project Purpose

This MCP Server aims to:
1. Convert user codebases into vector storage for better project comprehension
2. Provide AI agents with long-term memory capabilities
3. Optimize specifically for Java Spring Boot projects

## Key Features

### 1. Update Codebase (updateCodebase)
- **Input**:
  - `project_name`: Project identifier
  - `codebase_path`: Path to the Java codebase directory
- **Process**:
  - Read and parse Java code
  - Convert to vectors using Google Vertex AI embeddings
  - Store in project-specific Qdrant collection
- **Output**:
  - Success/Failure status with message

### 2. Query Codebase (readCodeBase)
- **Input**:
  - `project_name`: Project identifier
  - `question`: Natural language query
- **Process**:
  - Convert question to vector
  - Search relevant code in project collection
- **Output**:
  - Top 5 most relevant results with:
    - File path
    - Code type (class/method)
    - Class name (if applicable)
    - Method name (if applicable)
    - Code content
    - Similarity score

## Technical Stack

- **Package Management**: uv (fast Python package installer)
- **Embedding**: Google Vertex AI (gemini-embedding-exp-03-07)
- **Vector Storage**: Qdrant
- **Code Parsing**: tree-sitter-languages

## Implementation Status

### Phase 1: Core Functionality ✅
- [x] Basic project structure setup
- [x] Basic Java file reading
- [x] Tree-sitter code structure parsing
- [x] File splitting logic
- [x] Metadata extraction (methods, classes)

### Phase 2: Vectorization ✅
- [x] Embedding generation
- [x] Vector storage structure

### Phase 3: Storage Layer ✅
- [x] Qdrant setup
- [x] Vector storage and retrieval
- [x] Project isolation mechanism

### Phase 4: MCP Server ✅
- [x] MCP Server interface
- [x] Component integration
- [x] Error handling and logging

### Phase 5: Testing & Optimization 🚧
- [x] Unit testing
- [ ] Integration testing
- [ ] Performance optimization
- [x] Documentation

## Environment Setup

### Using uv (Recommended)

1. Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Create a new virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Install dependencies using uv
uv sync
```

3. Set required environment variables:
```bash
export GOOGLE_API_KEY=xxxxxxx
export QDRANT_HOST=localhost
export QDRANT_PORT=6333
```

### Using Docker

Build and run using Docker Compose:
```bash
docker compose up --build
```

## Running the Server

### Using uv
```bash
# Activate virtual environment if not already activated
source .venv/bin/activate  # On Unix/macOS
# or
.venv\Scripts\activate  # On Windows

# Start the server
./run_mcp_server.py
```

### Using Docker
```bash
docker compose up
```

## Example RPC Calls

### 1. List Available Tools
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tool/list",
  "params": {}
}
```

Expected Response:
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "updateCodebase",
        "description": "Convert user codebases into vector storage for better project comprehension",
        "inputSchema": {
          "type": "object",
          "properties": {
            "project_name": {"type": "string"},
            "codebase_path": {"type": "string"}
          },
          "required": ["project_name", "codebase_path"]
        }
      },
      {
        "name": "readCodeBase",
        "description": "Query the codebase with a question to get relevant code snippets",
        "inputSchema": {
          "type": "object",
          "properties": {
            "project_name": {"type": "string"},
            "question": {"type": "string"}
          },
          "required": ["project_name", "question"]
        }
      }
    ]
  }
}
```

### 2. Update Codebase
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tool/call",
  "params": {
    "name": "updateCodebase",
    "arguments": {
      "project_name": "my-spring-project",
      "codebase_path": "/path/to/java/project"
    }
  }
}
```

### 3. Query Codebase
```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tool/call",
  "params": {
    "name": "readCodeBase",
    "arguments": {
      "project_name": "my-spring-project",
      "question": "How is user authentication implemented?"
    }
  }
}
```

## Project Structure

```
.
├── src/
│   ├── config/         # Configuration management
│   ├── services/       # Core services
│   │   ├── code_parser.py      # Java code parsing
│   │   ├── vector_embedding.py # Embedding generation
│   │   ├── vector_storage.py   # Qdrant operations
│   │   └── codebase_service.py # Main service
│   ├── server/         # MCP server implementation
│   └── type_definitions/ # Type definitions
├── tests/             # Test files
├── pyproject.toml     # Project configuration and dependencies
├── uv.lock           # Dependency lock file
└── README.md         # This file
```

## Development

### Setting up Development Environment

1. Install development dependencies:
```bash
uv sync --dev
```

2. Run tests:
```bash
pytest
```

3. Format code:
```bash
ruff format .
```

4. Lint code:
```bash
ruff check .
```

## Contributing

This is an internal tool for enhancing AI agent capabilities in understanding and testing Java Spring Boot projects.

## Testing the Server

1. Start the server:
```bash
./run_mcp_server.py
```

2. In another terminal, you can use `nc` to send RPC calls:
```bash
nc localhost 3000
```

3. Then paste the JSON RPC calls shown above to test the server.

Note: The server uses stdio for communication, so you'll need to send the JSON requests line by line without formatting. 