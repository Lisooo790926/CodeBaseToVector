"""
MCP Server implementation for code understanding.
This server provides tools for updating code repositories and querying code context.
"""

import logging
from typing import List, Dict, Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent
from pydantic import BaseModel

# Import our own services
from services.codebase_service import CodebaseService

# Define the input schemas for our tools
class UpdateCodebase(BaseModel):
    """Input schema for updating codebase."""
    project_name: str
    codebase_path: str  # Path to the codebase directory

class ReadCodeBase(BaseModel):
    """Input schema for querying codebase."""
    project_name: str
    question: str

# Tool names enum
class CodeTools:
    UPDATE_CODEBASE = "updateCodebase"
    READ_CODEBASE = "readCodeBase"

async def serve() -> None:
    """Start the MCP server for code understanding."""
    logger = logging.getLogger(__name__)
    
    logger.info("Starting MCP server for code understanding")
    
    # Initialize our service
    codebase_service = CodebaseService()
    # await codebase_service.update_codebase(
    #     project_name="test_app",
    #     root_path="./test_app",
    #     language="java"
    # )
    
    # Create MCP server
    server = Server("codebase-mcp")
    
    @server.list_tools()
    async def list_tools() -> List[Tool]:
        """List available tools for code understanding."""
        return [
            Tool(
                name=CodeTools.UPDATE_CODEBASE,
                description="Convert user codebases into vector storage for better project comprehension",
                inputSchema=UpdateCodebase.schema(),
            ),
            Tool(
                name=CodeTools.READ_CODEBASE,
                description="Query the codebase with a question to get relevant code snippets",
                inputSchema=ReadCodeBase.schema(),
            ),
        ]
    
    @server.call_tool()
    async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
        """Handle tool calls."""
        logger.info(f"Tool call: {name} with arguments: {arguments}")
        
        if name == CodeTools.UPDATE_CODEBASE:
            try:
                project_name = arguments["project_name"]
                codebase_path = arguments["codebase_path"]
                
                # Use the CodebaseService to update the codebase
                success = await codebase_service.update_codebase(
                    project_name=project_name,
                    root_path=codebase_path
                )
                
                if success:
                    return [TextContent(
                        type="text",
                        text=f"Successfully updated codebase for project '{project_name}'"
                    )]
                else:
                    return [TextContent(
                        type="text",
                        text=f"Failed to update codebase for project '{project_name}'"
                    )]
                
            except Exception as e:
                logger.error(f"Error updating codebase: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error updating codebase: {str(e)}"
                )]
                
        elif name == CodeTools.READ_CODEBASE:
            try:
                project_name = arguments["project_name"]
                question = arguments["question"]
                
                # Query the codebase
                results = await codebase_service.query_codebase(
                    project_name=project_name,
                    question=question,
                    limit=5
                )
                
                # Format results
                if not results:
                    return [TextContent(
                        type="text",
                        text=f"No results found for query: {question}"
                    )]
                
                response_text = f"Query: {question}\n\nResults:\n"
                for i, result in enumerate(results):
                    metadata = result["metadata"]
                    score = result["score"]
                    
                    response_text += f"\n--- Result {i+1} (similarity: {score:.4f}) ---\n"
                    response_text += f"File: {metadata.get('file_path', 'Unknown')}\n"
                    response_text += f"Type: {metadata.get('type', 'Unknown')}\n"
                    if metadata.get("class_name"):
                        response_text += f"Class: {metadata.get('class_name')}\n"
                    if metadata.get("method_name"):
                        response_text += f"Method: {metadata.get('method_name')}\n"
                    response_text += f"\n{metadata.get('content', 'No content available')}\n"
                
                return [TextContent(
                    type="text",
                    text=response_text
                )]
                
            except Exception as e:
                logger.error(f"Error querying codebase: {str(e)}")
                return [TextContent(
                    type="text",
                    text=f"Error querying codebase: {str(e)}"
                )]
        
        else:
            return [TextContent(
                type="text",
                text=f"Unknown tool: {name}"
            )]
    
    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True) 