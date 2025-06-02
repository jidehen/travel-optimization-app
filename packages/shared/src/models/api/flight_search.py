from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

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