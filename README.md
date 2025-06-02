# Travel Optimization Application

A modern travel optimization application that helps users maximize their travel rewards and benefits by connecting to multiple MCP servers.

## Project Structure

```
travel-optimization-app/
├── packages/
│   ├── mcp_servers/           # MCP servers for different functionalities
│   │   ├── chase_travel/     # Flight search functionality
│   │   ├── safepay_wallet/   # Payment methods management
│   │   └── benefits/         # Card benefits and rewards
│   ├── optimization_agent/   # Smart agent that connects to MCP servers
│   └── shared/              # Shared models and utilities
└── README.md
```

## Prerequisites

- Python 3.12+
- UV package manager
- Smart SDK access
- Azure OpenAI API access

## Setup

1. Install UV:
```bash
pip install uv
```

2. Create and activate virtual environment:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Running the Application

1. Start the MCP servers:
```bash
# Chase Travel MCP
cd packages/mcp_servers/chase_travel
uv run python -m uvicorn chase_travel.server:app --port 8001

# SafePay Wallet MCP
cd packages/mcp_servers/safepay_wallet
uv run python -m uvicorn safepay_wallet.server:app --port 8002

# Benefits MCP
cd packages/mcp_servers/benefits
uv run python -m uvicorn benefits.server:app --port 8003
```

2. Run the optimization agent:
```bash
cd packages/optimization_agent
uv run python agent.py
```

## Development

Each MCP server is designed to be independently deployable and can be developed separately. The project uses UV for dependency management across packages.

### Health Checks

Each MCP server has a health check endpoint:
- Chase Travel: http://localhost:8001/health
- SafePay Wallet: http://localhost:8002/health
- Benefits: http://localhost:8003/health

### Logging

Logs are stored in the `logs` directory for each component:
- `logs/chase_travel_mcp.log`
- `logs/safepay_wallet_mcp.log`
- `logs/benefits_mcp.log`
- `logs/optimization_agent.log`

Logs are rotated daily and retained for 7 days. 