from pydantic import BaseModel, Field, ConfigDict

class EnvironmentConfig(BaseModel):
    """Model representing environment configuration."""
    environment: str = Field(..., description="Environment name (development, staging, production)")
    debug: bool = Field(False, description="Whether debug mode is enabled")
    log_level: str = Field("INFO", description="Logging level")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "environment": "development",
                "debug": True,
                "log_level": "DEBUG"
            }
        }
    ) 