from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Path
from pydantic import BaseModel, Field, confloat

# Response Models
class Multiplier(BaseModel):
    category: str = Field(..., description="Spending category")
    multiplier: confloat(ge=1.0) = Field(..., description="Reward multiplier for the category")
    description: str = Field(..., description="Description of the multiplier benefit")

class CardBenefit(BaseModel):
    benefit_id: str = Field(..., description="Unique benefit identifier")
    name: str = Field(..., description="Benefit name")
    description: str = Field(..., description="Benefit description")
    is_active: bool = Field(True, description="Whether the benefit is currently active")

class BenefitsResponse(BaseModel):
    card_id: str = Field(..., description="Card identifier")
    card_name: str = Field(..., description="Name of the card")
    multipliers: List[Multiplier] = Field(..., description="List of reward multipliers")
    benefits: List[CardBenefit] = Field(..., description="List of card benefits")
    annual_fee: float = Field(..., ge=0, description="Annual fee amount")
    currency: str = Field(..., min_length=3, max_length=3, description="Currency code (ISO 4217)")

# Error Models
class ErrorResponse(BaseModel):
    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[dict] = Field(None, description="Additional error details")

# Router
router = APIRouter(
    prefix="/api/benefits",
    tags=["benefits"],
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "Card not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": ErrorResponse, "description": "Internal server error"}
    }
)

@router.get(
    "/cards/{card_id}",
    response_model=BenefitsResponse,
    status_code=status.HTTP_200_OK,
    summary="Get card benefits",
    description="Retrieve benefits and multipliers for a specific card"
)
async def get_card_benefits(
    card_id: str = Path(..., description="Card identifier")
) -> BenefitsResponse:
    """
    Get benefits and multipliers for a specific card.
    
    - **card_id**: Card identifier in the URL path
    
    Returns the card's benefits, multipliers, and other relevant information.
    """
    # Implementation will be added in the actual service
    pass 