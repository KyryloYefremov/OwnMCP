import asyncio
import logging
from mcp.server import Server
from mcp.server.stdio import stdio_server

from mcp.types import Tool, TextContent

from tools import tools


# Configure logging to stderr (never use stdout for logging in stdio servers)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Create the server
server = Server("example-stdio-server")


@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List available tools"""
    tool_list = []
    print(tools)

    for tool in tools.values():
        tool_list.append(
            Tool(
                name=tool["name"],
                description=tool["description"],
                inputSchema=tool["input_schema"].model_json_schema(),
            )
        )
    return tool_list


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, str] | None
) -> list[TextContent]:
    
    # tools is a dictionary with tool names as keys
    if name not in tools:
        raise ValueError(f"Unknown tool: {name}")
    
    tool = tools[name]

    result = "default"
    try:
        # invoke the tool
        result = await tool["handler"](arguments)
    except Exception as e:
        raise ValueError(f"Error calling tool {name}: {str(e)}")

    return [
        TextContent(type="text", text=str(result))
    ] 

async def main():
    """Main server function using stdio transport"""
    logger.info("Starting MCP stdio server...")
    
    try:
        # Use stdio transport
        async with stdio_server() as (read_stream, write_stream):
            logger.info("Server connected via stdio transport")
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options()
            )
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())