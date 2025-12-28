"""
MODULE 01: Core Concepts - HANDS-ON EXAMPLES
==============================================

Source: https://github.com/microsoft/mcp-for-beginners/blob/main/01-CoreConcepts/README.md
Study Guide: Module_01_Core_Concepts.md

This file demonstrates MCP core concepts through detailed code examples.
You'll build simplified but functional implementations of each concept.

EXAMPLES:
1. Three Server Primitives in Action
2. Complete Tool Implementation
3. Complete Resource Implementation
4. Complete Prompt Implementation
5. Client Primitives - Sampling, Elicitation, Logging
6. JSON-RPC Message Handling
7. stdio Transport Simulation
8. HTTP Transport Simulation
9. Complete Session Lifecycle
10. Multi-Server Architecture
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import json
import time
from datetime import datetime

print("=" * 80)
print("MODULE 01: MCP CORE CONCEPTS - HANDS-ON EXAMPLES")
print("=" * 80)
print("Building the foundational components of MCP")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: Three Server Primitives - Complete Implementation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Three Server Primitives - Tools, Resources, Prompts")
print("=" * 80)
print("""
CONCEPT: Every MCP server can provide three types of primitives:
1. Tools - Actions to execute
2. Resources - Data to read
3. Prompts - Templates to use

LOGIC:
- Server maintains registries for each primitive type
- Client can discover what's available
- Each primitive has specific access patterns
""")

# Tool definition
@dataclass
class Tool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]  # JSON Schema for parameters

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }

# Resource definition
@dataclass
class Resource:
    """MCP Resource definition"""
    uri: str
    name: str
    description: str
    mime_type: str

    def to_dict(self) -> dict:
        return {
            "uri": self.uri,
            "name": self.name,
            "description": self.description,
            "mimeType": self.mime_type
        }

# Prompt definition
@dataclass
class Prompt:
    """MCP Prompt template"""
    name: str
    description: str
    arguments: List[Dict[str, str]]

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "arguments": self.arguments
        }

class CompleteMCPServer:
    """MCP Server with all three primitives"""

    def __init__(self, name: str):
        self.name = name

        # Registries for each primitive
        self.tools: Dict[str, Tool] = {}
        self.tool_handlers: Dict[str, Callable] = {}

        self.resources: Dict[str, Resource] = {}
        self.resource_content: Dict[str, Any] = {}

        self.prompts: Dict[str, Prompt] = {}
        self.prompt_templates: Dict[str, str] = {}

    # ─────────────────────────────────────────────────────────
    # TOOLS
    # ─────────────────────────────────────────────────────────

    def register_tool(self, tool: Tool, handler: Callable):
        """Register a tool with its handler"""
        self.tools[tool.name] = tool
        self.tool_handlers[tool.name] = handler
        print(f"  🛠️  [{self.name}] Registered tool: {tool.name}")

    def list_tools(self) -> List[Dict]:
        """List all available tools"""
        return [tool.to_dict() for tool in self.tools.values()]

    def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Execute a tool"""
        if tool_name not in self.tool_handlers:
            raise ValueError(f"Tool not found: {tool_name}")

        print(f"  ⚙️  [{self.name}] Executing tool: {tool_name}")
        handler = self.tool_handlers[tool_name]
        result = handler(arguments)

        return result

    # ─────────────────────────────────────────────────────────
    # RESOURCES
    # ─────────────────────────────────────────────────────────

    def register_resource(self, resource: Resource, content: Any):
        """Register a resource with its content"""
        self.resources[resource.uri] = resource
        self.resource_content[resource.uri] = content
        print(f"  📚 [{self.name}] Registered resource: {resource.uri}")

    def list_resources(self) -> List[Dict]:
        """List all available resources"""
        return [res.to_dict() for res in self.resources.values()]

    def read_resource(self, uri: str) -> Dict:
        """Read a resource's content"""
        if uri not in self.resources:
            raise ValueError(f"Resource not found: {uri}")

        resource = self.resources[uri]
        content = self.resource_content[uri]

        print(f"  📖 [{self.name}] Reading resource: {uri}")

        return {
            "uri": uri,
            "mimeType": resource.mime_type,
            "text": content if isinstance(content, str) else json.dumps(content)
        }

    # ─────────────────────────────────────────────────────────
    # PROMPTS
    # ─────────────────────────────────────────────────────────

    def register_prompt(self, prompt: Prompt, template: str):
        """Register a prompt template"""
        self.prompts[prompt.name] = prompt
        self.prompt_templates[prompt.name] = template
        print(f"  📝 [{self.name}] Registered prompt: {prompt.name}")

    def list_prompts(self) -> List[Dict]:
        """List all available prompts"""
        return [prompt.to_dict() for prompt in self.prompts.values()]

    def get_prompt(self, prompt_name: str, arguments: dict) -> Dict:
        """Get filled prompt template"""
        if prompt_name not in self.prompts:
            raise ValueError(f"Prompt not found: {prompt_name}")

        template = self.prompt_templates[prompt_name]

        # Fill template with arguments
        filled = template
        for arg_name, arg_value in arguments.items():
            placeholder = f"{{{arg_name}}}"
            filled = filled.replace(placeholder, str(arg_value))

        print(f"  📋 [{self.name}] Generated prompt: {prompt_name}")

        return {
            "description": self.prompts[prompt_name].description,
            "messages": [
                {
                    "role": "user",
                    "content": filled
                }
            ]
        }

