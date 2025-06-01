from pydantic import BaseModel, Field, ConfigDict

class CustomerProfileRequest(BaseModel):
    """
    Data model for customer profile requests.
    
    Attributes:
        account_number: The account number to fetch profile for.
            Must be a non-empty string.
    """
    account_number: str = Field(
        ...,
        description="The account number to fetch profile for",
        min_length=1,
        pattern=r"^\d+$"  # Ensure account number contains only digits
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account_number": "1234567890"
            }
        },
        str_strip_whitespace=True
    )