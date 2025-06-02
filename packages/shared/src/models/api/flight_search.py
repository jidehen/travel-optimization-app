from datetime import date
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, constr

# Request Models
class PassengerCount(BaseModel):
    adults: int = Field(..., ge=1, le=9, description="Number of adult passengers")
    children: int = Field(0, ge=0, le=9, description="Number of child passengers")
    infants: int = Field(0, ge=0, le=9, description="Number of infant passengers")

class FlightSearchRequest(BaseModel):
    origin: constr(min_length=3, max_length=3) = Field(..., description="Origin airport IATA code")
    destination: constr(min_length=3, max_length=3) = Field(..., description="Destination airport IATA code")
    departure_date: date = Field(..., description="Flight departure date")
    passengers: PassengerCount = Field(..., description="Number of passengers by type")
    return_date: Optional[date] = Field(None, description="Return flight date for round trips")
    cabin_class: Optional[str] = Field("ECONOMY", description="Cabin class (ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST)")

# Response Models
class Price(BaseModel):
    amount: float = Field(..., gt=0, description="Price amount")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (ISO 4217)")

class FlightSegment(BaseModel):
    flight_number: str = Field(..., description="Flight number")
    airline_code: str = Field(..., min_length=2, max_length=2, description="Airline IATA code")
    departure_airport: str = Field(..., min_length=3, max_length=3, description="Departure airport IATA code")
    arrival_airport: str = Field(..., min_length=3, max_length=3, description="Arrival airport IATA code")
    departure_time: str = Field(..., description="Departure time in ISO format")
    arrival_time: str = Field(..., description="Arrival time in ISO format")
    duration_minutes: int = Field(..., gt=0, description="Flight duration in minutes")

class Flight(BaseModel):
    id: str = Field(..., description="Unique flight identifier")
    segments: List[FlightSegment] = Field(..., min_items=1, description="Flight segments")
    price: Price = Field(..., description="Flight price")
    cabin_class: str = Field(..., description="Cabin class")
    available_seats: int = Field(..., ge=0, description="Number of available seats")

class FlightSearchResponse(BaseModel):
    flights: List[Flight] = Field(..., description="List of available flights")
    total_count: int = Field(..., ge=0, description="Total number of flights found")

# Error Models
class ErrorResponse(BaseModel):
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")

# Router
router = APIRouter(
    prefix="/api/flights",
    tags=["flights"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "Invalid request parameters"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "No flights found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

@router.post(
    "/search",
    response_model=FlightSearchResponse,
    status_code=status.HTTP_200_OK,
    summary="Search for available flights",
    description="Search for flights based on origin, destination, dates, and passenger information"
)
async def search_flights(request: FlightSearchRequest) -> FlightSearchResponse:
    """
    Search for available flights with the following parameters:
    
    - **origin**: Origin airport IATA code (3 characters)
    - **destination**: Destination airport IATA code (3 characters)
    - **departure_date**: Flight departure date
    - **passengers**: Number of passengers by type (adults, children, infants)
    - **return_date**: Optional return flight date for round trips
    - **cabin_class**: Optional cabin class preference
    
    Returns a list of available flights matching the search criteria.
    """
    # Implementation will be added in the actual service
    pass 