import argparse
import json
import subprocess
import sys
import os
from pathlib import Path
from loguru import logger

# Configure logging
logger.add(
    "logs/server.log",
    rotation="1 day",
    retention="7 days",
    level="INFO"
)

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

def create_uv_config(server_name: str) -> None:
    """Create UV configuration for a single server."""
    if server_name not in MCP_SERVERS:
        raise ValueError(f"Unknown server: {server_name}. Available servers: {', '.join(MCP_SERVERS.keys())}")
    
    config = {
        "servers": [
            {
                "name": server_name,
                "command": "python",
                "args": [MCP_SERVERS[server_name]["path"]],
                "env": {
                    "PORT": str(MCP_SERVERS[server_name]["port"])
                }
            }
        ]
    }
    
    config_path = Path("uv.json")
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
    logger.info(f"Created UV configuration for {server_name}")

def start_server(server_name: str) -> None:
    """Start a single MCP server using UV."""
    try:
        create_uv_config(server_name)
        # Use uv run instead of uv start
        subprocess.run(["uv", "run", server_name], check=True)
        logger.info(f"Successfully started {server_name} server")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to start {server_name} server: {str(e)}")
        raise

def stop_server(server_name: str) -> None:
    """Stop a running MCP server using UV."""
    try:
        # Use uv kill instead of uv stop
        subprocess.run(["uv", "kill", server_name], check=True)
        logger.info(f"Successfully stopped {server_name} server")
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to stop {server_name} server: {str(e)}")
        raise

def main():
    parser = argparse.ArgumentParser(description="Manage MCP servers using UV")
    parser.add_argument(
        "action",
        choices=["start", "stop"],
        help="Action to perform (start or stop)"
    )
    parser.add_argument(
        "server",
        choices=list(MCP_SERVERS.keys()),
        help="Name of the server to manage"
    )
    
    args = parser.parse_args()
    
    if args.action == "start":
        start_server(args.server)
    else:
        stop_server(args.server)

if __name__ == "__main__":
    main() 