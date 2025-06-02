import asyncio
import os
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from mcp import FastMCP, MCPRequest, MCPResponse
from dotenv import load_dotenv
from tools.search_flights import SearchFlightsTool
from tools.get_flight_details import GetFlightDetailsTool

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Chase Travel MCP Server",
    description="MCP server for flight search functionality",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize MCP server
mcp = FastMCP("Chase Travel")

# Register tools using decorator pattern
@mcp.tool("search_flights")
async def search_flights(request: MCPRequest) -> MCPResponse:
    """Search for available flights based on criteria."""
    try:
        tool = SearchFlightsTool()
        result = await tool.execute(None, **request.parameters)
        return MCPResponse(status="success", data=result)
    except ValueError as e:
        return MCPResponse(status="error", error=str(e))
    except Exception as e:
        logger.error(f"Error in flight search: {str(e)}")
        return MCPResponse(status="error", error="Internal server error")

@mcp.tool("get_flight_details")
async def get_flight_details(request: MCPRequest) -> MCPResponse:
    """Get detailed information about a specific flight."""
    try:
        tool = GetFlightDetailsTool()
        result = await tool.execute(None, **request.parameters)
        return MCPResponse(status="success", data=result)
    except ValueError as e:
        return MCPResponse(status="error", error=str(e))
    except Exception as e:
        logger.error(f"Error getting flight details: {str(e)}")
        return MCPResponse(status="error", error="Internal server error")

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "chase-travel-mcp"}

# Mount MCP server to FastAPI app
app.mount("/mcp", mcp.app)

async def main():
    """Main entry point for the server."""
    # Configure logging
    logger.add(
        "logs/chase_travel_mcp.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )
    
    # Start the server
    import uvicorn
    port = int(os.getenv("PORT", "3001"))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

if __name__ == "__main__":
    asyncio.run(main()) 