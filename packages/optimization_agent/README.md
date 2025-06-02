# Travel Optimization Agent

An intelligent agent that helps users maximize their travel rewards and benefits by connecting to multiple MCP servers.

## Features

- **Flight Search and Booking**: Find the best flight options based on user preferences
- **Payment Optimization**: Recommend the best payment methods for maximum rewards
- **Benefits Analysis**: Analyze card benefits and calculate potential rewards
- **Travel Planning**: Help users plan trips while maximizing their rewards

## Prerequisites

- Python 3.9+
- Smart SDK access
- Azure OpenAI API access
- All MCP servers running (Chase Travel, SafePay Wallet, Benefits)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Ensure all MCP servers are running:
- Chase Travel MCP Server (port 3001)
- SafePay Wallet MCP Server (port 3002)
- Benefits MCP Server (port 3003)

## Usage

Run the agent:
```bash
python agent.py
```

The agent will:
1. Connect to all MCP servers
2. Initialize the Smart SDK agent
3. Start an interactive conversation loop

## Response Format

The agent formats responses in a clear, structured manner:
- Bullet points for lists
- Tables for comparing options
- Highlighted key benefits and savings
- Clear explanations for recommendations

## Error Handling

The agent includes comprehensive error handling for:
- MCP server connection issues
- Model client errors
- User input processing
- Tool execution failures

## Logging

Logs are stored in:
- `logs/optimization_agent.log`
- Rotation: Daily
- Retention: 7 days
- Level: INFO 