print("\n▶ Building complete MCP server with all primitives:")

server = CompleteMCPServer("FileAndCodeServer")

# Register tools
print("\n  Registering TOOLS:")

read_file_tool = Tool(
    name="read_file",
    description="Read contents from a file",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "File path"}
        },
        "required": ["path"]
    }
)

def read_file_handler(args: dict) -> dict:
    path = args.get("path")
    # Simulate reading
    return {"content": f"Contents of {path}", "size": 1024}

server.register_tool(read_file_tool, read_file_handler)

write_file_tool = Tool(
    name="write_file",
    description="Write content to a file",
    input_schema={
        "type": "object",
        "properties": {
            "path": {"type": "string"},
            "content": {"type": "string"}
        },
        "required": ["path", "content"]
    }
)

def write_file_handler(args: dict) -> dict:
    path = args.get("path")
    content = args.get("content")
    return {"success": True, "bytes_written": len(content)}

server.register_tool(write_file_tool, write_file_handler)

# Register resources
print("\n  Registering RESOURCES:")

api_docs_resource = Resource(
    uri="file:///docs/api.md",
    name="API Documentation",
    description="Complete API documentation",
    mime_type="text/markdown"
)

server.register_resource(
    api_docs_resource,
    "# API Docs\n\n## GET /users\nFetch all users\n\n## POST /data\nCreate data"
)

config_resource = Resource(
    uri="file:///config.json",
    name="Configuration",
    description="Application configuration",
    mime_type="application/json"
)

server.register_resource(
    config_resource,
    {"host": "localhost", "port": 8080, "debug": True}
)

# Register prompts
print("\n  Registering PROMPTS:")

analyze_code_prompt = Prompt(
    name="analyze_code",
    description="Analyze code for issues",
    arguments=[
        {"name": "code", "description": "Code to analyze"},
        {"name": "language", "description": "Programming language"}
    ]
)

server.register_prompt(
    analyze_code_prompt,
    """Analyze this {language} code for potential issues:

```{language}
{code}
```

Check for:
1. Bugs and logic errors
2. Performance issues
3. Security vulnerabilities
4. Code quality and readability
5. Best practices"""
)

# Use all three primitives
print("\n▶ Using server primitives:")

print("\n  1. Listing tools:")
tools = server.list_tools()
for tool in tools:
    print(f"     • {tool['name']}: {tool['description']}")

print("\n  2. Calling a tool:")
result = server.call_tool("read_file", {"path": "/data/test.txt"})
print(f"     Result: {result}")

print("\n  3. Listing resources:")
resources = server.list_resources()
for resource in resources:
    print(f"     • {resource['name']} ({resource['uri']})")

print("\n  4. Reading a resource:")
resource_data = server.read_resource("file:///config.json")
print(f"     Content: {resource_data['text'][:50]}...")

print("\n  5. Listing prompts:")
prompts = server.list_prompts()
for prompt in prompts:
    print(f"     • {prompt['name']}: {prompt['description']}")

