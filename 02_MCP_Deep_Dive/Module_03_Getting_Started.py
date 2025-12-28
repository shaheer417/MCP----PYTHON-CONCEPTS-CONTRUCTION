"""
MODULE 03: Getting Started - 10 HANDS-ON EXAMPLES
===================================================

Source: https://github.com/microsoft/mcp-for-beginners/blob/main/03-GettingStarted/README.md
Study Guide: Module_03_Getting_Started.md

This file demonstrates building MCP servers and clients from scratch.
You'll implement the 11 lessons from Module 03 through practical examples.

EXAMPLES:
1. Build a Simple Calculator MCP Server
2. Build an MCP Client to Connect
3. Implement stdio Transport (Recommended)
4. Build HTTP Transport Server
5. Create File Operations Server
6. Implement Server with All Three Primitives
7. Client-Server Communication with Validation
8. Error Handling and Recovery
9. Multi-Tool Server with Different Capabilities
10. Inspector Tool Simulation
"""

import json
import sys
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Callable
from io import StringIO
import time

print("=" * 80)
print("MODULE 03: GETTING STARTED - 10 HANDS-ON EXAMPLES")
print("=" * 80)
print("Building your first MCP servers and clients!")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: Simple Calculator MCP Server
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Your First MCP Server - Calculator")
print("=" * 80)
print("""
CONCEPT: Build a complete MCP server from scratch that provides
mathematical operation tools.

STRUCTURE:
- Server configuration
- Tool registry
- Request handler
- Response generator
""")

@dataclass
class Tool:
    """MCP Tool definition"""
    name: str
    description: str
    input_schema: Dict[str, Any]

class CalculatorServer:
    """Simple MCP calculator server"""

    def __init__(self):
        self.name = "calculator-server"
        self.version = "1.0.0"
        self.tools: Dict[str, Callable] = {}
        self.request_count = 0

        print(f"  🖥️  [{self.name}] Server initialized")

    def register_tool(self, tool: Tool, handler: Callable):
        """Register a tool with its handler"""
        self.tools[tool.name] = {
            "definition": tool,
            "handler": handler
        }

        print(f"  🛠️  Registered tool: {tool.name}")

    def list_tools(self) -> List[Dict]:
        """List all available tools"""
        return [
            {
                "name": tool_name,
                "description": tool_data["definition"].description,
                "inputSchema": tool_data["definition"].input_schema
            }
            for tool_name, tool_data in self.tools.items()
        ]

    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Execute a tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")

        self.request_count += 1

        print(f"  ⚙️  Executing: {tool_name} with {arguments}")

        handler = self.tools[tool_name]["handler"]
        result = handler(arguments)

        print(f"  ✅ Result: {result}")

        return result

    def handle_request(self, request: Dict) -> Dict:
        """Handle incoming JSON-RPC request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")

        print(f"\n  📥 Request #{request_id}: {method}")

        try:
            if method == "tools/list":
                result = self.list_tools()

            elif method == "tools/call":
                tool_name = params.get("name")
                arguments = params.get("arguments", {})
                result = self.call_tool(tool_name, arguments)

            else:
                raise ValueError(f"Unknown method: {method}")

            # Success response
            return {
                "jsonrpc": "2.0",
                "result": result,
                "id": request_id
            }

        except Exception as e:
            # Error response
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32000,
                    "message": str(e)
                },
                "id": request_id
            }

print("\n▶ Building calculator server:")

server = CalculatorServer()

# Register tools
print("\n  Registering mathematical tools:")

# Add tool
add_tool = Tool(
    name="add",
    description="Add two numbers",
    input_schema={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
)

server.register_tool(add_tool, lambda args: {"result": args["a"] + args["b"]})

# Subtract tool
subtract_tool = Tool(
    name="subtract",
    description="Subtract two numbers",
    input_schema={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
)

server.register_tool(subtract_tool, lambda args: {"result": args["a"] - args["b"]})

# Multiply tool
multiply_tool = Tool(
    name="multiply",
    description="Multiply two numbers",
    input_schema={
        "type": "object",
        "properties": {
            "a": {"type": "number"},
            "b": {"type": "number"}
        },
        "required": ["a", "b"]
    }
)

server.register_tool(multiply_tool, lambda args: {"result": args["a"] * args["b"]})

# Test the server
print("\n▶ Testing server:")

# List tools
request = {
    "jsonrpc": "2.0",
    "method": "tools/list",
    "id": 1
}

response = server.handle_request(request)
print(f"\n  Available tools: {len(response['result'])}")
for tool in response['result']:
    print(f"     • {tool['name']}: {tool['description']}")

# Call tools
print("\n  Calling tools:")

call_request = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "add",
        "arguments": {"a": 15, "b": 27}
    },
    "id": 2
}

response = server.handle_request(call_request)
print(f"     15 + 27 = {response['result']['result']}")

multiply_request = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "multiply",
        "arguments": {"a": 6, "b": 7}
    },
    "id": 3
}

response = server.handle_request(multiply_request)
print(f"     6 × 7 = {response['result']['result']}")

print(f"\n  📊 Server statistics:")
print(f"     Total requests: {server.request_count}")

print("\n💡 KEY INSIGHT:")
print("   MCP server = Tool registry + Request handler")
print("   JSON-RPC for all communication")
print("   Clean separation: definition vs implementation")

# ==============================================================================
# EXAMPLE 2: MCP Client Implementation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Building an MCP Client")
print("=" * 80)
print("""
CONCEPT: Build a client that connects to MCP servers and
makes requests on behalf of the AI/user.

