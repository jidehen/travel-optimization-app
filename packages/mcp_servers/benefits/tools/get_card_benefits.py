from typing import List
from mcp import Tool, ToolContext
from shared.models.api.travel_benefits import (
    BenefitsResponse,
    Multiplier,
    CardBenefit
)

class GetCardBenefitsTool(Tool):
    """Tool for retrieving card benefits and multipliers."""
    
    name = "get_card_benefits"
    description = "Get benefits and multipliers for a specific card"
    
    async def execute(self, context: ToolContext, **kwargs) -> dict:
        try:
            card_id = kwargs.get("card_id")
            if not card_id:
                raise ValueError("Card ID is required")
            
            # TODO: Implement actual card benefits retrieval logic
            # This is a mock implementation
            mock_multipliers = [
                Multiplier(
                    category="TRAVEL",
                    multiplier=3.0,
                    description="3x points on all travel purchases"
                ),
                Multiplier(
                    category="DINING",
                    multiplier=2.0,
                    description="2x points on dining purchases"
                ),
                Multiplier(
                    category="GENERAL",
                    multiplier=1.0,
                    description="1x points on all other purchases"
                )
            ]
            
            mock_benefits = [
                CardBenefit(
                    benefit_id="benefit_1",
                    name="Travel Insurance",
                    description="Comprehensive travel insurance coverage",
                    is_active=True
                ),
                CardBenefit(
                    benefit_id="benefit_2",
                    name="Airport Lounge Access",
                    description="Access to Priority Pass lounges worldwide",
                    is_active=True
                )
            ]
            
            response = BenefitsResponse(
                card_id=card_id,
                card_name="Chase Sapphire Reserve",
                multipliers=mock_multipliers,
                benefits=mock_benefits,
                annual_fee=550.00,
                currency="USD"
            )
            
            return response.model_dump()
            
        except ValueError as e:
            raise ValueError(f"Invalid input parameters: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving card benefits: {str(e)}")
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "Card identifier"
                }
            },
            "required": ["card_id"]
        } 