print("\n  6. Getting a prompt:")
filled_prompt = server.get_prompt(
    "analyze_code",
    {"code": "def add(a, b):\n    return a + b", "language": "python"}
)
print(f"     Generated prompt (first 100 chars):")
print(f"     {filled_prompt['messages'][0]['content'][:100]}...")

print("\n💡 KEY INSIGHT:")
print("   One server can provide all three primitive types!")
print("   Each has different discovery and access patterns")
print("   This is the foundation of MCP's flexibility")

# ==============================================================================
# EXAMPLE 2: JSON-RPC 2.0 Message System
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: JSON-RPC 2.0 - The Protocol Language")
print("=" * 80)
print("""
CONCEPT: MCP uses JSON-RPC 2.0 for ALL communication.
Understanding this format is critical for building MCP systems.

LOGIC:
- Every message is JSON
- Requests have: jsonrpc, method, params, id
- Responses have: jsonrpc, result/error, id
- Notifications have: jsonrpc, method, params (no id)
""")

class JSONRPCMessage:
    """Base class for JSON-RPC messages"""

    @staticmethod
    def create_request(method: str, params: Any, request_id: int) -> dict:
        """Create a JSON-RPC request"""
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id
        }

    @staticmethod
    def create_response(result: Any, request_id: int) -> dict:
        """Create a success response"""
        return {
            "jsonrpc": "2.0",
            "result": result,
            "id": request_id
        }

    @staticmethod
    def create_error(code: int, message: str, request_id: int, data: Any = None) -> dict:
        """Create an error response"""
        error = {
            "jsonrpc": "2.0",
            "error": {
                "code": code,
                "message": message
            },
            "id": request_id
        }

        if data:
            error["error"]["data"] = data

        return error

    @staticmethod
    def create_notification(method: str, params: Any) -> dict:
        """Create a notification (no response expected)"""
        return {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }

class MCPProtocolHandler:
    """Handles JSON-RPC message creation and parsing"""

    def __init__(self):
        self.request_id = 0

    def next_id(self) -> int:
        """Generate next request ID"""
        self.request_id += 1
        return self.request_id

    # Tool-related messages
    def create_tools_list_request(self) -> dict:
        """Request to list all tools"""
        return JSONRPCMessage.create_request(
            method="tools/list",
            params={},
            request_id=self.next_id()
        )

    def create_tools_call_request(self, tool_name: str, arguments: dict) -> dict:
        """Request to call a tool"""
        return JSONRPCMessage.create_request(
            method="tools/call",
            params={
                "name": tool_name,
                "arguments": arguments
            },
            request_id=self.next_id()
        )

    # Resource-related messages
    def create_resources_list_request(self) -> dict:
        """Request to list all resources"""
        return JSONRPCMessage.create_request(
            method="resources/list",
            params={},
            request_id=self.next_id()
        )

    def create_resources_read_request(self, uri: str) -> dict:
        """Request to read a resource"""
        return JSONRPCMessage.create_request(
            method="resources/read",
            params={"uri": uri},
            request_id=self.next_id()
        )

    # Prompt-related messages
    def create_prompts_get_request(self, name: str, arguments: dict) -> dict:
        """Request to get a prompt"""
        return JSONRPCMessage.create_request(
            method="prompts/get",
            params={
                "name": name,
                "arguments": arguments
            },
            request_id=self.next_id()
        )

print("\n▶ Creating JSON-RPC messages:")

protocol = MCPProtocolHandler()

# Tools messages
print("\n  TOOLS:")
tools_list_msg = protocol.create_tools_list_request()
print(f"     List tools: {json.dumps(tools_list_msg, indent=2)}")

tools_call_msg = protocol.create_tools_call_request(
    "read_file",
    {"path": "/data/file.txt"}
)
print(f"\n     Call tool: {json.dumps(tools_call_msg, indent=2)}")

# Resources messages
print("\n  RESOURCES:")
resources_list_msg = protocol.create_resources_list_request()
print(f"     List resources: {json.dumps(resources_list_msg, indent=2)}")

resources_read_msg = protocol.create_resources_read_request("file:///docs/api.md")
print(f"\n     Read resource: {json.dumps(resources_read_msg, indent=2)}")

# Create responses
print("\n  RESPONSES:")