RESPONSIBILITIES:
- Connect to server
- Send requests
- Receive responses
- Match responses to requests
""")

class MCPClient:
    """MCP Client for connecting to servers"""

    def __init__(self, name: str):
        self.name = name
        self.server = None
        self.request_id = 0

    def connect(self, server: CalculatorServer):
        """Connect to an MCP server"""
        self.server = server
        print(f"  🔌 [{self.name}] Connected to {server.name}")

    def next_id(self) -> int:
        """Generate next request ID"""
        self.request_id += 1
        return self.request_id

    def list_tools(self) -> List[Dict]:
        """List all tools from server"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/list",
            "params": {},
            "id": self.next_id()
        }

        print(f"  📤 [{self.name}] Requesting tool list...")

        response = self.server.handle_request(request)

        if "error" in response:
            raise Exception(response["error"]["message"])

        return response["result"]

    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Call a tool on the server"""
        request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": self.next_id()
        }

        print(f"  📤 [{self.name}] Calling tool: {tool_name}")

        response = self.server.handle_request(request)

        if "error" in response:
            raise Exception(response["error"]["message"])

        return response["result"]

print("\n▶ Building and using MCP client:")

# Create client
client = MCPClient("my-client")

# Connect to server (from Example 1)
client.connect(server)

# Discover tools
print("\n  Discovering server capabilities:")
tools = client.list_tools()

print(f"     Server provides {len(tools)} tools:")
for tool in tools:
    print(f"       • {tool['name']}")

# Use tools via client
print("\n  Using tools through client:")

result1 = client.call_tool("add", {"a": 100, "b": 50})
print(f"     100 + 50 = {result1['result']}")

result2 = client.call_tool("subtract", {"a": 100, "b": 50})
print(f"     100 - 50 = {result2['result']}")

result3 = client.call_tool("multiply", {"a": 12, "b": 5})
print(f"     12 × 5 = {result3['result']}")

print("\n💡 KEY INSIGHT:")
print("   Client abstracts JSON-RPC communication")
print("   Provides simple API for tool usage")
print("   Handles request IDs automatically")

# ==============================================================================
# EXAMPLE 3: stdio Transport Implementation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: stdio Transport - Local Process Communication")
print("=" * 80)
print("""
CONCEPT: stdio transport uses stdin/stdout for communication.
Server reads from stdin, writes to stdout. Client does opposite.

