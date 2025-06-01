# MCP Server Reference Implementation

This directory contains a reference implementation of an MCP (Message Control Protocol) server for customer profile management. This code serves as a template and learning resource for future MCP server implementations.

## Structure

```
mcp-server-reference/
├── model/
│   ├── customer_profile_request.py    # Request model with validation
│   └── customer_profile_response.py   # Response models (full and simplified)
├── server/
│   └── pteaas-mcp-server.py          # Main server implementation
└── README.md                         # This file
```

## Key Features

1. **Modern Python Practices**
   - Type hints throughout
   - Async/await patterns
   - Pydantic v2 models
   - Functional programming approach

2. **Error Handling**
   - Comprehensive error handling
   - Custom exceptions
   - Proper error logging
   - Error context preservation

3. **Performance Optimizations**
   - Caching with `@lru_cache`
   - Async HTTP client
   - Resource management
   - Timeout handling

4. **Code Organization**
   - Separation of concerns
   - Modular design
   - Clear function responsibilities
   - Comprehensive documentation

## Usage Examples

### Basic Server Setup
```python
from mcp.server.fastmcp import FastMCP

# Initialize server
mcp = FastMCP("ServiceName")

# Define tool
@mcp.tool()
async def my_tool(request: RequestModel) -> ResponseModel:
    # Implementation
    pass

# Run server
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Model Definition
```python
from pydantic import BaseModel, Field, ConfigDict

class MyModel(BaseModel):
    field: str = Field(..., description="Field description")
    
    model_config = ConfigDict(
        json_schema_extra={"example": {"field": "value"}},
        str_strip_whitespace=True
    )
```

### HTTP Client Usage
```python
async with httpx.AsyncClient(timeout=30.0) as client:
    response = await client.get(url, headers=headers)
    data = response.json()
```

## Best Practices Demonstrated

1. **Logging**
   - Structured logging
   - Different log levels
   - Context in log messages
   - File and line numbers

2. **Type Safety**
   - Comprehensive type hints
   - Return type annotations
   - Generic types
   - Union types for flexibility

3. **Error Handling**
   - Try-except blocks
   - Custom exceptions
   - Error context
   - Proper error messages

4. **Code Organization**
   - Small, focused functions
   - Clear responsibilities
   - Proper documentation
   - Consistent style

## Notes

- This is a reference implementation and should be adapted based on specific needs
- The code demonstrates patterns that can be reused in other MCP server implementations
- Error handling and logging patterns are particularly valuable for production code
- The model structure shows how to handle both full and simplified responses 