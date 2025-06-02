from typing import List
from mcp import Tool, ToolContext
from shared.models.api.payment_methods import (
    PaymentMethodsResponse,
    Card
)

class GetPaymentMethodsTool(Tool):
    """Tool for retrieving user's payment methods."""
    
    name = "get_payment_methods"
    description = "Get all payment methods associated with a user"
    
    async def execute(self, context: ToolContext, **kwargs) -> dict:
        try:
            user_id = kwargs.get("user_id")
            if not user_id:
                raise ValueError("User ID is required")
            
            # TODO: Implement actual payment methods retrieval logic
            # This is a mock implementation
            mock_cards = [
                Card(
                    card_id="card_123",
                    type="CREDIT",
                    last_four_digits="1234",
                    expiry_month=12,
                    expiry_year=2025,
                    cardholder_name="John Doe",
                    is_default=True
                ),
                Card(
                    card_id="card_456",
                    type="DEBIT",
                    last_four_digits="5678",
                    expiry_month=6,
                    expiry_year=2026,
                    cardholder_name="John Doe",
                    is_default=False
                )
            ]
            
            response = PaymentMethodsResponse(
                cards=mock_cards,
                total_count=len(mock_cards)
            )
            
            return response.model_dump()
            
        except ValueError as e:
            raise ValueError(f"Invalid input parameters: {str(e)}")
        except Exception as e:
            raise Exception(f"Error retrieving payment methods: {str(e)}")
    
    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User ID for authentication"
                }
            },
            "required": ["user_id"]
        } 