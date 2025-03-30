# MCP Server for Code Understanding

A specialized MCP (Memory Context Provider) server designed to enhance AI agents' understanding of Java Spring Boot projects, particularly for test case design.

## Project Purpose

This MCP Server aims to:
1. Convert user codebases into vector storage for better project comprehension
2. Provide AI agents with long-term memory capabilities
3. Optimize specifically for Java Spring Boot projects

## Key Features

### 1. Update Codebase (updateCodebase)
- **Input**:
  - projectName: Project identifier
  - codebase folder: Complete code directory
- **Process**:
  - Read and parse code
  - Convert to vectors
  - Store in project-specific collection
- **Output**:
  - Success/Failure status

### 2. Query Codebase (readCodeBase)
- **Input**:
  - projectName: Project identifier
  - question: Query text
- **Process**:
  - Convert question to vector
  - Search relevant code in project collection
- **Output**:
  - Top 5 most relevant results with similarity scores

## Technical Stack

- **Embedding**: Google Vertex AI (gemini-embedding-exp-03-07)
- **Vector Storage**: Qdrant
- **Code Parsing**: tree-sitter-languages

## Implementation Plan

### Phase 1: Core Functionality
- [v] Basic project structure setup
- [V] Basic Java file reading
- [v] Tree-sitter code structure parsing
- [v] File splitting logic
- [v] Metadata extraction (methods, classes)

### Phase 2: Vectorization
- [ ] Google Vertex AI integration
- [ ] Embedding generation
- [ ] Vector storage structure

### Phase 3: Storage Layer
- [ ] Qdrant setup
- [ ] Vector storage and retrieval
- [ ] Project isolation mechanism

### Phase 4: API & Integration
- [ ] MCP Server interface
- [ ] Component integration
- [ ] Error handling and logging

### Phase 5: Testing & Optimization
- [ ] Unit testing
- [ ] Integration testing
- [ ] Performance optimization
- [ ] Documentation

## Special Requirements

### Java File Processing
- Chunk by Java file unit
- Split by method when file is too large
- Maintain method relationships

## Environment Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Required environment variables
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
QDRANT_HOST=localhost
QDRANT_PORT=6333
MAX_FILE_SIZE=1000
```

## Project Structure

```
.
├── src/
│   ├── config/         # Configuration management
│   └── services/       # Core services
├── tests/             # Test files
├── test_app/          # Sample Spring Boot app for testing
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Development Status

Currently in Phase 1: Implementing core functionality for Java code parsing and analysis.

## Contributing

This is an internal tool for enhancing AI agent capabilities in understanding and testing Java Spring Boot projects. 