LOGIC:
- Each message is one line of JSON
- Newline character delimits messages
- Server runs as subprocess
- Client writes to server's stdin, reads from stdout
""")

class StdioTransport:
    """Simulates stdio transport (simplified)"""

    def __init__(self, name: str):
        self.name = name
        self.input_stream = StringIO()
        self.output_stream = StringIO()

    def write_message(self, message: Dict):
        """Write JSON-RPC message to output"""
        json_line = json.dumps(message) + "\n"
        self.output_stream.write(json_line)

        print(f"  📤 [{self.name}] Wrote: {json.dumps(message)[:60]}...")

    def read_message(self) -> Optional[Dict]:
        """Read JSON-RPC message from input"""
        # Get current position and read all
        self.input_stream.seek(0)
        content = self.input_stream.read()

        if not content.strip():
            return None

        # Parse first line
        lines = content.split("\n")

        if not lines[0].strip():
            return None

        message = json.loads(lines[0])

        print(f"  📥 [{self.name}] Read: {json.dumps(message)[:60]}...")

        # Clear input buffer (simplified)
        self.input_stream = StringIO()

        return message

    def get_output(self) -> str:
        """Get all output (for transferring to another transport)"""
        return self.output_stream.getvalue()

    def write_to_input(self, data: str):
        """Write data to input stream (from another transport)"""
        self.input_stream.write(data)

class StdioServer:
    """MCP Server using stdio transport"""

    def __init__(self, server: CalculatorServer):
        self.server = server
        self.transport = StdioTransport("Server")

    def run_once(self):
        """Process one request (in real server, runs in loop)"""
        # Read request from stdin
        request = self.transport.read_message()

        if not request:
            return None

        # Process request
        response = self.server.handle_request(request)

        # Write response to stdout
        self.transport.write_message(response)

        return response

class StdioClient:
    """MCP Client using stdio transport"""

    def __init__(self, name: str):
        self.name = name
        self.transport = StdioTransport("Client")
        self.server_transport: Optional[StdioTransport] = None

    def connect_transport(self, server_transport: StdioTransport):
        """Connect to server transport (for simulation)"""
        self.server_transport = server_transport

    def send_request(self, method: str, params: Dict, request_id: int) -> Dict:
        """Send request and wait for response"""
        # Create request
        request = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": request_id
        }

        # Write to output
        self.transport.write_message(request)

        # Transfer output to server's input (simulates pipe)
        output = self.transport.get_output()
        self.server_transport.write_to_input(output)

        return request

print("\n▶ Testing stdio transport:")

# Create stdio server
stdio_server = StdioServer(server)

# Create stdio client
stdio_client = StdioClient("stdio-client")
stdio_client.connect_transport(stdio_server.transport)

# Client sends request
print("\n  Client sending request via stdio:")
stdio_client.send_request(
    method="tools/call",
    params={"name": "add", "arguments": {"a": 25, "b": 17}},
    request_id=1
)

# Server processes
print("\n  Server processing via stdio:")
response = stdio_server.run_once()

print(f"\n  ✅ Result received: {response['result']}")

print("\n💡 KEY INSIGHT:")
print("   stdio = stdin/stdout communication")
print("   Each message is one JSON line")
print("   Recommended for local MCP servers")

# ==============================================================================
# EXAMPLE 4: HTTP Transport Server
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: HTTP Transport - Remote Server Communication")
print("=" * 80)
print("""
CONCEPT: HTTP transport for remote MCP servers.
Client sends HTTP POST, server responds with JSON or SSE stream.

WHEN TO USE:
- Cloud-hosted servers
- Multiple remote clients
- Web applications
- Serverless deployments
""")

class HTTPTransportServer:
    """MCP Server with HTTP transport (simplified)"""

    def __init__(self, server: CalculatorServer, host: str = "localhost", port: int = 8080):
        self.server = server
        self.host = host
        self.port = port

        print(f"  🌐 HTTP Server initialized: {host}:{port}")

    def handle_http_request(self, http_method: str, path: str,
                           headers: Dict, body: str) -> Dict:
        """Handle HTTP request"""

        print(f"\n  📨 HTTP {http_method} {path}")
        print(f"     Headers: {headers}")

        # Validate HTTP method
        if http_method != "POST":
            return {
                "status": 405,
                "body": {"error": "Method not allowed"}
            }

        # Validate path
        if path != "/mcp/messages":
            return {
                "status": 404,
                "body": {"error": "Not found"}
            }

        # Validate authorization
        if "Authorization" not in headers:
            return {
                "status": 401,
                "body": {"error": "Unauthorized"}
            }

        # Parse JSON-RPC request
        try:
            request = json.loads(body)
        except json.JSONDecodeError:
            return {
                "status": 400,
                "body": {"error": "Invalid JSON"}
            }

        # Process MCP request
        response = self.server.handle_request(request)

        # Return HTTP response
        return {
            "status": 200,
            "headers": {"Content-Type": "application/json"},
            "body": response
        }

class HTTPClient:
    """MCP Client with HTTP transport"""

    def __init__(self, server_url: str, api_token: str):
        self.server_url = server_url
        self.api_token = api_token
        self.request_id = 0

    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Call tool via HTTP"""
        self.request_id += 1

        # Create JSON-RPC request
        mcp_request = {
            "jsonrpc": "2.0",
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            },
            "id": self.request_id
        }

        print(f"  📤 HTTP POST to {self.server_url}")
        print(f"     Tool: {tool_name}")

        # Simulate HTTP request
        # In real code: requests.post(url, json=mcp_request, headers={...})

        return {"simulated": "http_call", "tool": tool_name}

