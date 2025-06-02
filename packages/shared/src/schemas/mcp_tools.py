from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class SearchFlightsInput(BaseModel):
    """Input schema for the search_flights MCP tool."""
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    departure_date: str = Field(..., description="Departure date in ISO format")
    return_date: Optional[str] = Field(None, description="Return date in ISO format")
    passengers: int = Field(1, ge=1, le=9, description="Number of passengers")
    cabin_class: str = Field("economy", description="Cabin class")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "origin": "JFK",
                "destination": "LAX",
                "departure_date": "2024-03-15",
                "passengers": 2,
                "cabin_class": "business"
            }
        }
    )

class SearchFlightsOutput(BaseModel):
    """Output schema for the search_flights MCP tool."""
    flights: List[Dict[str, Any]] = Field(..., description="List of available flights")
    search_id: str = Field(..., description="Unique identifier for this search")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "flights": [],
                "search_id": "search_123"
            }
        }
    )

class GetPaymentMethodsInput(BaseModel):
    """Input schema for the get_payment_methods MCP tool."""
    user_id: str = Field(..., description="User identifier")
    include_digital_wallets: bool = Field(True, description="Whether to include digital wallet payment methods")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "user_id": "user_123",
                "include_digital_wallets": True
            }
        }
    )

class GetPaymentMethodsOutput(BaseModel):
    """Output schema for the get_payment_methods MCP tool."""
    payment_methods: List[Dict[str, Any]] = Field(..., description="List of available payment methods")
    default_method: Optional[str] = Field(None, description="ID of the default payment method")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_methods": [],
                "default_method": "pm_123"
            }
        }
    )

class GetBenefitsInput(BaseModel):
    """Input schema for the get_benefits MCP tool."""
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

class GetBenefitsOutput(BaseModel):
    """Output schema for the get_benefits MCP tool."""
    benefits: List[Dict[str, Any]] = Field(..., description="List of available benefits")
    total_value: float = Field(..., description="Total monetary value of benefits")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "benefits": [],
                "total_value": 0.0
            }
        }
    )

class OptimizeTravelInput(BaseModel):
    """Input schema for the optimize_travel MCP tool."""
    flight_search_id: str = Field(..., description="ID of the flight search to optimize")
    user_id: str = Field(..., description="User identifier")
    preferences: Dict[str, Any] = Field(..., description="User preferences for optimization")
    
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

class OptimizeTravelOutput(BaseModel):
    """Output schema for the optimize_travel MCP tool."""
    recommendations: List[Dict[str, Any]] = Field(..., description="List of optimization recommendations")
    optimization_id: str = Field(..., description="Unique identifier for this optimization")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "recommendations": [],
                "optimization_id": "opt_123"
            }
        }
    )

class GetRecommendationDetailsInput(BaseModel):
    """Input schema for the get_recommendation_details MCP tool."""
    recommendation_id: str = Field(..., description="ID of the recommendation to get details for")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "recommendation_id": "rec_123"
            }
        }
    )

class GetRecommendationDetailsOutput(BaseModel):
    """Output schema for the get_recommendation_details MCP tool."""
    recommendation: Dict[str, Any] = Field(..., description="Detailed recommendation information")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "recommendation": {
                    "id": "rec_123",
                    "flight": {},
                    "payment_method": {},
                    "benefits": [],
                    "total_savings": 100.0,
                    "explanation": "Using this card provides 3x points on travel"
                }
            }
        }
    ) 