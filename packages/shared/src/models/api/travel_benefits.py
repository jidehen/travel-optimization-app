from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

class BenefitsRequest(BaseModel):
    """Request model for retrieving travel benefits."""
    user_id: str = Field(..., description="User identifier")
    card_id: Optional[str] = Field(None, description="Specific card ID to check benefits for")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user_123",
                "card_id": "card_456"
            }
        }
    )

class BenefitsResponse(BaseModel):
    """Response model for travel benefits."""
    benefits: List["Benefit"] = Field(..., description="List of available benefits")
    total_value: float = Field(..., description="Total monetary value of benefits")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "benefits": [],
                "total_value": 0.0
            }
        }
    ) 