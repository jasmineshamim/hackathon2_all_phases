"""
Chat agent initialization using OpenAI Agents SDK.
Handles natural language processing and tool invocation.
"""
import os
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from src.agents.prompts import SYSTEM_PROMPT, HELP_PROMPT
from src.mcp.server import mcp_server

class ChatAgent:
    """
    AI chat agent for task management conversations.

    Uses OpenAI's GPT model to understand natural language and invoke
    appropriate MCP tools for task operations.
    """

    def __init__(self):
        """Initialize chat agent with OpenAI client and tools."""
        api_key = os.getenv("OPENAI_API_KEY")
        # Enable mock mode if explicitly set or if no API key
        self.mock_mode = os.getenv("CHAT_MOCK_MODE", "false").lower() == "true" or not api_key

        if not api_key:
            # Don't fail at initialization - will use mock mode
            self.client = None
        else:
            self.client = AsyncOpenAI(api_key=api_key)
        # Use gpt-4o-mini for better availability and cost efficiency
        # Alternative models: "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.tools = mcp_server.get_tool_schemas()

    async def process_message(
        self,
        messages: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Process a chat message and generate response.

        Args:
            messages: Conversation history including new message
            user_id: Authenticated user's ID for tool invocations

        Returns:
            dict: {
                "response": str,  # Agent's text response
                "tool_calls": List[dict]  # Tools invoked during processing
            }
        """
        # Add system prompt if not present
        if not messages or messages[0].get("role") != "system":
            messages.insert(0, {
                "role": "system",
                "content": SYSTEM_PROMPT
            })

        # Check for help request
        last_message = messages[-1].get("content", "").lower()
        if "help" in last_message and len(last_message.split()) <= 3:
            return {
                "response": HELP_PROMPT,
                "tool_calls": []
            }

        try:
            # Use mock mode if enabled or if OpenAI client is unavailable
            if self.mock_mode or not self.client:
                return await self._mock_response(messages, user_id)

            # Call OpenAI API with tools
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )

            message = response.choices[0].message
            tool_calls_made = []

            # Process tool calls if any
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = eval(tool_call.function.arguments)  # Parse JSON string

                    # Add user_id to tool arguments
                    tool_args["user_id"] = user_id

                    # Invoke tool via MCP server
                    try:
                        result = await mcp_server.invoke_tool(tool_name, tool_args)
                        tool_calls_made.append({
                            "tool": tool_name,
                            "parameters": tool_args,
                            "result": result
                        })
                    except Exception as e:
                        tool_calls_made.append({
                            "tool": tool_name,
                            "parameters": tool_args,
                            "error": str(e)
                        })

                # Get final response after tool execution
                messages.append({
                    "role": "assistant",
                    "content": message.content or "",
                    "tool_calls": [
                        {
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        }
                        for tc in message.tool_calls
                    ]
                })

                # Add tool results to conversation
                for i, tool_call in enumerate(message.tool_calls):
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(tool_calls_made[i].get("result", tool_calls_made[i].get("error")))
                    })

                # Get final natural language response
                final_response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )

                return {
                    "response": final_response.choices[0].message.content,
                    "tool_calls": tool_calls_made
                }
            else:
                # No tools called, return direct response
                return {
                    "response": message.content,
                    "tool_calls": []
                }

        except Exception as e:
            # If OpenAI API fails, fall back to mock mode
            error_msg = str(e).lower()
            error_type = type(e).__name__

            # Check for OpenAI API errors (401, 404, quota, rate limit, etc.)
            if any(keyword in error_msg for keyword in ['401', '404', 'quota', 'insufficient_quota', 'not found', 'rate limit', 'incorrect api key', 'authentication']) or \
               any(keyword in error_type.lower() for keyword in ['notfound', 'ratelimit', 'apierror', 'authentication']):
                # Automatically switch to mock mode for this request
                print(f"[CHAT_AGENT] OpenAI API error detected: {error_type} - {error_msg[:100]}")
                print("[CHAT_AGENT] Falling back to mock mode")
                return await self._mock_response(messages, user_id)

            print(f"[CHAT_AGENT] Unexpected error: {error_type} - {error_msg[:100]}")
            return {
                "response": f"I encountered an error processing your request. Please try again or rephrase your message.",
                "tool_calls": [],
                "error": str(e)
            }

    async def _mock_response(
        self,
        messages: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Generate responses and invoke real MCP tools when OpenAI API is unavailable.

        Args:
            messages: Conversation history
            user_id: User ID for tool invocations

        Returns:
            dict: Response with actual tool invocation results
        """
        # Get the last user message
        last_message = messages[-1].get("content", "").lower()
        tool_calls_made = []

        # Greetings
        if any(word in last_message for word in ["hello", "hi", "hey"]) and len(last_message.split()) <= 3:
            return {
                "response": "Hello! I'm your AI Task Assistant. I can help you manage your tasks. Try asking me to:\n\n• Create a new task\n• Show your tasks\n• Mark a task as complete\n• Delete a task\n\nWhat would you like to do?",
                "tool_calls": []
            }

        # Help
        elif any(word in last_message for word in ["help", "what can you do"]):
            return {
                "response": HELP_PROMPT,
                "tool_calls": []
            }

        # Create task - ACTUALLY invoke the MCP tool
        elif "create" in last_message or "add" in last_message or "remember" in last_message or "note" in last_message:
            # Extract task title from message
            task_title = "New Task"

            # Try to extract meaningful task description
            for keyword in ["create a task", "add a task", "create task", "add task", "remember to", "note down", "i need to remember", "create", "add"]:
                if keyword in last_message:
                    parts = last_message.split(keyword, 1)
                    if len(parts) > 1:
                        task_title = parts[1].strip().strip("to ").strip(".,!?")
                        if task_title:
                            break

            if not task_title or task_title == "New Task":
                # Fallback: use everything after common words
                words = last_message.split()
                if len(words) > 2:
                    task_title = " ".join(words[2:]).strip(".,!?")

            # Invoke the actual add_task MCP tool
            try:
                result = await mcp_server.invoke_tool("add_task", {
                    "title": task_title,
                    "user_id": user_id
                })
                tool_calls_made.append({
                    "tool": "add_task",
                    "parameters": {"title": task_title, "user_id": user_id},
                    "result": result
                })
                return {
                    "response": f"✓ I've created a new task: '{task_title}'. You can view all your tasks by asking me to show them.",
                    "tool_calls": tool_calls_made
                }
            except Exception as e:
                return {
                    "response": f"I tried to create the task '{task_title}' but encountered an error: {str(e)}",
                    "tool_calls": []
                }

        # List tasks - ACTUALLY invoke the MCP tool
        elif "show" in last_message or "list" in last_message or "my tasks" in last_message or "view" in last_message or "what" in last_message or "pending" in last_message or "remaining" in last_message:
            # Determine status filter
            status = "all"
            if "completed" in last_message or "finished" in last_message or "done" in last_message:
                status = "completed"
            elif "pending" in last_message or "remaining" in last_message or "left" in last_message or "not completed" in last_message:
                status = "pending"

            try:
                result = await mcp_server.invoke_tool("list_tasks", {"user_id": user_id, "status": status})
                tool_calls_made.append({
                    "tool": "list_tasks",
                    "parameters": {"user_id": user_id, "status": status},
                    "result": result
                })

                # Format the tasks nicely
                # list_tasks returns {"tasks": [...], "count": ...}
                tasks = result.get("tasks", []) if isinstance(result, dict) else []
                if tasks and len(tasks) > 0:
                    task_list = "\n".join([
                        f"Task {task.get('id')}: {task.get('title', 'Untitled')} - {'✓ Completed' if task.get('completed') else 'Not completed'}"
                        for task in tasks
                    ])
                    status_text = f" ({status})" if status != "all" else ""
                    response = f"Here are your tasks{status_text}:\n\n{task_list}"
                else:
                    response = f"You don't have any {status} tasks yet. Try creating one by saying 'create a task to buy groceries'."

                return {
                    "response": response,
                    "tool_calls": tool_calls_made
                }
            except Exception as e:
                return {
                    "response": f"I tried to retrieve your tasks but encountered an error: {str(e)}",
                    "tool_calls": []
                }

        # Complete task - ACTUALLY invoke the MCP tool
        elif "complete" in last_message or "done" in last_message or "finish" in last_message or "mark" in last_message:
            # Try to extract task ID or title
            import re
            task_id_match = re.search(r'\b(\d+)\b', last_message)

            if task_id_match:
                task_id = int(task_id_match.group(1))
                try:
                    result = await mcp_server.invoke_tool("complete_task", {
                        "task_id": task_id,
                        "user_id": user_id
                    })
                    tool_calls_made.append({
                        "tool": "complete_task",
                        "parameters": {"task_id": task_id, "user_id": user_id},
                        "result": result
                    })
                    return {
                        "response": f"✓ I've marked task #{task_id} as complete! Great job on finishing it.",
                        "tool_calls": tool_calls_made
                    }
                except Exception as e:
                    return {
                        "response": f"I tried to complete task #{task_id} but encountered an error: {str(e)}",
                        "tool_calls": []
                    }
            else:
                return {
                    "response": "Please specify which task you want to mark as complete. For example: 'mark task 1 as complete' or 'complete task 2'.",
                    "tool_calls": []
                }

        # Update task - ACTUALLY invoke the MCP tool
        elif "update" in last_message or "change" in last_message or "rename" in last_message or "modify" in last_message:
            # Try to extract task ID
            import re
            task_id_match = re.search(r'\btask\s+(\d+)\b', last_message)

            if task_id_match:
                task_id = int(task_id_match.group(1))
                # Extract new title after "to" or similar keywords
                new_title = None
                for keyword in [" to ", " to'", ' to"']:
                    if keyword in last_message:
                        parts = last_message.split(keyword, 1)
                        if len(parts) > 1:
                            new_title = parts[1].strip().strip("'\".,!?")
                            break

                if new_title:
                    try:
                        result = await mcp_server.invoke_tool("update_task", {
                            "task_id": task_id,
                            "title": new_title,
                            "user_id": user_id
                        })
                        tool_calls_made.append({
                            "tool": "update_task",
                            "parameters": {"task_id": task_id, "title": new_title, "user_id": user_id},
                            "result": result
                        })
                        return {
                            "response": f"✓ I've updated task #{task_id} to '{new_title}'.",
                            "tool_calls": tool_calls_made
                        }
                    except Exception as e:
                        return {
                            "response": f"I tried to update task #{task_id} but encountered an error: {str(e)}",
                            "tool_calls": []
                        }
                else:
                    return {
                        "response": "Please specify what you want to change the task to. For example: 'update task 1 to Buy organic groceries'.",
                        "tool_calls": []
                    }
            else:
                return {
                    "response": "Please specify which task you want to update. For example: 'update task 1 to Buy organic groceries'.",
                    "tool_calls": []
                }

        # Delete task - ACTUALLY invoke the MCP tool
        elif "delete" in last_message or "remove" in last_message:
            # Try to extract task ID
            import re
            task_id_match = re.search(r'\btask\s+(\d+)\b', last_message)
            if not task_id_match:
                task_id_match = re.search(r'\b(\d+)\b', last_message)

            if task_id_match:
                task_id = int(task_id_match.group(1))
                try:
                    result = await mcp_server.invoke_tool("delete_task", {
                        "task_id": task_id,
                        "user_id": user_id
                    })
                    tool_calls_made.append({
                        "tool": "delete_task",
                        "parameters": {"task_id": task_id, "user_id": user_id},
                        "result": result
                    })
                    return {
                        "response": f"✓ I've deleted task #{task_id}. It's been removed from your list.",
                        "tool_calls": tool_calls_made
                    }
                except Exception as e:
                    return {
                        "response": f"I tried to delete task #{task_id} but encountered an error: {str(e)}",
                        "tool_calls": []
                    }
            else:
                return {
                    "response": "Please specify which task you want to delete. For example: 'delete task 17' or 'remove task 18'.",
                    "tool_calls": []
                }

        else:
            # Default response for unrecognized queries
            return {
                "response": "I can help you with:\n\n• Creating tasks (e.g., 'create a task to buy groceries')\n• Listing tasks (e.g., 'show my tasks')\n• Completing tasks (e.g., 'mark task 1 as complete')\n• Deleting tasks (e.g., 'delete task 2')\n\nWhat would you like to do?",
                "tool_calls": []
            }

# Global chat agent instance
chat_agent = ChatAgent()
