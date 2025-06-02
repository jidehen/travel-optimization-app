from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class Recommendation(BaseModel):
    """Model representing an optimization recommendation."""
    id: str = Field(..., description="Recommendation identifier")
    flight: "Flight" = Field(..., description="Recommended flight")
    payment_method: "PaymentMethod" = Field(..., description="Recommended payment method")
    benefits: List["Benefit"] = Field(..., description="Applicable benefits")
    total_savings: float = Field(..., description="Total savings amount")
    currency: str = Field("USD", description="Currency for savings")
    explanation: str = Field(..., description="Explanation of the recommendation")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "rec_123",
                "flight": {
                    "flight_number": "AA100",
                    "airline": {"code": "AA", "name": "American Airlines"}
                },
                "payment_method": {
                    "id": "pm_123",
                    "type": "card"
                },
                "benefits": [],
                "total_savings": 100.0,
                "currency": "USD",
                "explanation": "Using this card provides 3x points on travel"
            }
        }
    )

class OptimizationResult(BaseModel):
    """Model representing the complete optimization result."""
    id: str = Field(..., description="Optimization result identifier")
    recommendations: List[Recommendation] = Field(..., description="List of recommendations")
    created_at: datetime = Field(..., description="Creation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "opt_123",
                "recommendations": [],
                "created_at": "2024-03-15T10:00:00Z",
                "metadata": {}
            }
        }
    ) 