"""AI agent service for natural language processing and MCP tool invocation."""
from typing import List, Dict, Any, Optional
import os
import json
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class AIAgentService:
    """Service for handling AI agent interactions with MCP tools."""

    def __init__(self):
        self.model = "gpt-4-turbo-preview"
        self.mcp_tools = self._discover_mcp_tools()

    def _discover_mcp_tools(self) -> List[Dict[str, Any]]:
        """Discover available MCP tools."""
        # In a real implementation, this would query the MCP server
        # For now, we'll define the tools based on our MCP tool definitions
        return [
            {
                "type": "function",
                "function": {
                    "name": "create_todo",
                    "description": "Creates a new todo item with the specified title and optional details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "title": {
                                "type": "string",
                                "description": "Title of the task"
                            },
                            "description": {
                                "type": "string",
                                "description": "Detailed description of the task"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Priority level of the task"
                            },
                            "due_date": {
                                "type": "string",
                                "description": "Due date in ISO 8601 format"
                            }
                        },
                        "required": ["title"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_todos",
                    "description": "Retrieves all todo items for the user, with optional filtering.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "status": {
                                "type": "string",
                                "enum": ["pending", "completed"],
                                "description": "Filter by status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "Filter by priority"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_todo",
                    "description": "Updates an existing todo item.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "New title"
                            },
                            "description": {
                                "type": "string",
                                "description": "New description"
                            },
                            "status": {
                                "type": "string",
                                "enum": ["pending", "completed"],
                                "description": "New status"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                                "description": "New priority"
                            }
                        },
                        "required": ["todo_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_todo",
                    "description": "Deletes a todo item by ID.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo to delete"
                            }
                        },
                        "required": ["todo_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "toggle_todo_status",
                    "description": "Toggles the status of a todo between pending and completed.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "ID of the todo to toggle"
                            }
                        },
                        "required": ["todo_id"]
                    }
                }
            }
        ]

    async def process_message(
        self,
        message: str,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        mcp_tool_executor: Any = None
    ) -> Dict[str, Any]:
        """Process a user message and return AI response with tool invocations."""
        # Build messages for OpenAI
        messages = conversation_history or []
        messages.append({"role": "user", "content": message})

        # Call OpenAI with function calling
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=self.mcp_tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message
        tool_calls = assistant_message.tool_calls

        # If AI wants to call tools
        if tool_calls:
            # Execute tool calls
            tool_results = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                # Execute the MCP tool
                if mcp_tool_executor:
                    result = await mcp_tool_executor(function_name, function_args)
                    tool_results.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": json.dumps(result)
                    })

            # Get final response with tool results
            messages.append(assistant_message)
            messages.extend(tool_results)

            final_response = client.chat.completions.create(
                model=self.model,
                messages=messages
            )

            return {
                "response": final_response.choices[0].message.content,
                "tool_calls": [
                    {
                        "function": tc.function.name,
                        "arguments": json.loads(tc.function.arguments)
                    }
                    for tc in tool_calls
                ],
                "tool_results": tool_results
            }
        else:
            # No tool calls, just return the response
            return {
                "response": assistant_message.content,
                "tool_calls": [],
                "tool_results": []
            }

    def format_response_for_chat(self, ai_response: Dict[str, Any]) -> str:
        """Format AI response for chat display."""
        response_text = ai_response.get("response", "")

        # Add information about tool calls if any
        tool_calls = ai_response.get("tool_calls", [])
        if tool_calls:
            actions = []
            for tc in tool_calls:
                function_name = tc["function"]
                if function_name == "create_todo":
                    actions.append("✓ Created a new todo")
                elif function_name == "list_todos":
                    actions.append("✓ Retrieved your todos")
                elif function_name == "update_todo":
                    actions.append("✓ Updated the todo")
                elif function_name == "delete_todo":
                    actions.append("✓ Deleted the todo")
                elif function_name == "toggle_todo_status":
                    actions.append("✓ Updated todo status")

            if actions:
                response_text = "\n".join(actions) + "\n\n" + response_text

        return response_text
