from typing import List, Optional
from datetime import date
from mcp import Tool, ToolContext
from shared.models.api.flight_search import (
    FlightSearchRequest,
    FlightSearchResponse,
    Flight,
    FlightSegment,
    Price,
    PassengerCount
)

class SearchFlightsTool(Tool):
    """Tool for searching available flights."""
    
    name = "search_flights"
    description = "Search for available flights based on origin, destination, dates, and passenger information"
    
    async def execute(self, context: ToolContext, **kwargs) -> dict:
        try:
            # Parse request parameters
            request = FlightSearchRequest(
                origin=kwargs.get("origin"),
                destination=kwargs.get("destination"),
                departure_date=date.fromisoformat(kwargs.get("departure_date")),
                passengers=PassengerCount(
                    adults=kwargs.get("adults", 1),
                    children=kwargs.get("children", 0),
                    infants=kwargs.get("infants", 0)
                ),
                return_date=date.fromisoformat(kwargs.get("return_date")) if kwargs.get("return_date") else None,
                cabin_class=kwargs.get("cabin_class", "ECONOMY")
            )
            
            # TODO: Implement actual flight search logic
            # This is a mock implementation
            mock_flight = Flight(
                id="FL123",
                segments=[
                    FlightSegment(
                        flight_number="AA123",
                        airline_code="AA",
                        departure_airport=request.origin,
                        arrival_airport=request.destination,
                        departure_time="2024-03-15T10:00:00Z",
                        arrival_time="2024-03-15T12:00:00Z",
                        duration_minutes=120
                    )
                ],
                price=Price(amount=299.99, currency="USD"),
                cabin_class=request.cabin_class,
                available_seats=10
            )
            
            response = FlightSearchResponse(
                flights=[mock_flight],
                total_count=1
            )
            
            return response.model_dump()
            
        except ValueError as e:
            raise ValueError(f"Invalid input parameters: {str(e)}")
        except Exception as e:
            raise Exception(f"Error searching flights: {str(e)}")
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Origin airport IATA code (3 characters)"
                },
                "destination": {
                    "type": "string",
                    "description": "Destination airport IATA code (3 characters)"
                },
                "departure_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Flight departure date (YYYY-MM-DD)"
                },
                "adults": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 9,
                    "default": 1,
                    "description": "Number of adult passengers"
                },
                "children": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 9,
                    "default": 0,
                    "description": "Number of child passengers"
                },
                "infants": {
                    "type": "integer",
                    "minimum": 0,
                    "maximum": 9,
                    "default": 0,
                    "description": "Number of infant passengers"
                },
                "return_date": {
                    "type": "string",
                    "format": "date",
                    "description": "Return flight date for round trips (YYYY-MM-DD)"
                },
                "cabin_class": {
                    "type": "string",
                    "enum": ["ECONOMY", "PREMIUM_ECONOMY", "BUSINESS", "FIRST"],
                    "default": "ECONOMY",
                    "description": "Cabin class preference"
                }
            },
            "required": ["origin", "destination", "departure_date"]
        } 