success_response = JSONRPCMessage.create_response(
    result={"content": "File contents", "size": 100},
    request_id=1
)
print(f"     Success: {json.dumps(success_response, indent=2)}")

error_response = JSONRPCMessage.create_error(
    code=404,
    message="File not found",
    request_id=2,
    data={"path": "/missing.txt"}
)
print(f"\n     Error: {json.dumps(error_response, indent=2)}")

print("\n💡 KEY INSIGHT:")
print("   All MCP communication follows JSON-RPC 2.0 format")
print("   Method names follow pattern: category/action")
print("   ID field links requests to responses")

# ==============================================================================
# EXAMPLE 3: Client Primitives - Sampling Implementation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Client Primitive - Sampling (Server Asks AI)")
print("=" * 80)
print("""
CONCEPT: Servers can request AI completions from the client!
This enables servers to use AI for autonomous operations.

SCENARIO: A code review server asks AI to analyze code quality.

LOGIC:
- Server sends sampling/createMessage to client
- Client forwards to AI model (LLM)
- AI generates response
- Client sends result back to server
- Server uses AI-generated content
""")

class AIModel:
    """Simulates an AI model (LLM)"""

    def __init__(self, model_name: str):
        self.model_name = model_name

    def generate(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate AI completion"""
        print(f"  🤖 [{self.model_name}] Generating completion...")
        print(f"     Prompt: {prompt[:80]}...")

        time.sleep(0.3)  # Simulate generation time

        # Simulate AI response
        if "analyze" in prompt.lower():
            response = "This code looks good! Some suggestions: 1) Add error handling, 2) Add type hints, 3) Write docstrings"
        elif "generate" in prompt.lower():
            response = "Here's the generated code:\n\ndef example():\n    pass"
        else:
            response = "I've processed your request."

        print(f"     Generated: {len(response)} characters")

        return response

class ClientWithSampling:
    """MCP Client that supports sampling primitive"""

    def __init__(self, ai_model: AIModel):
        self.ai_model = ai_model

    def handle_sampling_request(self, prompt: str, max_tokens: int) -> dict:
        """Handle sampling request from server"""
        print(f"\n  📨 Client: Received sampling request from server")

        # Forward to AI model
        completion = self.ai_model.generate(prompt, max_tokens)

        # Return to server
        return {
            "content": completion,
            "stopReason": "endTurn",
            "model": self.ai_model.model_name
        }

class ServerUsingSampling:
    """Server that uses sampling to get AI help"""

    def __init__(self, name: str, client: ClientWithSampling):
        self.name = name
        self.client = client

    def review_code(self, code: str, language: str) -> dict:
        """Review code using AI sampling"""
        print(f"\n  🖥️  [{self.name}] Code review requested")

        # Create prompt for AI
        prompt = f"""Analyze this {language} code and provide feedback:

```{language}
{code}
```

Focus on: bugs, performance, security, best practices."""

        # Request AI completion via sampling
        print(f"  🖥️  [{self.name}] Requesting AI analysis via sampling...")

        sampling_result = self.client.handle_sampling_request(prompt, max_tokens=500)

        # Use AI's analysis
        return {
            "code_review": sampling_result["content"],
            "language": language,
            "model_used": sampling_result["model"]
        }

print("\n▶ Testing sampling primitive:")

# Create AI model and client
ai = AIModel("claude-3-opus")
client = ClientWithSampling(ai)

# Create server that uses sampling
review_server = ServerUsingSampling("CodeReviewServer", client)

# Server asks for code review (which uses AI)
code_to_review = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
"""

review = review_server.review_code(code_to_review, "python")

print(f"\n  ✅ Review result:")
print(f"     {review['code_review']}")

print("\n💡 KEY INSIGHT:")
print("   Sampling allows servers to be AI-powered!")
print("   Server can autonomously use AI for complex tasks")
print("   Enables powerful server-side intelligence")

# ==============================================================================
# EXAMPLE 4: stdio Transport - How Messages Travel Locally
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: stdio Transport - Process Communication")
print("=" * 80)
print("""
CONCEPT: stdio transport uses standard input/output for communication.
Client and server run as separate processes, communicating via pipes.

LOGIC:
- Server reads from stdin (receives requests)
- Server writes to stdout (sends responses)
- Client writes to server's stdin (sends requests)
- Client reads from server's stdout (receives responses)
- Each message is one line of JSON
""")

import io
from queue import Queue

class StdioTransport:
    """Simulates stdio transport (simplified)"""

    def __init__(self, name: str):
        self.name = name
        self.input_buffer = Queue()
        self.output_buffer = Queue()

    def send_message(self, message: dict):
        """Send a message (write to output)"""
        json_str = json.dumps(message)
        print(f"  📤 [{self.name}] Sending: {json_str[:80]}...")
        self.output_buffer.put(json_str)

    def receive_message(self) -> Optional[dict]:
        """Receive a message (read from input)"""
        if self.input_buffer.empty():
            return None

        json_str = self.input_buffer.get()
        print(f"  📥 [{self.name}] Received: {json_str[:80]}...")

        return json.loads(json_str)

    def connect_to(self, other_transport: 'StdioTransport'):
        """Connect this transport to another (pipe simulation)"""
        # This transport's output → other's input
        # Other's output → this transport's input
        self.pipe_to = other_transport

print("\n▶ Simulating stdio communication:")

# Create transports for client and server
client_transport = StdioTransport("Client")
server_transport = StdioTransport("Server")

# Connect them (simulate pipes)
# Note: In real stdio, this is done via subprocess pipes

# Client sends request
print("\n  Client sending request:")
request = JSONRPCMessage.create_request(
    method="tools/list",
    params={},
    request_id=1
)

client_transport.send_message(request)

# Simulate: transfer from client output to server input
message_json = client_transport.output_buffer.get()
server_transport.input_buffer.put(message_json)

# Server receives and processes
print("\n  Server receiving and processing:")
received_request = server_transport.receive_message()
print(f"     Method: {received_request['method']}")
print(f"     ID: {received_request['id']}")

# Server creates response
response = JSONRPCMessage.create_response(
    result={"tools": [{"name": "read_file"}, {"name": "write_file"}]},
    request_id=received_request['id']
)

server_transport.send_message(response)

# Simulate: transfer from server output to client input
response_json = server_transport.output_buffer.get()
client_transport.input_buffer.put(response_json)

# Client receives response
print("\n  Client receiving response:")
received_response = client_transport.receive_message()
print(f"     Result: {received_response['result']}")
print(f"     ID: {received_response['id']} (matches request)")

print("\n💡 KEY INSIGHT:")
print("   stdio uses process pipes for local communication")
print("   Each message is one line of JSON")
print("   Secure (process isolation) and simple (no network)")

# ==============================================================================
# EXAMPLE 5: Complete Session Lifecycle
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: Session Lifecycle - From Connect to Disconnect")
print("=" * 80)
print("""
CONCEPT: Every MCP session goes through:
1. Initialization (capability negotiation)
2. Active usage (requests/responses)
3. Termination (cleanup)

LOGIC:
- Initialize handshake exchanges capabilities
- Both sides know what's supported
- Can then use tools/resources/prompts
- Graceful shutdown on close
""")

class MCPSession:
    """Represents a complete MCP session"""

    def __init__(self, client_name: str, server_name: str):
        self.client_name = client_name
        self.server_name = server_name
        self.initialized = False
        self.protocol_version = "2025-11-25"
        self.server_capabilities = {}
        self.client_capabilities = {}

    def initialize(self, client_caps: dict, server_caps: dict):
        """Initialize session with capability negotiation"""
        print(f"\n  🔄 Initializing MCP session")
        print(f"     Client: {self.client_name}")
        print(f"     Server: {self.server_name}")

        # Client sends initialize request
        init_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {
                "protocolVersion": self.protocol_version,
                "capabilities": client_caps,
                "clientInfo": {
                    "name": self.client_name,
                    "version": "1.0.0"
                }
            },
            "id": 1
        }

        print(f"\n     📤 Client → Server: initialize request")
        print(f"        Client capabilities: {list(client_caps.keys())}")

        # Server responds
        init_response = {
            "jsonrpc": "2.0",
            "result": {
                "protocolVersion": self.protocol_version,
                "capabilities": server_caps,
                "serverInfo": {
                    "name": self.server_name,
                    "version": "1.0.0"
                }
            },
            "id": 1
        }

        print(f"     📥 Server → Client: initialize response")
        print(f"        Server capabilities: {list(server_caps.keys())}")

        # Store capabilities
        self.client_capabilities = client_caps
        self.server_capabilities = server_caps
        self.initialized = True

        print(f"\n  ✅ Session initialized!")
        print(f"     Protocol version: {self.protocol_version}")
        print(f"     Server supports: {', '.join(server_caps.keys())}")

    def execute_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute a tool during active session"""
        if not self.initialized:
            raise RuntimeError("Session not initialized!")

        if "tools" not in self.server_capabilities:
            raise RuntimeError("Server doesn't support tools!")

        print(f"\n  ⚙️  Executing tool: {tool_name}")

        # Create request
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {"name": tool_name, "arguments": arguments},
            "id": 2
        }

        print(f"     📤 Request: {request['params']}")

        # Simulate server execution
        time.sleep(0.1)

        # Response
        response = {
            "jsonrpc": "2.0",
            "result": {"output": f"Executed {tool_name} successfully"},
            "id": 2
        }

        print(f"     📥 Response: {response['result']}")

        return response

    def close(self):
        """Close the session"""
        print(f"\n  🔌 Closing MCP session")
        print(f"     Cleaning up resources...")
        self.initialized = False
        print(f"  ✅ Session closed")

print("\n▶ Complete session lifecycle:")

# Create session
session = MCPSession("claude-desktop", "file-server")

# Phase 1: Initialize
session.initialize(
    client_caps={
        "tools": {},
        "resources": {}
    },
    server_caps={
        "tools": {},
        "resources": {},
        "prompts": {}
    }
)

# Phase 2: Use
session.execute_tool("read_file", {"path": "/data/test.txt"})
session.execute_tool("write_file", {"path": "/output.txt", "content": "Hello"})

# Phase 3: Close
session.close()

print("\n💡 KEY INSIGHT:")
print("   Every session starts with 'initialize' handshake")
print("   Capabilities are negotiated (what does each side support?)")
print("   Only after init can tools/resources be used")

# ==============================================================================
# EXAMPLE 6: Multi-Server Architecture
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Multi-Server System - Ecosystem in Action")
print("=" * 80)
print("""
CONCEPT: One host/client can connect to MULTIPLE servers simultaneously.
Each server specializes in different capabilities.

