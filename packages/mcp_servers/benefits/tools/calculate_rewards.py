from typing import List, Dict
from mcp import Tool, ToolContext
from shared.models.api.travel_benefits import Multiplier

class CalculateRewardsTool(Tool):
    """Tool for calculating potential rewards for purchases."""
    
    name = "calculate_rewards"
    description = "Calculate potential rewards for purchases based on card multipliers"
    
    async def execute(self, context: ToolContext, **kwargs) -> dict:
        try:
            card_id = kwargs.get("card_id")
            purchases = kwargs.get("purchases", [])
            
            if not card_id:
                raise ValueError("Card ID is required")
            if not purchases:
                raise ValueError("At least one purchase is required")
            
            # TODO: Implement actual rewards calculation logic
            # This is a mock implementation
            mock_multipliers = {
                "TRAVEL": 3.0,
                "DINING": 2.0,
                "GENERAL": 1.0
            }
            
            total_rewards = 0
            purchase_rewards = []
            
            for purchase in purchases:
                category = purchase.get("category", "GENERAL")
                amount = float(purchase.get("amount", 0))
                multiplier = mock_multipliers.get(category, 1.0)
                
                rewards = amount * multiplier
                total_rewards += rewards
                
                purchase_rewards.append({
                    "category": category,
                    "amount": amount,
                    "multiplier": multiplier,
                    "rewards": rewards
                })
            
            return {
                "card_id": card_id,
                "total_rewards": total_rewards,
                "purchase_rewards": purchase_rewards
            }
            
        except ValueError as e:
            raise ValueError(f"Invalid input parameters: {str(e)}")
        except Exception as e:
            raise Exception(f"Error calculating rewards: {str(e)}")
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "card_id": {
                    "type": "string",
                    "description": "Card identifier"
                },
                "purchases": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "category": {
                                "type": "string",
                                "enum": ["TRAVEL", "DINING", "GENERAL"],
                                "description": "Purchase category"
                            },
                            "amount": {
                                "type": "number",
                                "minimum": 0,
                                "description": "Purchase amount"
                            }
                        },
                        "required": ["category", "amount"]
                    },
                    "description": "List of purchases to calculate rewards for"
                }
            },
            "required": ["card_id", "purchases"]
        } 