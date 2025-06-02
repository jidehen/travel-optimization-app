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
import sys
import time
import signal
from dotenv import load_dotenv

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# Load environment variables
load_dotenv()

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# Constants
TOKEN_URL = "https://agents-hub.dev.aws.jpmchase.net/smart-runtime/v1/utility/token"
DEFAULT_USER_SID = "D649217"
MODEL_CONFIG = {
    "model": "o3-mini-2025-01-31",
    "api_version": None,
    "azure_endpoint": None,
    "azure_deployment": None
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

class MCPServerManager:
    """Manages the lifecycle of MCP servers."""
    
    def __init__(self):
        self.servers = {
            "chase_travel": {
                "name": "Chase Travel MCP",
                "port": 8001,
                "path": project_root / "packages/mcp_servers/chase_travel"
            },
            "safepay_wallet": {
                "name": "SafePay Wallet MCP",
                "port": 8002,
                "path": project_root / "packages/mcp_servers/safepay_wallet"
            },
            "benefits": {
                "name": "Benefits MCP",
                "port": 8003,
                "path": project_root / "packages/mcp_servers/benefits"
            }
        }
        self.processes: Dict[str, subprocess.Popen] = {}
    
    def start_servers(self) -> None:
        """Start all MCP servers."""
        for server_id, server in self.servers.items():
            try:
                logger.info(f"Starting {server['name']}...")
                # Use uv run to start the server
                process = subprocess.Popen(
                    ["uv", "run", "--project", str(server["path"]), "python", "-m", "uvicorn", f"{server_id}.server:app", "--port", str(server["port"])],
                    cwd=str(server["path"]),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                self.processes[server_id] = process
                logger.info(f"{server['name']} started on port {server['port']}")
            except Exception as e:
                logger.error(f"Failed to start {server['name']}: {str(e)}")
                self.stop_servers()
                raise
    
    def stop_servers(self) -> None:
        """Stop all running MCP servers."""
        for server_id, process in self.processes.items():
            try:
                logger.info(f"Stopping {self.servers[server_id]['name']}...")
                # Send SIGTERM to the process
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    # If process doesn't terminate gracefully, force kill it
                    process.kill()
                logger.info(f"{self.servers[server_id]['name']} stopped")
            except Exception as e:
                logger.error(f"Error stopping {self.servers[server_id]['name']}: {str(e)}")
        
        self.processes.clear()

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
        server_manager = MCPServerManager()
        server_manager.start_servers()
        
        # Initialize MCP server tools
        tools = {}
        for server_id, server in server_manager.servers.items():
            server_params = StdioServerParams(
                command="uv",
                args=["run", "--project", str(server["path"]), "python", "-m", "uvicorn", f"{server_id}.server:app", "--port", str(server["port"])]
            )
            server_tools = await mcp_server_tools(server_params)
            tools.update(server_tools)
        
        agent = create_agent(tools)
        await run_conversation_loop(agent)
                
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        print(f"An error occurred: {str(e)}")
    finally:
        # Clean up UV processes
        server_manager.stop_servers()
        logger.info("Successfully stopped all MCP servers")

if __name__ == "__main__":
    asyncio.run(main()) 