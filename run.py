#!/usr/bin/env python3
"""
Entry point script for running the stock analysis MCP server.
"""

import logging
import sys
import main

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, 
                       format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Stock Price MCP Server...")
    
    try:
        main.mcp.run()
        logger.info("Server started successfully")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)
