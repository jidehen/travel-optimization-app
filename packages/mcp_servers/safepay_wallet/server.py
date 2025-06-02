import asyncio
import os
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from mcp import FastMCP, MCPRequest, MCPResponse
from dotenv import load_dotenv
from tools.get_payment_methods import GetPaymentMethodsTool

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
mcp = FastMCP("SafePay Wallet")

# Register tools using decorator pattern
@mcp.tool("get_payment_methods")
async def get_payment_methods(request: MCPRequest) -> MCPResponse:
    """Get available payment methods for a user."""
    try:
        tool = GetPaymentMethodsTool()
        result = await tool.execute(None, **request.parameters)
        return MCPResponse(status="success", data=result)
    except ValueError as e:
        return MCPResponse(status="error", error=str(e))
    except Exception as e:
        logger.error(f"Error getting payment methods: {str(e)}")
        return MCPResponse(status="error", error="Internal server error")

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "safepay-wallet-mcp"}

# Mount MCP server to FastAPI app
app.mount("/mcp", mcp.app)

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