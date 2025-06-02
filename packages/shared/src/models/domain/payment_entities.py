from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

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