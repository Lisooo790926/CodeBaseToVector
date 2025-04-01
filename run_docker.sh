#!/bin/bash

# Create network if it doesn't exist
docker network create mcp_network 2>/dev/null || true

# Run Qdrant container
docker run -d --name qdrant \
  --network mcp_network \
  -p 6333:6333 \
  -p 6334:6334 \
  qdrant/qdrant:latest

# Wait for Qdrant to start
sleep 5

# Run codebase-mcp container
docker run -d --name codebase-mcp \
  --network mcp_network \
  -p 3000:3000 \
  -e QDRANT_HOST=qdrant \
  -e QDRANT_PORT=6333 \
  -e GOOGLE_API_KEY=${GOOGLE_API_KEY} \
  codebase-mcp

# Wait for server to start
sleep 5

# Test RPC connection
python test_rpc.py 