from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# Flight Search Models
class FlightSearchRequest(BaseModel):
    """Request model for flight search."""
    origin: str = Field(..., description="Origin airport code")
    destination: str = Field(..., description="Destination airport code")
    departure_date: datetime = Field(..., description="Departure date and time")
    return_date: Optional[datetime] = Field(None, description="Return date and time for round trips")
    passengers: int = Field(1, ge=1, le=9, description="Number of passengers")
    cabin_class: str = Field("economy", description="Cabin class (economy, premium, business, first)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "origin": "JFK",
                "destination": "LAX",
                "departure_date": "2024-03-15T10:00:00Z",
                "passengers": 2,
                "cabin_class": "business"
            }
        }
    )

class FlightSearchResponse(BaseModel):
    """Response model for flight search results."""
    flights: List["Flight"] = Field(..., description="List of available flights")
    total_results: int = Field(..., description="Total number of results found")
    search_id: str = Field(..., description="Unique identifier for this search")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "flights": [],
                "total_results": 0,
                "search_id": "search_123"
            }
        }
    )

# Payment Methods Models
class PaymentMethodsRequest(BaseModel):
    """Request model for retrieving payment methods."""
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

class PaymentMethodsResponse(BaseModel):
    """Response model for payment methods."""
    payment_methods: List["PaymentMethod"] = Field(..., description="List of available payment methods")
    default_method: Optional[str] = Field(None, description="ID of the default payment method")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_methods": [],
                "default_method": "pm_123"
            }
        }
    )

# Benefits Models
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

# Optimization Models
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