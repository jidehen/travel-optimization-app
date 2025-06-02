from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class OptimizationRequest(BaseModel):
    """Request model for travel optimization."""
    flight_search_id: str = Field(..., description="ID of the flight search to optimize")
    user_id: str = Field(..., description="User identifier")
    preferences: dict = Field(..., description="User preferences for optimization")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "flight_search_id": "search_123",
                "user_id": "user_123",
                "preferences": {
                    "max_price": 1000.0,
                    "preferred_airlines": ["AA", "DL"],
                    "min_layover_time": 60
                }
            }
        }
    )

class OptimizationResponse(BaseModel):
    """Response model for optimization results."""
    recommendations: List["Recommendation"] = Field(..., description="List of optimization recommendations")
    optimization_id: str = Field(..., description="Unique identifier for this optimization")
    created_at: datetime = Field(..., description="Timestamp of optimization creation")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "recommendations": [],
                "optimization_id": "opt_123",
                "created_at": "2024-03-15T10:00:00Z"
            }
        }
    ) 