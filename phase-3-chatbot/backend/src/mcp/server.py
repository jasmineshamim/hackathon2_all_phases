"""
MCP (Model Context Protocol) server initialization.
Provides tools for task management operations that the AI agent can invoke.
"""
from typing import List, Dict, Any

class MCPServer:
    """
    MCP Server for exposing task management tools to the AI agent.

    Tools are registered and made available for the OpenAI Agents SDK
    to invoke based on natural language understanding.
    """

    def __init__(self):
        """Initialize MCP server with empty tool registry."""
        self.tools: List[Dict[str, Any]] = []
        self._tool_functions: Dict[str, callable] = {}

    def register_tool(self, name: str, function: callable, schema: Dict[str, Any]):
        """
        Register a tool with the MCP server.

        Args:
            name: Tool name (e.g., "add_task")
            function: Async function to execute
            schema: JSON schema describing tool parameters
        """
        self.tools.append({
            "name": name,
            "function": function,
            "schema": schema
        })
        self._tool_functions[name] = function

    async def invoke_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a registered tool by name.

        Args:
            tool_name: Name of the tool to invoke
            parameters: Tool parameters

        Returns:
            Tool execution result

        Raises:
            ValueError: If tool not found
        """
        if tool_name not in self._tool_functions:
            raise ValueError(f"Tool '{tool_name}' not found")

        function = self._tool_functions[tool_name]
        return await function(**parameters)

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """
        Get all tool schemas for agent configuration.

        Returns:
            List of tool schemas
        """
        return [{"name": tool["name"], "schema": tool["schema"]} for tool in self.tools]

# Global MCP server instance
mcp_server = MCPServer()

# Register all task management tools
from src.mcp.tools.add_task import add_task
from src.mcp.tools.list_tasks import list_tasks
from src.mcp.tools.complete_task import complete_task
from src.mcp.tools.delete_task import delete_task
from src.mcp.tools.update_task import update_task
from src.mcp.schemas import (
    ADD_TASK_SCHEMA,
    LIST_TASKS_SCHEMA,
    COMPLETE_TASK_SCHEMA,
    DELETE_TASK_SCHEMA,
    UPDATE_TASK_SCHEMA
)

# Register tools with their schemas
mcp_server.register_tool("add_task", add_task, ADD_TASK_SCHEMA)
mcp_server.register_tool("list_tasks", list_tasks, LIST_TASKS_SCHEMA)
mcp_server.register_tool("complete_task", complete_task, COMPLETE_TASK_SCHEMA)
mcp_server.register_tool("delete_task", delete_task, DELETE_TASK_SCHEMA)
mcp_server.register_tool("update_task", update_task, UPDATE_TASK_SCHEMA)
