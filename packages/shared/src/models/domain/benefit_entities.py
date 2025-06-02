from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

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