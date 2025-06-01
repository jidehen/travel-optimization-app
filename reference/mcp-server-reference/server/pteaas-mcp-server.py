import httpx
import logging
from typing import Union, List, Dict, Any
from functools import lru_cache
from mcp.server.fastmcp import FastMCP
from model.customer_profile_request import CustomerProfileRequest
from model.customer_profile_response import SimplifiedCustomerProfileResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
API_BASE_URL = "https://pteaas-syrphid-rls.test.aws.jpmchase.net/jpmc/customer/profile/party-account-relationships/fzbzesh2/syrphid/v2/relationships"
DEFAULT_TIMEOUT = 30.0
DEFAULT_HEADERS = {
    "Channel-Type": "PARTNER",
    "Trace-Id": "postman_test_traceId",
    "Environment-Database-Name": "db009",
    "Client-Id": "CC-111935-B054156-303503-UAT"
}

# Initialize FastMCP server
mcp = FastMCP("CustomerProfile")

@lru_cache(maxsize=128)
def get_headers(account_number: str, auth_token: str = "authorization") -> Dict[str, str]:
    """
    Generate headers for the API request with caching for performance.
    
    Args:
        account_number: The account number to include in the query params
        auth_token: The authorization token to use
        
    Returns:
        Dict[str, str]: The complete headers dictionary
    """
    return {
        **DEFAULT_HEADERS,
        "Authorization": f"Bearer {auth_token}",
        "Query-Params": f'{{"accountNumber":"{account_number}"}}'
    }

async def fetch_profile_data(client: httpx.AsyncClient, headers: Dict[str, str]) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Fetch profile data from the API.
    
    Args:
        client: The httpx client to use
        headers: The headers to include in the request
        
    Returns:
        Union[Dict[str, Any], List[Dict[str, Any]]]: The response data
        
    Raises:
        httpx.HTTPStatusError: If the API request fails
    """
    response = await client.get(API_BASE_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def create_simplified_response(data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[SimplifiedCustomerProfileResponse, List[SimplifiedCustomerProfileResponse]]:
    """
    Create simplified profile response objects from the API data.
    
    Args:
        data: The API response data
        
    Returns:
        Union[SimplifiedCustomerProfileResponse, List[SimplifiedCustomerProfileResponse]]: 
            The simplified profile response object(s)
    """
    def extract_fields(item: Dict[str, Any]) -> Dict[str, Any]:
        """Extract only the required fields from the response data."""
        return {
            "accountAliasName": item["accountAliasName"],
            "accountNumber": item["accountNumber"],
            "accountIdentifier": item["accountIdentifier"],
            "bankName": item["bankName"],
            "bankIdentifier": item["bankIdentifier"]
        }
    
    if isinstance(data, list):
        return [SimplifiedCustomerProfileResponse(**extract_fields(item)) for item in data]
    return SimplifiedCustomerProfileResponse(**extract_fields(data))

@mcp.tool()
async def fetch_customer_profile(request: CustomerProfileRequest) -> Union[SimplifiedCustomerProfileResponse, List[SimplifiedCustomerProfileResponse], Dict[str, str]]:
    """
    Fetch customer profile data for a given account number.
    Returns only essential fields: accountAliasName, accountNumber, accountIdentifier, bankName, and bankIdentifier.
    
    Args:
        request: The customer profile request containing the account number
        
    Returns:
        Union[SimplifiedCustomerProfileResponse, List[SimplifiedCustomerProfileResponse], Dict[str, str]]: 
            The simplified customer profile data or error response
    """
    logger.info(f"Fetching customer profile for account: {request.account_number}")
    
    headers = get_headers(request.account_number)
    logger.debug(f"Request headers: {headers}")

    async with httpx.AsyncClient(timeout=DEFAULT_TIMEOUT) as client:
        try:
            data = await fetch_profile_data(client, headers)
            logger.debug(f"Response data: {data}")
            
            response = create_simplified_response(data)
            logger.info(f"Retrieved {'multiple' if isinstance(response, list) else 'single'} customer profile(s)")
            
            return response

        except httpx.HTTPStatusError as e:
            error_msg = f"HTTP error {e.response.status_code}: {e.response.text}"
            logger.error(error_msg)
            return {"error": error_msg}
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return {"error": error_msg}

if __name__ == "__main__":
    logger.info("Starting CustomerProfile MCP server")
    mcp.run(transport="stdio")