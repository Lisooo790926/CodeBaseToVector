#!/usr/bin/env python3
"""
Main entry point for the MCP Server for code understanding.
"""

import click
import logging
import sys

from .mcp_server import serve

@click.command()
@click.option("-v", "--verbose", count=True, help="Increase verbosity")
def main(verbose: bool) -> None:
    """MCP Server for Code Understanding"""
    import asyncio
    
    # Set up logging based on verbosity
    logging_level = logging.WARN
    if verbose == 1:
        logging_level = logging.INFO
    elif verbose >= 2:
        logging_level = logging.DEBUG

    # Configure logging
    logging.basicConfig(
        level=logging_level,
        stream=sys.stderr,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Run the server
    try:
        asyncio.run(serve())
    except Exception as e:
        logging.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()