SCENARIO: AI assistant with access to:
- File operations (file server)
- Database queries (database server)
- Web search (web server)

LOGIC:
- Host creates separate client for each server
- Each client maintains its own connection
- Host routes requests to appropriate server
- Responses aggregated and sent to AI
""")

class MultiServerHost:
    """Host managing multiple MCP clients/servers"""

    def __init__(self, name: str):
        self.name = name
        self.clients = {}  # {server_name: client}
        self.servers = {}  # {server_name: server}

    def add_server(self, server_name: str, server):
        """Add and connect to a server"""
        # Create client for this server
        client = SimpleMCPClient(f"client-for-{server_name}")
        client.connect_to_server(server)

        self.clients[server_name] = client
        self.servers[server_name] = server

        print(f"  🔌 [{self.name}] Connected to server: {server_name}")

    def list_all_capabilities(self):
        """List capabilities from all servers"""
        print(f"\n  📋 [{self.name}] All capabilities:")

        for server_name, client in self.clients.items():
            print(f"\n     Server: {server_name}")

            tools = client.list_tools()
            print(f"       Tools: {[t['name'] for t in tools]}")

            resources = client.list_resources()
            print(f"       Resources: {[r['name'] for r in resources]}")

    def call_any_tool(self, tool_name: str, arguments: dict) -> Any:
        """Find and call a tool across all servers"""
        print(f"\n  🔍 [{self.name}] Looking for tool: {tool_name}")

        # Find which server has this tool
        for server_name, client in self.clients.items():
            tools = client.list_tools()

            if any(t['name'] == tool_name for t in tools):
                print(f"     Found in server: {server_name}")
                return client.call_tool(tool_name, arguments)

        raise ValueError(f"Tool '{tool_name}' not found in any server")

class SimpleMCPClient:
    """Simplified MCP client"""

    def __init__(self, name: str):
        self.name = name
        self.server = None

    def connect_to_server(self, server: CompleteMCPServer):
        """Connect to a server"""
        self.server = server

    def list_tools(self) -> List[dict]:
        """List server's tools"""
        return self.server.list_tools()

    def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Call a tool on the server"""
        return self.server.call_tool(tool_name, arguments)

    def list_resources(self) -> List[dict]:
        """List server's resources"""
        return self.server.list_resources()

    def read_resource(self, uri: str) -> dict:
        """Read a resource"""
        return self.server.read_resource(uri)

