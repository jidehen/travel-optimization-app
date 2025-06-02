from pydantic import BaseModel, Field, ConfigDict

class MCPConfig(BaseModel):
    """Model representing MCP server configuration."""
    chase_travel_url: str = Field(..., description="Chase Travel API endpoint")
    safepay_wallet_url: str = Field(..., description="SafePay Wallet API endpoint")
    benefits_url: str = Field(..., description="Benefits API endpoint")
    timeout: float = Field(30.0, description="API request timeout in seconds")
    retry_attempts: int = Field(3, description="Number of retry attempts for failed requests")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "chase_travel_url": "https://api.chase-travel.example.com/v1",
                "safepay_wallet_url": "https://api.safepay.example.com/v1",
                "benefits_url": "https://api.benefits.example.com/v1",
                "timeout": 30.0,
                "retry_attempts": 3
            }
        }
    ) 