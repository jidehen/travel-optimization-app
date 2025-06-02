from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# Flight Entities
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

# Payment Entities
class Card(BaseModel):
    """Model representing a credit/debit card."""
    id: str = Field(..., description="Card identifier")
    last_four: str = Field(..., description="Last four digits of the card")
    brand: str = Field(..., description="Card brand (Visa, Mastercard, etc.)")
    expiry_month: int = Field(..., description="Card expiry month")
    expiry_year: int = Field(..., description="Card expiry year")
    is_default: bool = Field(False, description="Whether this is the default card")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "card_123",
                "last_four": "4242",
                "brand": "Visa",
                "expiry_month": 12,
                "expiry_year": 2025,
                "is_default": True
            }
        }
    )

class DigitalWallet(BaseModel):
    """Model representing a digital wallet."""
    id: str = Field(..., description="Wallet identifier")
    type: str = Field(..., description="Wallet type (e.g., Apple Pay, Google Pay)")
    is_default: bool = Field(False, description="Whether this is the default wallet")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "wallet_123",
                "type": "Apple Pay",
                "is_default": False
            }
        }
    )

class PaymentMethod(BaseModel):
    """Model representing a payment method."""
    id: str = Field(..., description="Payment method identifier")
    type: str = Field(..., description="Payment method type (card, digital_wallet)")
    card: Optional[Card] = Field(None, description="Card details if type is card")
    digital_wallet: Optional[DigitalWallet] = Field(None, description="Digital wallet details if type is digital_wallet")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "pm_123",
                "type": "card",
                "card": {
                    "id": "card_123",
                    "last_four": "4242",
                    "brand": "Visa"
                }
            }
        }
    )

# Benefit Entities
class Reward(BaseModel):
    """Model representing a reward."""
    type: str = Field(..., description="Reward type (points, miles, cashback)")
    amount: float = Field(..., description="Reward amount")
    currency: Optional[str] = Field(None, description="Currency for cashback rewards")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "type": "points",
                "amount": 1000.0
            }
        }
    )

class Multiplier(BaseModel):
    """Model representing a reward multiplier."""
    category: str = Field(..., description="Spending category")
    multiplier: float = Field(..., description="Reward multiplier value")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category": "travel",
                "multiplier": 3.0
            }
        }
    )

class Benefit(BaseModel):
    """Model representing a travel benefit."""
    id: str = Field(..., description="Benefit identifier")
    name: str = Field(..., description="Benefit name")
    description: str = Field(..., description="Benefit description")
    type: str = Field(..., description="Benefit type")
    rewards: List[Reward] = Field(..., description="Available rewards")
    multipliers: List[Multiplier] = Field(..., description="Available multipliers")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "benefit_123",
                "name": "Travel Rewards",
                "description": "Earn points on travel purchases",
                "type": "rewards",
                "rewards": [{"type": "points", "amount": 1000.0}],
                "multipliers": [{"category": "travel", "multiplier": 3.0}]
            }
        }
    )

# Optimization Entities
class Recommendation(BaseModel):
    """Model representing an optimization recommendation."""
    id: str = Field(..., description="Recommendation identifier")
    flight: Flight = Field(..., description="Recommended flight")
    payment_method: PaymentMethod = Field(..., description="Recommended payment method")
    benefits: List[Benefit] = Field(..., description="Applicable benefits")
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