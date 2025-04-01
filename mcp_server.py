"""
MCP Server implementation for code understanding.
This server provides tools for updating code repositories and querying code context.
"""

from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator
from mcp.types import TextContent
from mcp.server.fastmcp import FastMCP, Context

# Import our own services
from services.codebase_service import CodebaseService


mcp = FastMCP("codebase-mcp")

@dataclass
class ServerContext:
    codebase_service: CodebaseService

@mcp.tool()
async def update_codebase(project_name: str, codebase_path: str, ctx: Context) -> str:
    """Tool that updates the codebase"""
    try:
        codebase_service = CodebaseService()
        result = await codebase_service.update_codebase(
            project_name=project_name,
            root_path=codebase_path,
        )
        if result:
            return [TextContent(
                type="text",
                text=f"Successfully updated codebase for project '{project_name}', with result: {result}"
            )]
        else:
            return [TextContent(
                type="text",
                text=f"Failed to update codebase for project '{project_name}', with result: {result}"
            )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error updating codebase: {str(e)}"
        )]
    
@mcp.tool()
async def files_count(codebase_path: str, ctx: Context) -> str:
    """Tool that gets the files count in the codebase"""
    try:
        codebase_service = CodebaseService()
        result = codebase_service.java_code_parser.parse_directory(codebase_path)
        return [TextContent(
            type="text",
            text=f"Files count: {len(result)}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting files count: {str(e)}"
        )]
    
@mcp.tool()
async def get_points_for_vector(codebase_path: str, ctx: Context) -> str:
    """Tool that gets the points for vector"""
    try:
        codebase_service = CodebaseService()
        result = codebase_service.get_separated_code_for_vector(codebase_path)
        return [TextContent(
            type="text",
            text=f"Points: {len(result)}"
        )]
    except Exception as e:
        return [TextContent(
            type="text",
            text=f"Error getting points for vector: {str(e)}"
        )]

@mcp.tool()
async def read_codebase(project_name: str, question: str, ctx: Context) -> str:
    """Tool that reads the codebase"""
    try:
        codebase_service = CodebaseService()
        results = await codebase_service.query_codebase(
            project_name=project_name,
            question=question,
            limit=5
        )
        
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
        return [TextContent(
            type="text",
            text=f"Error querying codebase: {str(e)}"
        )]

if __name__ == "__main__":
    mcp.run()