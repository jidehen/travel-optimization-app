from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class Airport(BaseModel):
    """Model representing an airport."""
    code: str = Field(..., description="Airport IATA code")
    name: str = Field(..., description="Airport name")
    city: str = Field(..., description="City where the airport is located")
    country: str = Field(..., description="Country where the airport is located")
    timezone: str = Field(..., description="Airport timezone")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "JFK",
                "name": "John F. Kennedy International Airport",
                "city": "New York",
                "country": "United States",
                "timezone": "America/New_York"
            }
        }
    )

class Airline(BaseModel):
    """Model representing an airline."""
    code: str = Field(..., description="Airline IATA code")
    name: str = Field(..., description="Airline name")
    alliance: Optional[str] = Field(None, description="Airline alliance (e.g., Star Alliance, Oneworld)")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "code": "AA",
                "name": "American Airlines",
                "alliance": "Oneworld"
            }
        }
    )

class Flight(BaseModel):
    """Model representing a flight."""
    flight_number: str = Field(..., description="Flight number")
    airline: Airline = Field(..., description="Operating airline")
    origin: Airport = Field(..., description="Origin airport")
    destination: Airport = Field(..., description="Destination airport")
    departure_time: datetime = Field(..., description="Scheduled departure time")
    arrival_time: datetime = Field(..., description="Scheduled arrival time")
    duration: int = Field(..., description="Flight duration in minutes")
    aircraft_type: str = Field(..., description="Type of aircraft")
    cabin_class: str = Field(..., description="Cabin class")
    price: float = Field(..., description="Flight price")
    currency: str = Field("USD", description="Price currency")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "flight_number": "AA100",
                "airline": {"code": "AA", "name": "American Airlines"},
                "origin": {"code": "JFK", "name": "JFK International"},
                "destination": {"code": "LAX", "name": "Los Angeles International"},
                "departure_time": "2024-03-15T10:00:00Z",
                "arrival_time": "2024-03-15T13:00:00Z",
                "duration": 360,
                "aircraft_type": "B777",
                "cabin_class": "business",
                "price": 500.0,
                "currency": "USD"
            }
        }
    ) 