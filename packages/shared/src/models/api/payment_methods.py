from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Header
from pydantic import BaseModel, Field, constr

# Response Models
class Card(BaseModel):
    card_id: str = Field(..., description="Unique card identifier")
    type: str = Field(..., description="Card type (CREDIT, DEBIT)")
    last_four_digits: constr(min_length=4, max_length=4) = Field(..., description="Last 4 digits of card number")
    expiry_month: int = Field(..., ge=1, le=12, description="Card expiry month")
    expiry_year: int = Field(..., ge=2024, description="Card expiry year")
    cardholder_name: str = Field(..., description="Name on card")
    is_default: bool = Field(False, description="Whether this is the default payment method")

class PaymentMethodsResponse(BaseModel):
    cards: List[Card] = Field(..., description="List of user's payment methods")
    total_count: int = Field(..., ge=0, description="Total number of payment methods")

# Error Models
class ErrorResponse(BaseModel):
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")

# Router
router = APIRouter(
    prefix="/api/wallet",
    tags=["wallet"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "Unauthorized access"},
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "No payment methods found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

@router.get(
    "/payment-methods",
    response_model=PaymentMethodsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get user's payment methods",
    description="Retrieve all payment methods associated with the user"
)
async def get_payment_methods(
    user_id: str = Header(..., description="User ID for authentication")
) -> PaymentMethodsResponse:
    """
    Get all payment methods for a user.
    
    - **user_id**: User ID in request header for authentication
    
    Returns a list of payment methods associated with the user.
    """
    # Implementation will be added in the actual service
    pass 