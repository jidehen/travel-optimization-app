# Travel Optimization Agent

An intelligent agent that helps users maximize their travel rewards and benefits by connecting to multiple MCP servers.

## Features

- **Flight Search and Booking**: Find the best flight options based on user preferences
- **Payment Optimization**: Recommend the best payment methods for maximum rewards
- **Benefits Analysis**: Analyze card benefits and calculate potential rewards
- **Travel Planning**: Help users plan trips while maximizing their rewards

## Prerequisites

- Python 3.12+
- Smart SDK access
- Azure OpenAI API access
- UV process manager

## Setup

1. Install dependencies:
```bash
uv pip install -e .
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

Run the agent:
```bash
uv run python agent.py
```

The agent will:
1. Connect to the MCP servers
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