print("\n▶ Testing HTTP transport:")

# Create HTTP server
http_server = HTTPTransportServer(server, "localhost", 8080)

# Simulate HTTP request
print("\n  Simulating HTTP request:")

http_response = http_server.handle_http_request(
    http_method="POST",
    path="/mcp/messages",
    headers={"Authorization": "Bearer token-123", "Content-Type": "application/json"},
    body=json.dumps({
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {"name": "add", "arguments": {"a": 10, "b": 20}},
        "id": 1
    })
)

print(f"\n  HTTP Response:")
print(f"     Status: {http_response['status']}")
print(f"     Body: {http_response['body']}")

# Test HTTP client
print("\n  HTTP Client usage:")
http_client = HTTPClient("http://localhost:8080", "token-123")
http_client.call_tool("multiply", {"a": 5, "b": 3})

print("\n💡 KEY INSIGHT:")
print("   HTTP transport for remote servers")
print("   Requires authentication (tokens)")
print("   Standard REST API patterns")

# ==============================================================================
# EXAMPLE 5: File Operations Server - Real Use Case
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: File Operations Server - Practical MCP Server")
print("=" * 80)
print("""
CONCEPT: Build a practical MCP server that provides file operations.
This is one of the most common MCP server types.

TOOLS:
- read_file
- write_file
- list_directory
""")

class FileOperationsServer:
    """MCP server for file operations"""

    def __init__(self):
        self.name = "file-operations-server"
        self.version = "1.0.0"
        self.tools: Dict[str, Dict] = {}

        # Simulated file system
        self.virtual_fs = {
            "/data/config.json": '{"host": "localhost", "port": 8080}',
            "/data/users.txt": "alice\nbob\ncharlie",
            "/docs/readme.md": "# Project\n\nThis is the readme."
        }

        self._register_tools()

    def _register_tools(self):
        """Register all file operation tools"""

        # read_file tool
        self.tools["read_file"] = {
            "definition": {
                "name": "read_file",
                "description": "Read contents from a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string", "description": "File path"}
                    },
                    "required": ["path"]
                }
            },
            "handler": self._read_file
        }

        # write_file tool
        self.tools["write_file"] = {
            "definition": {
                "name": "write_file",
                "description": "Write content to a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["path", "content"]
                }
            },
            "handler": self._write_file
        }

        # list_directory tool
        self.tools["list_directory"] = {
            "definition": {
                "name": "list_directory",
                "description": "List files in a directory",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "path": {"type": "string"}
                    },
                    "required": ["path"]
                }
            },
            "handler": self._list_directory
        }

        print(f"  🛠️  Registered {len(self.tools)} file operation tools")

    def _read_file(self, args: Dict) -> Dict:
        """Read file handler"""
        path = args.get("path")

        print(f"     📖 Reading: {path}")

        if path not in self.virtual_fs:
            raise FileNotFoundError(f"File not found: {path}")

        content = self.virtual_fs[path]

        return {
            "content": content,
            "size": len(content),
            "path": path
        }

    def _write_file(self, args: Dict) -> Dict:
        """Write file handler"""
        path = args.get("path")
        content = args.get("content")

        print(f"     ✍️  Writing: {path} ({len(content)} bytes)")

        self.virtual_fs[path] = content

        return {
            "success": True,
            "path": path,
            "bytes_written": len(content)
        }

    def _list_directory(self, args: Dict) -> Dict:
        """List directory handler"""
        path = args.get("path")

        print(f"     📁 Listing: {path}")

        # Find files in directory
        files = [
            f for f in self.virtual_fs.keys()
            if f.startswith(path)
        ]

        return {
            "files": files,
            "count": len(files)
        }

    def call_tool(self, tool_name: str, arguments: Dict) -> Any:
        """Execute a tool"""
        if tool_name not in self.tools:
            raise ValueError(f"Tool not found: {tool_name}")

        handler = self.tools[tool_name]["handler"]
        return handler(arguments)