print("\n▶ Building multi-server ecosystem:")

# Create host
host = MultiServerHost("ClaudeDesktop")

# Create multiple servers
file_server = CompleteMCPServer("FileServer")
file_server.register_tool(
    Tool("read_file", "Read files", {"type": "object"}),
    lambda args: {"content": f"File: {args.get('path')}"}
)

db_server = CompleteMCPServer("DatabaseServer")
db_server.register_tool(
    Tool("db_query", "Query database", {"type": "object"}),
    lambda args: {"rows": [{"id": 1}, {"id": 2}]}
)

web_server = CompleteMCPServer("WebServer")
web_server.register_tool(
    Tool("web_search", "Search web", {"type": "object"}),
    lambda args: {"results": ["Result 1", "Result 2"]}
)

# Connect all servers to host
print("\n  Connecting servers to host:")
host.add_server("files", file_server)
host.add_server("database", db_server)
host.add_server("web", web_server)

# List all capabilities
host.list_all_capabilities()

# AI uses tools from different servers
print("\n▶ AI using tools from different servers:")

result1 = host.call_any_tool("read_file", {"path": "/data/sales.csv"})
print(f"     File result: {result1}")

result2 = host.call_any_tool("db_query", {"sql": "SELECT * FROM users"})
print(f"     DB result: {result2['rows']}")

