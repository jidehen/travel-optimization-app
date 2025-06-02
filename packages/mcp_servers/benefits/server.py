import asyncio
import os
from typing import Dict, Any, List
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
    title="Benefits MCP Server",
    description="MCP server for card benefits functionality",
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
benefits_mcp = FastMCP("Benefits")

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "benefits-mcp"}

# MCP tool for getting benefits
@benefits_mcp.tool("get_benefits")
async def get_benefits(request: MCPRequest) -> MCPResponse:
    """
    Get available benefits for a user's card.
    
    Args:
        request: MCP request containing user ID and optional card ID
        
    Returns:
        MCP response with available benefits
    """
    try:
        # Extract parameters from request
        user_id = request.parameters.get("user_id")
        card_id = request.parameters.get("card_id")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        # TODO: Implement actual benefits retrieval
        # This is a placeholder response
        response_data = {
            "benefits": [
                {
                    "id": "benefit_123",
                    "name": "Travel Rewards",
                    "description": "Earn points on travel purchases",
                    "type": "rewards",
                    "rewards": [{"type": "points", "amount": 1000.0}],
                    "multipliers": [{"category": "travel", "multiplier": 3.0}]
                }
            ],
            "total_value": 1000.0
        }
        
        return MCPResponse(
            status="success",
            data=response_data
        )
    except Exception as e:
        logger.error(f"Error getting benefits: {str(e)}")
        return MCPResponse(
            status="error",
            error=str(e)
        )

# MCP tool for calculating rewards
@benefits_mcp.tool("calculate_rewards")
async def calculate_rewards(request: MCPRequest) -> MCPResponse:
    """
    Calculate potential rewards for a purchase.
    
    Args:
        request: MCP request containing purchase details
        
    Returns:
        MCP response with calculated rewards
    """
    try:
        # Extract purchase details from request
        purchase_amount = request.parameters.get("amount")
        purchase_category = request.parameters.get("category")
        card_id = request.parameters.get("card_id")
        
        if not all([purchase_amount, purchase_category, card_id]):
            raise HTTPException(
                status_code=400,
                detail="Purchase amount, category, and card ID are required"
            )
        
        # TODO: Implement actual rewards calculation
        # This is a placeholder response
        response_data = {
            "rewards": [
                {
                    "type": "points",
                    "amount": float(purchase_amount) * 3.0,
                    "multiplier": 3.0,
                    "category": purchase_category
                }
            ],
            "total_rewards": float(purchase_amount) * 3.0
        }
        
        return MCPResponse(
            status="success",
            data=response_data
        )
    except Exception as e:
        logger.error(f"Error calculating rewards: {str(e)}")
        return MCPResponse(
            status="error",
            error=str(e)
        )

# Mount MCP server to FastAPI app
app.mount("/mcp", benefits_mcp.app)

async def main():
    """Main entry point for the server."""
    # Configure logging
    logger.add(
        "logs/benefits_mcp.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )
    
    # Start the server
    import uvicorn
    port = int(os.getenv("PORT", "3003"))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

if __name__ == "__main__":
    asyncio.run(main()) 