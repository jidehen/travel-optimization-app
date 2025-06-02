import asyncio
import logging
from typing import Optional, Dict, Any
import requests
from smart_sdk.tools import StdioServerParams, mcp_server_tools
from smart_sdk.agents import SMARTLLMAgent
from smart_sdk import CancellationToken, Console
from smart_sdk.model import AzureOpenAIChatCompletionClient
from loguru import logger
import subprocess
import os
from pathlib import Path
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
TOKEN_URL = "https://agents-hub.dev.aws.jpmchase.net/smart-runtime/v1/utility/token"
DEFAULT_USER_SID = "D649217"
MODEL_CONFIG = {
    "model": "o3-mini-2025-01-31",
    "api_version": None,
    "azure_endpoint": None,
    "azure_deployment": None
}

# MCP Server Configuration
MCP_SERVERS = {
    "chase_travel": {
        "port": 3001,
        "path": "packages/mcp_servers/chase_travel/server.py"
    },
    "safepay_wallet": {
        "port": 3002,
        "path": "packages/mcp_servers/safepay_wallet/server.py"
    },
    "benefits": {
        "port": 3003,
        "path": "packages/mcp_servers/benefits/server.py"
    }
}

class ModelClientError(Exception):
    """Custom exception for model client errors."""
    pass

def fetch_model_config() -> Dict[str, Any]:
    """Fetch model configuration from the token service."""
    try:
        logger.info("Fetching model configuration from token service")
        response = requests.get(TOKEN_URL)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        error_msg = f"Failed to fetch model configuration: {str(e)}"
        logger.error(error_msg)
        raise ModelClientError(error_msg) from e

def create_model_client(model_details: Dict[str, Any]) -> AzureOpenAIChatCompletionClient:
    """Create an Azure OpenAI model client from configuration."""
    logger.debug("Creating model client with retrieved configuration")
    return AzureOpenAIChatCompletionClient(
        azure_deployment=model_details["model"],
        model=MODEL_CONFIG["model"],
        api_version=model_details["api_version"],
        azure_endpoint=model_details["base_url"],
        api_key=model_details["api_key"],
        default_headers={
            "Authorization": f"Bearer {model_details['token']}", 
            "user_sid": DEFAULT_USER_SID
        }
    )

async def start_mcp_servers() -> None:
    """Start all MCP servers using UV."""
    logger.info("Starting MCP servers using UV")
    
    # Create UV configuration
    uv_config = {
        "servers": [
            {
                "name": name,
                "command": "python",
                "args": [config["path"]],
                "env": {
                    "PORT": str(config["port"])
                }
            }
            for name, config in MCP_SERVERS.items()
        ]
    }
    
    # Write UV configuration
    config_path = Path("uv.json")
    with open(config_path, "w") as f:
        json.dump(uv_config, f, indent=2)
    
    # Start servers using UV
    try:
        subprocess.run(["uv", "start"], check=True)
        logger.info("Successfully started all MCP servers")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start MCP servers: {str(e)}")
        raise

async def setup_mcp_servers() -> Any:
    """Set up all MCP server parameters and tools."""
    logger.info("Setting up MCP server parameters")
    
    # Start servers if not already running
    await start_mcp_servers()
    
    # Set up server parameters
    server_params = {
        name: StdioServerParams(
            command="uv",
            args=["connect", name]
        )
        for name in MCP_SERVERS.keys()
    }
    
    logger.info("Initializing MCP server tools")
    tools = {}
    for name, params in server_params.items():
        server_tools = await mcp_server_tools(params)
        tools.update(server_tools)
    
    return tools

def create_agent(tools: Any) -> SMARTLLMAgent:
    """Create a SMART LLM agent with the given tools."""
    logger.info("Creating SMART LLM agent")
    model_details = fetch_model_config()
    model_client = create_model_client(model_details)
    
    return SMARTLLMAgent(
        name="TravelOptimizationAgent",
        description="An intelligent assistant specialized in travel optimization and rewards maximization",
        system_message="""You are a travel optimization expert assistant that helps users maximize their travel rewards and benefits. 
        Your capabilities include:
        1. Flight Search and Booking: Find the best flight options based on user preferences
        2. Payment Optimization: Recommend the best payment methods for maximum rewards
        3. Benefits Analysis: Analyze card benefits and calculate potential rewards
        4. Travel Planning: Help users plan trips while maximizing their rewards
        
        Always format your responses in a clear, structured manner:
        - Use bullet points for lists
        - Use tables for comparing options
        - Highlight key benefits and savings
        - Provide clear explanations for recommendations
        
        Be proactive in suggesting ways to maximize rewards and benefits.""",
        model_client=model_client,
        tools=tools,
        reflect_on_tool_use=True
    )

async def process_user_input(agent: SMARTLLMAgent, user_input: str) -> None:
    """Process user input and generate response using the agent."""
    try:
        logger.info(f"Processing user input: {user_input}")
        await Console(agent.run_stream(
            task=user_input,
            cancellation_token=CancellationToken()
        ))
    except Exception as e:
        logger.error(f"Error processing user input: {str(e)}", exc_info=True)
        print(f"An error occurred: {str(e)}")

async def run_conversation_loop(agent: SMARTLLMAgent) -> None:
    """Run the main conversation loop."""
    print("Welcome to the Travel Optimization Assistant! Type 'exit' or 'quit' to end the conversation.")
    
    while True:
        try:
            user_input = input("User: ").strip()
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                logger.info("User requested to end conversation")
                print("Ending conversation.")
                break
                
            await process_user_input(agent, user_input)
            
        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
            print("\nEnding conversation.")
            break

async def main() -> None:
    """Main entry point for the application."""
    try:
        logger.info("Starting application")
        tools = await setup_mcp_servers()
        agent = create_agent(tools)
        await run_conversation_loop(agent)
                
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up UV processes
        try:
            subprocess.run(["uv", "stop"], check=True)
            logger.info("Successfully stopped all MCP servers")
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to stop MCP servers: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 