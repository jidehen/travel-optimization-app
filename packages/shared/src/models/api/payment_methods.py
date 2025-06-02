from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

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