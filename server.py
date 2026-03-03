from mcp.server.fastmcp import FastMCP
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mcp = FastMCP("Demo")


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@mcp.tool()
def subtract(a: int, b: int) -> int:
    """Subtract two numbers."""
    return a - b


@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@mcp.tool()
def divide(a: int, b: int) -> float:
    """Divide two numbers."""
    if b == 0:
        raise ValueError("division by zero")
    return a / b


@mcp.tool()
def help() -> str:
    """Get help information"""
    return "This server provides basic arithmetic operations: add, subtract, multiply, divide."


@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting message"""
    logger.debug(f"Registering resource: greeting://{name}")
    return f"Hello, {name}!"


if __name__ == "__main__":
    mcp.run()