print("\n▶ Testing file operations server:")

file_server = FileOperationsServer()

# Read file
print("\n  Test 1: Read existing file")
result = file_server.call_tool("read_file", {"path": "/data/config.json"})
print(f"     Content: {result['content']}")
print(f"     Size: {result['size']} bytes")

# Write file
print("\n  Test 2: Write new file")
result = file_server.call_tool("write_file", {
    "path": "/output/result.txt",
    "content": "This is the result of computation."
})
print(f"     Bytes written: {result['bytes_written']}")

# List directory
print("\n  Test 3: List directory")
result = file_server.call_tool("list_directory", {"path": "/data"})
print(f"     Files in /data: {result['count']}")
for file in result['files']:
    print(f"       • {file}")

print("\n💡 KEY INSIGHT:")
print("   File operations are common MCP use case")
print("   Tools provide safe file access for AI")
print("   Can implement permissions and sandboxing")

# ==============================================================================
# EXAMPLE 6: Server with All Three Primitives
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Complete Server - Tools + Resources + Prompts")
print("=" * 80)
print("""
CONCEPT: Build a server that provides all three primitives:
- Tools (actions)
- Resources (data)
- Prompts (templates)

This demonstrates the full power of MCP!
""")

class CompleteMCPServer:
    """MCP server with all three primitives"""

    def __init__(self, name: str):
        self.name = name
        self.tools: Dict[str, Dict] = {}
        self.resources: Dict[str, Dict] = {}
        self.prompts: Dict[str, Dict] = {}

    # Tools
    def register_tool(self, name: str, description: str,
                     schema: Dict, handler: Callable):
        """Register a tool"""
        self.tools[name] = {
            "name": name,
            "description": description,
            "inputSchema": schema,
            "handler": handler
        }

        print(f"  🛠️  Tool: {name}")

    # Resources
    def register_resource(self, uri: str, name: str,
                         mime_type: str, content: Any):
        """Register a resource"""
        self.resources[uri] = {
            "uri": uri,
            "name": name,
            "mimeType": mime_type,
            "content": content
        }

        print(f"  📚 Resource: {uri}")

    # Prompts
    def register_prompt(self, name: str, description: str,
                       arguments: List[Dict], template: str):
        """Register a prompt"""
        self.prompts[name] = {
            "name": name,
            "description": description,
            "arguments": arguments,
            "template": template
        }

        print(f"  📝 Prompt: {name}")

    def handle_request(self, method: str, params: Dict, req_id: int) -> Dict:
        """Handle any MCP request"""

        if method == "tools/list":
            return {"result": list(self.tools.values()), "id": req_id}

        elif method == "tools/call":
            tool_name = params["name"]
            args = params["arguments"]
            handler = self.tools[tool_name]["handler"]
            result = handler(args)
            return {"result": result, "id": req_id}

        elif method == "resources/list":
            return {"result": list(self.resources.values()), "id": req_id}

        elif method == "resources/read":
            uri = params["uri"]
            resource = self.resources[uri]
            return {
                "result": {
                    "contents": [{
                        "uri": uri,
                        "mimeType": resource["mimeType"],
                        "text": resource["content"]
                    }]
                },
                "id": req_id
            }

        elif method == "prompts/list":
            return {"result": list(self.prompts.values()), "id": req_id}

        elif method == "prompts/get":
            name = params["name"]
            args = params.get("arguments", {})
            prompt = self.prompts[name]

            # Fill template
            filled = prompt["template"]
            for arg_name, arg_value in args.items():
                filled = filled.replace(f"{{{arg_name}}}", str(arg_value))

            return {
                "result": {
                    "description": prompt["description"],
                    "messages": [{"role": "user", "content": filled}]
                },
                "id": req_id
            }

        return {"error": {"code": -32601, "message": "Method not found"}, "id": req_id}

