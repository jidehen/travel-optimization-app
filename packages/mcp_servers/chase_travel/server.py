import asyncio
import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from mcp import FastMCP, MCPRequest, MCPResponse
from pydantic import BaseModel
from dotenv import load_dotenv

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
chase_travel_mcp = FastMCP("Chase Travel")

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "chase-travel-mcp"}

# MCP tool for flight search
@chase_travel_mcp.tool("search_flights")
async def search_flights(request: MCPRequest) -> MCPResponse:
    """
    Search for available flights based on criteria.
    
    Args:
        request: MCP request containing search parameters
        
    Returns:
        MCP response with flight search results
    """
    try:
        # Extract search parameters from request
        params = request.parameters
        
        # TODO: Implement actual flight search logic
        # This is a placeholder response
        response_data = {
            "flights": [],
            "total_results": 0,
            "search_id": "search_123"
        }
        
        return MCPResponse(
            status="success",
            data=response_data
        )
    except Exception as e:
        logger.error(f"Error in flight search: {str(e)}")
        return MCPResponse(
            status="error",
            error=str(e)
        )

# MCP tool for flight details
@chase_travel_mcp.tool("get_flight_details")
async def get_flight_details(request: MCPRequest) -> MCPResponse:
    """
    Get detailed information about a specific flight.
    
    Args:
        request: MCP request containing flight ID
        
    Returns:
        MCP response with flight details
    """
    try:
        # Extract flight ID from request
        flight_id = request.parameters.get("flight_id")
        
        if not flight_id:
            raise HTTPException(status_code=400, detail="Flight ID is required")
        
        # TODO: Implement actual flight details retrieval
        # This is a placeholder response
        response_data = {
            "flight_number": "AA100",
            "airline": {"code": "AA", "name": "American Airlines"},
            "origin": {"code": "JFK", "name": "JFK International"},
            "destination": {"code": "LAX", "name": "Los Angeles International"},
            "departure_time": "2024-03-15T10:00:00Z",
            "arrival_time": "2024-03-15T13:00:00Z",
            "duration": 360,
            "aircraft_type": "B777",
            "cabin_class": "business",
            "price": 500.0,
            "currency": "USD"
        }
        
        return MCPResponse(
            status="success",
            data=response_data
        )
    except Exception as e:
        logger.error(f"Error getting flight details: {str(e)}")
        return MCPResponse(
            status="error",
            error=str(e)
        )

# Mount MCP server to FastAPI app
app.mount("/mcp", chase_travel_mcp.app)

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