result3 = host.call_any_tool("web_search", {"query": "MCP protocol"})
print(f"     Web result: {result3['results']}")

print("\n💡 KEY INSIGHT:")
print("   One host can orchestrate multiple specialized servers")
print("   Each server focuses on one domain (files, DB, web, etc.)")
print("   Together they create powerful AI capabilities!")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 MODULE 01 COMPLETE - CORE CONCEPTS MASTERED!")
print("=" * 80)

summary = """
What You've Learned:

✅ MCP Architecture:
   • Host (user interface layer)
   • Client (protocol communication layer)
   • Server (capability provider layer)
   • How they work together

✅ Six Primitives:
   SERVER PRIMITIVES (Server → AI):
   • Tools - Executable functions
   • Resources - Read-only data
   • Prompts - Conversation templates

   CLIENT PRIMITIVES (Server → Client):
   • Sampling - Request AI completion
   • Elicitation - Request user input
   • Logging - Send debug messages

✅ Protocol Details:
   • JSON-RPC 2.0 message format
   • Request/response pattern
   • Message ID matching
   • Notification pattern

✅ Transport Layers:
   • stdio - Local process communication
   • HTTP + SSE - Remote network communication

✅ Session Lifecycle:
   • Initialization (capability negotiation)
   • Active usage (tool/resource calls)
   • Termination (cleanup)

✅ Multi-Server Architecture:
   • One host, multiple servers
   • Specialized servers per domain
   • Orchestrated by host

Key Technical Points:
────────────────────────────────────────────────
1. JSON-RPC 2.0 is the message format
2. stdio recommended for local, HTTP for remote
3. Every session starts with 'initialize'
4. Capabilities negotiated at connection time
5. User consent required for operations
6. Servers can request AI help (sampling)
7. One client per server (1:1 relationship)
8. One host can manage many clients (1:many)

You're Ready For:
────────────────────────────────────────────────
→ Module 02: Security (deep dive into security)
→ Module 03: Building your first real server!
→ Implementing actual MCP protocol in Python

Next: Module_02_Security.md
"""

print(summary)

print("\n" + "=" * 80)
print("📝 PRACTICE EXERCISE:")
print("=" * 80)
print("""
Design your own MCP server:

1. Choose a domain (e.g., email, calendar, git)
2. List 3 tools it would provide
3. List 2 resources it would provide
4. Design 1 prompt template
5. Consider security: what permissions needed?

This mental exercise prepares you for building real servers!
""")