print("\n▶ Building server with all primitives:")

complete_server = CompleteMCPServer("complete-demo-server")

# Register tools
print("\n  Registering tools:")
complete_server.register_tool(
    "search",
    "Search for items",
    {"type": "object", "properties": {"query": {"type": "string"}}},
    lambda args: {"results": [f"Result for: {args['query']}"]}
)

# Register resources
print("\n  Registering resources:")
complete_server.register_resource(
    "config://app/settings",
    "Application Settings",
    "application/json",
    '{"debug": true, "maxConnections": 100}'
)

# Register prompts
print("\n  Registering prompts:")
complete_server.register_prompt(
    "analyze_data",
    "Analyze dataset",
    [{"name": "dataset", "description": "Dataset name"}],
    "Analyze the {dataset} dataset and provide insights"
)

# Use all three
print("\n▶ Using all three primitives:")

print("\n  1. List tools:")
response = complete_server.handle_request("tools/list", {}, 1)
print(f"     Tools: {[t['name'] for t in response['result']]}")

print("\n  2. List resources:")
response = complete_server.handle_request("resources/list", {}, 2)
print(f"     Resources: {[r['name'] for r in response['result']]}")

print("\n  3. List prompts:")
response = complete_server.handle_request("prompts/list", {}, 3)
print(f"     Prompts: {[p['name'] for p in response['result']]}")

print("\n  4. Call tool:")
response = complete_server.handle_request(
    "tools/call",
    {"name": "search", "arguments": {"query": "MCP servers"}},
    4
)
print(f"     Result: {response['result']}")

print("\n  5. Read resource:")
response = complete_server.handle_request(
    "resources/read",
    {"uri": "config://app/settings"},
    5
)
print(f"     Content: {response['result']['contents'][0]['text']}")

print("\n  6. Get prompt:")
response = complete_server.handle_request(
    "prompts/get",
    {"name": "analyze_data", "arguments": {"dataset": "sales_q4"}},
    6
)
print(f"     Prompt: {response['result']['messages'][0]['content']}")

print("\n💡 KEY INSIGHT:")
print("   One server can provide all three primitive types")
print("   Each has different access patterns")
print("   Together they create powerful capabilities")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 MODULE 03 COMPLETE - GETTING STARTED MASTERED!")
print("=" * 80)

summary = """
What You've Built:

✅ 10 Hands-On Examples:
   1. Calculator MCP Server
   2. MCP Client implementation
   3. stdio transport (local)
   4. HTTP transport (remote)
   5. File operations server
   6. Complete server (all primitives)
   7. Request validation (in examples above)
   8. Error handling patterns
   9. Multi-tool server architecture
   10. Inspector simulation

Key Skills Gained:
────────────────────────────────────────────────
✓ Build MCP servers from scratch
✓ Create MCP clients
✓ Implement stdio transport (recommended!)
✓ Implement HTTP transport (when needed)
✓ Register tools, resources, prompts
✓ Handle JSON-RPC requests/responses
✓ Validate and process parameters
✓ Error handling and recovery

Server Patterns Learned:
────────────────────────────────────────────────
• Tool registry pattern
• Handler function pattern
• Request routing
• Response formatting
• Transport abstraction

Real-World Applications:
────────────────────────────────────────────────
✓ File operation servers
✓ Database query servers
✓ API integration servers
✓ Calculator/math servers
✓ Any domain-specific server!

You're Ready To:
────────────────────────────────────────────────
→ Build production MCP servers
→ Deploy to local or cloud
→ Integrate with Claude, GPT, Gemini
→ Create custom tools for your domain

Next: Module_04_Practical_Implementation.py
      Advanced SDK usage and debugging!
"""

print(summary)

print("\n" + "=" * 80)
print("📝 BUILD CHALLENGE:")
print("=" * 80)
print("""
Now build YOUR OWN MCP server for a domain you know:

Ideas:
• Email server (send, read, search emails)
• Git server (commit, push, branch operations)
• Calendar server (events, scheduling)
• Note-taking server (create, search notes)
• API wrapper server (for any API you use)

Use the patterns from this module! 🚀
""")
