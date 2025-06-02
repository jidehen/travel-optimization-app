from pydantic import BaseModel, Field, ConfigDict
from .environment import EnvironmentConfig
from .mcp import MCPConfig

class AppConfig(BaseModel):
    """Model representing the complete application configuration."""
    environment: EnvironmentConfig = Field(..., description="Environment configuration")
    mcp: MCPConfig = Field(..., description="External API configuration")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "environment": {
                    "environment": "development",
                    "debug": True,
                    "log_level": "INFO"
                },
                "mcp": {
                    "chase_travel_url": "https://api.chase-travel.example.com/v1",
                    "safepay_wallet_url": "https://api.safepay.example.com/v1",
                    "benefits_url": "https://api.benefits.example.com/v1",
                    "timeout": 30.0,
                    "retry_attempts": 3
                }
            }
        }
    ) 