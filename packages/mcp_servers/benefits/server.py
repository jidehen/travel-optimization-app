import asyncio
import os
from typing import Dict, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from mcp import FastMCP, MCPRequest, MCPResponse
from dotenv import load_dotenv
from tools.get_card_benefits import GetCardBenefitsTool
from tools.calculate_rewards import CalculateRewardsTool

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Benefits MCP Server",
    description="MCP server for card benefits and rewards functionality",
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
mcp = FastMCP("Benefits")

# Register tools using decorator pattern
@mcp.tool("get_card_benefits")
async def get_card_benefits(request: MCPRequest) -> MCPResponse:
    """Get benefits for a specific card."""
    try:
        tool = GetCardBenefitsTool()
        result = await tool.execute(None, **request.parameters)
        return MCPResponse(status="success", data=result)
    except ValueError as e:
        return MCPResponse(status="error", error=str(e))
    except Exception as e:
        logger.error(f"Error getting card benefits: {str(e)}")
        return MCPResponse(status="error", error="Internal server error")

@mcp.tool("calculate_rewards")
async def calculate_rewards(request: MCPRequest) -> MCPResponse:
    """Calculate rewards for a purchase."""
    try:
        tool = CalculateRewardsTool()
        result = await tool.execute(None, **request.parameters)
        return MCPResponse(status="success", data=result)
    except ValueError as e:
        return MCPResponse(status="error", error=str(e))
    except Exception as e:
        logger.error(f"Error calculating rewards: {str(e)}")
        return MCPResponse(status="error", error="Internal server error")

# Health check endpoint
@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "benefits-mcp"}

# Mount MCP server to FastAPI app
app.mount("/mcp", mcp.app)

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