import asyncio
import json
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client


class MCPCalculatorClient:
    def __init__(self):
        self.server_params = StdioServerParameters(
            command="python",
            args=["./server.py"],
            env=None,
        )

    async def run(self):
        """Run the MCP client and interact with the server."""
        print("Starting MCP Calculator Client...")

        try:
            async with stdio_client(self.server_params) as (read, write):
                async with ClientSession(read, write) as session:
                    print("Connecting to MCP server...")

                    await session.initialize()
                    print("Connected to MCP server successfully.")

                    await self.list_tools(session)

                    await self.test_calculator_operations(session)

                    await self.list_and_test_resources(session)

                    await self.test_greeting_resource(session)

                    print("All operations completed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    
    async def list_tools(self, session: ClientSession):
        """List available tools on the server."""
        print("\nListing available tools...")
        try:
            tools = await session.list_tools()
            for tool in tools:
                print(f" - {tool.name}: {tool.description}")
        except Exception as e:
            print(f"Error listing tools: {e}")

    async def test_calculator_operations(self, session: ClientSession):
        """Test basic calculator operations."""
        print("\nTesting calculator operations...")
        
        operations = [
            ("add", {"a": 5, "b": 3},"Adding 5 and 3"),
            ("subtract", {"a": 5, "b": 3}, "Subtracting 3 from 5"),
            ("multiply", {"a": 5, "b": 3}, "Multiplying 5 and 3"),
            ("divide", {"a": 5, "b": 3}, "Dividing 5 by 3"),
            ("help", {}, "Getting help information"),
        ]

        for tool_name, params, description in operations:
            print(f"\n{description}...")
            try:
                result = await session.call_tool(tool_name, params)
                result_text = self.extract_text_result(result)
                print(f"Result: {result_text}")
            except Exception as e:
                print(f"Error calling tool '{tool_name}': {e}")

    async def list_and_test_resources(self, session: ClientSession):
        """List available resources and test them."""
        print("\nListing available resources...")
        try:
            resources = await session.list_resources()
            for resource in resources:
                print(f" - {resource.name}: {resource.description}")
                print(f"    URI: {resource.uri}")

            if resources.resources:
                first_resource = resources.resources[0]
                print(f"\nReading resource '{first_resource.name}'...")
                try:
                    content = await session.read_resource(first_resource.uri)
                    print(f"Resource content: {content}")
                except Exception as e:
                    print(f"Error reading resource '{first_resource.name}': {e}")

        except Exception as e:
            print(f"Error listing resources: {e}")

    async def test_greeting_resource(self, session: ClientSession):
        """Test the greeting resource with a specific name."""
        name = "Alice"
        resource_uri = f"greeting://{name}"
        print(f"\nTesting greeting resource: {resource_uri}")
        try:
            content = await session.read_resource(resource_uri)
            content_text = self.extract_text_result(content)
            print(f"Greeting for {name}: {content_text}")
        except Exception as e:
            print(f"Error reading greeting resource for '{name}': {e}")

    def extract_text_result(self, result) -> str:
        """Extract text result from a ToolResult object."""
        try:
            if hasattr(result, "contents") and result.contents:
                for content_item in result.contents:
                    if hasattr(content_item, "text") and content_item.text:
                        return content_item.text
                    
            if hasattr(result, "content") and result.content:
                for content_item in result.content:
                    if hasattr(content_item, "text") and content_item.text:
                        return content_item.text
                    
            return str(result)  # Fallback to string representation if no text content found
        except Exception as e:
            return "No result"
        

async def main():
    """Main entry point for the MCP Calculator Client."""
    client = MCPCalculatorClient()
    await client.run()


if __name__ == "__main__":
    asyncio.run(main())