from typing import Optional
from mcp import Tool, ToolContext
from shared.models.api.flight_search import (
    Flight,
    FlightSegment,
    Price
)

class GetFlightDetailsTool(Tool):
    """Tool for retrieving detailed flight information."""
    
    name = "get_flight_details"
    description = "Get detailed information about a specific flight"
    
    async def execute(self, context: ToolContext, **kwargs) -> dict:
        try:
            flight_id = kwargs.get("flight_id")
            if not flight_id:
                raise ValueError("Flight ID is required")
            
            # TODO: Implement actual flight details retrieval logic
            # This is a mock implementation
            mock_flight = Flight(
                id=flight_id,
                segments=[
                    FlightSegment(
                        flight_number="AA123",
                        airline_code="AA",
                        departure_airport="JFK",
                        arrival_airport="LAX",
                        departure_time="2024-03-15T10:00:00Z",
                        arrival_time="2024-03-15T12:00:00Z",
                        duration_minutes=120
                    )
                ],
                price=Price(amount=299.99, currency="USD"),
                cabin_class="ECONOMY",
                available_seats=10
            )
            
            return mock_flight.model_dump()
            
        except ValueError as e:
            raise ValueError(f"Invalid input parameters: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving flight details: {str(e)}")
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "flight_id": {
                    "type": "string",
                    "description": "Unique identifier of the flight"
                }
            },
            "required": ["flight_id"]
        } 