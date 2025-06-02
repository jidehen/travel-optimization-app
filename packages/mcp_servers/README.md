# MCP Servers

This directory contains three independent MCP (Model Context Protocol) servers that provide specialized functionality for the travel optimization application.

## Servers

### 1. Chase Travel MCP Server (Port 8001)
- **Purpose**: Flight search functionality
- **Tools**:
  - `search_flights`: Search for available flights
  - `get_flight_details`: Get detailed flight information

### 2. SafePay Wallet MCP Server (Port 8002)
- **Purpose**: Payment methods management
- **Tools**:
  - `get_payment_methods`: Retrieve user's payment methods
  - `add_payment_method`: Add a new payment method

### 3. Benefits MCP Server (Port 8003)
- **Purpose**: Card benefits and rewards
- **Tools**:
  - `get_benefits`: Get available card benefits
  - `calculate_rewards`: Calculate potential rewards for purchases

## Development

Each server is independently runnable and has its own:
- Configuration
- Dependencies
- Logging
- Health checks

### Prerequisites
- Python 3.12+
- UV process manager

### Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
# Using requirements.txt
pip install -r requirements.txt

# Or using pyproject.toml
pip install .
```

3. Set up environment variables:
```bash
# Copy example env file
cp .env.example .env
# Edit .env with your configuration
```

### Running Locally

Start individual servers:
```bash
# Chase Travel MCP
cd chase_travel
uv run python -m uvicorn chase_travel.server:app --port 8001

# SafePay Wallet MCP
cd safepay_wallet
uv run python -m uvicorn safepay_wallet.server:app --port 8002

# Benefits MCP
cd benefits
uv run python -m uvicorn benefits.server:app --port 8003
```

### Health Checks
Each server has a health check endpoint:
- Chase Travel: http://localhost:8001/health
- SafePay Wallet: http://localhost:8002/health
- Benefits: http://localhost:8003/health

## Future Separation

These servers are designed to be easily separated into individual repositories. Each server:
- Has its own dependencies
- Uses environment variables for configuration
- Has independent logging
- Can be deployed separately

## Logging

Logs are stored in the `logs` directory for each server:
- `logs/chase_travel_mcp.log`
- `logs/safepay_wallet_mcp.log`
- `logs/benefits_mcp.log`

Logs are rotated daily and retained for 7 days.

## Dependencies

Each server can be installed using either:
- `requirements.txt` for pip installation
- `pyproject.toml` for modern Python packaging

Both methods provide the same dependencies:
- FastAPI for the web server
- Uvicorn for ASGI server
- Pydantic for data validation
- Python-dotenv for environment variables
- Loguru for logging
- HTTPX for async HTTP client
- MCP for Model Context Protocol support 