# Travel Optimization App

A Python-based travel optimization application that uses multiple MCP (Message Control Protocol) servers and a Smart SDK agent to optimize travel experiences.

## Project Structure

```
travel-optimization-app/
├── packages/
│   ├── mcp_servers/
│   │   ├── chase_travel/        # Chase Travel MCP server
│   │   ├── safepay_wallet/      # SafePay Wallet MCP server
│   │   └── benefits/            # Benefits MCP server
│   ├── optimization_agent/      # Smart SDK agent
│   └── shared/                  # Shared types and utilities
├── pyproject.toml               # Python project configuration
├── docker-compose.yml           # Development environment
└── README.md
```

## Requirements

- Python 3.11+
- Poetry for dependency management
- Docker and Docker Compose for development environment

## Setup

1. Install Poetry:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install dependencies:
```bash
poetry install
```

3. Start the development environment:
```bash
docker-compose up
```

## Development

Each MCP server is designed to be independently deployable and can be developed separately. The project uses Poetry workspaces to manage dependencies across packages.

### MCP Servers

- Chase Travel MCP: Port 8001
- SafePay Wallet MCP: Port 8002
- Benefits MCP: Port 8003

### Smart SDK Agent

The optimization agent uses the Smart SDK to coordinate between the MCP servers and optimize travel experiences.

## Notes

- The Smart SDK is an internal tool and will not be available for testing on personal machines
- Each MCP server is designed to be independently deployable
- Redis is used for caching and state management
- Type hints are used throughout the codebase 