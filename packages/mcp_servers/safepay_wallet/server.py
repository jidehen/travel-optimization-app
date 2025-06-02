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
    title="SafePay Wallet MCP Server",
    description="MCP server for payment methods functionality",
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
safepay_wallet_mcp = FastMCP("SafePay Wallet")

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "safepay-wallet-mcp"}

# MCP tool for getting payment methods
@safepay_wallet_mcp.tool("get_payment_methods")
async def get_payment_methods(request: MCPRequest) -> MCPResponse:
    """
    Get available payment methods for a user.
    
    Args:
        request: MCP request containing user ID
        
    Returns:
        MCP response with payment methods
    """
    try:
        # Extract user ID from request
        user_id = request.parameters.get("user_id")
        
        if not user_id:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        # TODO: Implement actual payment methods retrieval
        # This is a placeholder response
        response_data = {
            "payment_methods": [
                {
                    "id": "pm_123",
                    "type": "card",
                    "card": {
                        "id": "card_123",
                        "last_four": "4242",
                        "brand": "Visa"
                    }
                }
            ],
            "default_method": "pm_123"
        }
        
        return MCPResponse(
            status="success",
            data=response_data
        )
    except Exception as e:
        logger.error(f"Error getting payment methods: {str(e)}")
        return MCPResponse(
            status="error",
            error=str(e)
        )

# MCP tool for adding payment method
@safepay_wallet_mcp.tool("add_payment_method")
async def add_payment_method(request: MCPRequest) -> MCPResponse:
    """
    Add a new payment method for a user.
    
    Args:
        request: MCP request containing payment method details
        
    Returns:
        MCP response with the added payment method
    """
    try:
        # Extract payment method details from request
        payment_method = request.parameters.get("payment_method")
        
        if not payment_method:
            raise HTTPException(status_code=400, detail="Payment method details are required")
        
        # TODO: Implement actual payment method addition
        # This is a placeholder response
        response_data = {
            "id": "pm_123",
            "type": "card",
            "card": {
                "id": "card_123",
                "last_four": "4242",
                "brand": "Visa"
            }
        }
        
        return MCPResponse(
            status="success",
            data=response_data
        )
    except Exception as e:
        logger.error(f"Error adding payment method: {str(e)}")
        return MCPResponse(
            status="error",
            error=str(e)
        )

# Mount MCP server to FastAPI app
app.mount("/mcp", safepay_wallet_mcp.app)

async def main():
    """Main entry point for the server."""
    # Configure logging
    logger.add(
        "logs/safepay_wallet_mcp.log",
        rotation="1 day",
        retention="7 days",
        level="INFO"
    )
    
    # Start the server
    import uvicorn
    port = int(os.getenv("PORT", "3002"))
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )

if __name__ == "__main__":
    asyncio.run(main()) 