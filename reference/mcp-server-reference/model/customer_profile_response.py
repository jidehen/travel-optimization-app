from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class AccountInfo(BaseModel):
    """Account information fields."""
    accountAliasName: str = Field(..., description="Display name for the account")
    accountNumber: str = Field(..., description="Unique identifier for the account")
    accountOpenDate: str = Field(..., description="Date when the account was opened")
    accountStatusChangeDate: str = Field(..., description="Last status change date")

class ProductInfo(BaseModel):
    """Product information fields."""
    accountProductClassificationCode: str = Field(..., description="Product classification code")
    accountProductClassificationName: str = Field(..., description="Product classification name")
    productCode: str = Field(..., description="Product code")
    productName: str = Field(..., description="Product name")
    subProductCode: str = Field(..., description="Sub-product code")
    subProductName: str = Field(..., description="Sub-product name")

class RelationshipInfo(BaseModel):
    """Relationship information fields."""
    accountRelationshipCode: str = Field(..., description="Relationship code")
    accountRelationshipName: str = Field(..., description="Relationship name")
    accountRelationshipStartDate: str = Field(..., description="Relationship start date")
    accountDirectRelationships: Optional[str] = Field(None, description="Direct relationship information")

class IdentifierInfo(BaseModel):
    """Identifier information fields."""
    accountIdentifier: str = Field(..., description="Account identifier")
    accountOwnerEnterprisePartyIdentifier: str = Field(..., description="Owner party identifier")
    enterprisePartyIdentifier: str = Field(..., description="Enterprise party identifier")
    relationshipIdentifier: str = Field(..., description="Relationship identifier")
    tokenIdentifier: Optional[str] = Field(None, description="Token identifier")

class BankInfo(BaseModel):
    """Bank information fields."""
    bankIdentifier: str = Field(..., description="Bank identifier")
    bankName: str = Field(..., description="Bank name")

class StatusInfo(BaseModel):
    """Status and classification information fields."""
    lifeCycleStatusCode: str = Field(..., description="Life cycle status code")
    alternateCategoryProductCode: str = Field(..., description="Alternate category product code")
    alternateCategoryProductName: str = Field(..., description="Alternate category product name")
    costCenterCode: str = Field(..., description="Cost center code")

class PermissionInfo(BaseModel):
    """Permission code fields."""
    balanceInquiryAccountPermissionCode: str = Field(..., description="Balance inquiry permission")
    statementReconciliationAccountPermissionCode: str = Field(..., description="Statement reconciliation permission")
    stopPaymentAccountPermissionCode: str = Field(..., description="Stop payment permission")
    transferFromAccountPermissionCode: str = Field(..., description="Transfer from permission")
    transferToAccountPermissionCode: str = Field(..., description="Transfer to permission")
    webAccessAccountPermissionCode: str = Field(..., description="Web access permission")
    ivrAccessAccountPermissionCode: str = Field(..., description="IVR access permission")
    balanceAutomaticPlayAccountPermissionCode: str = Field(..., description="Balance automatic play permission")
    onlineTradingAccountPermissionCode: str = Field(..., description="Online trading permission")
    dividendReinvestmentAccountPermissionCode: str = Field(..., description="Dividend reinvestment permission")
    securityTransferFromAccountPermissionCode: str = Field(..., description="Security transfer from permission")
    securityTransferToAccountPermissionCode: str = Field(..., description="Security transfer to permission")
    automatedTellerMachineAccessAccountPermissionCode: str = Field(..., description="ATM access permission")

class CustomerProfileResponse(BaseModel):
    """
    Data model for customer profile responses.
    
    This model represents the complete customer profile information including
    account details, permissions, and relationship information.
    """
    account: AccountInfo
    product: ProductInfo
    relationship: RelationshipInfo
    identifiers: IdentifierInfo
    bank: BankInfo
    status: StatusInfo
    permissions: PermissionInfo
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "account": {
                    "accountAliasName": "My Checking",
                    "accountNumber": "1234567890",
                    "accountOpenDate": "2023-01-01",
                    "accountStatusChangeDate": "2023-01-01"
                },
                "product": {
                    "accountProductClassificationCode": "CHK",
                    "accountProductClassificationName": "Checking",
                    "productCode": "CHK001",
                    "productName": "Basic Checking",
                    "subProductCode": "CHK001A",
                    "subProductName": "Basic Checking Plus"
                },
                "relationship": {
                    "accountRelationshipCode": "OWN",
                    "accountRelationshipName": "Owner",
                    "accountRelationshipStartDate": "2023-01-01",
                    "accountDirectRelationships": None
                },
                "identifiers": {
                    "accountIdentifier": "ACC123",
                    "accountOwnerEnterprisePartyIdentifier": "OWN123",
                    "enterprisePartyIdentifier": "ENT123",
                    "relationshipIdentifier": "REL123",
                    "tokenIdentifier": None
                },
                "bank": {
                    "bankIdentifier": "BANK123",
                    "bankName": "Example Bank"
                },
                "status": {
                    "lifeCycleStatusCode": "ACTIVE",
                    "alternateCategoryProductCode": "ALT001",
                    "alternateCategoryProductName": "Alternate Product",
                    "costCenterCode": "CC001"
                },
                "permissions": {
                    "balanceInquiryAccountPermissionCode": "Y",
                    "statementReconciliationAccountPermissionCode": "Y",
                    "stopPaymentAccountPermissionCode": "Y",
                    "transferFromAccountPermissionCode": "Y",
                    "transferToAccountPermissionCode": "Y",
                    "webAccessAccountPermissionCode": "Y",
                    "ivrAccessAccountPermissionCode": "Y",
                    "balanceAutomaticPlayAccountPermissionCode": "Y",
                    "onlineTradingAccountPermissionCode": "Y",
                    "dividendReinvestmentAccountPermissionCode": "Y",
                    "securityTransferFromAccountPermissionCode": "Y",
                    "securityTransferToAccountPermissionCode": "Y",
                    "automatedTellerMachineAccessAccountPermissionCode": "Y"
                }
            }
        },
        str_strip_whitespace=True
    )

class SimplifiedCustomerProfileResponse(BaseModel):
    """
    Simplified data model for customer profile responses containing only essential fields.
    
    Attributes:
        accountAliasName: Display name for the account
        accountNumber: Unique identifier for the account
        accountIdentifier: Account identifier
        bankName: Name of the bank
        bankIdentifier: Bank identifier
    """
    accountAliasName: str = Field(..., description="Display name for the account")
    accountNumber: str = Field(..., description="Unique identifier for the account")
    accountIdentifier: str = Field(..., description="Account identifier")
    bankName: str = Field(..., description="Name of the bank")
    bankIdentifier: str = Field(..., description="Bank identifier")
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "accountAliasName": "My Checking",
                "accountNumber": "1234567890",
                "accountIdentifier": "ACC123",
                "bankName": "Example Bank",
                "bankIdentifier": "BANK123"
            }
        },
        str_strip_whitespace=True
    )
