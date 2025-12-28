"""
MODULE 00: Introduction to MCP - HANDS-ON EXAMPLES
====================================================

Source: https://github.com/microsoft/mcp-for-beginners/tree/main/00-Introduction
Study Guide: Module_00_Introduction_to_MCP.md

This file demonstrates MCP concepts through code simulations. While these are
simplified examples, they illustrate the core ideas of how MCP works.

EXAMPLES IN THIS FILE:
1. Simulating MCP Message Format
2. Host-Client-Server Communication Flow
3. MCP Tool Definition and Execution
4. MCP Resource Access Pattern
5. MCP Prompt Templates
6. Request-Response Pattern
7. Multiple MCP Servers Working Together
8. Error Handling in MCP
9. Permission System Simulation
10. Comparing Direct vs MCP Integration
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Optional, Callable
from enum import Enum
import json
import time

print("=" * 80)
print("MODULE 00: MCP INTRODUCTION - HANDS-ON EXAMPLES")
print("=" * 80)
print("Understanding MCP through code simulations")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: MCP Message Format - The Protocol Language
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: MCP Message Format - How MCP 'Talks'")
print("=" * 80)
print("""
CONCEPT: MCP uses JSON-RPC 2.0 format for messages.
Every message has a standard structure that both client and server understand.

ANALOGY: Like writing a letter with standard format:
- To: (recipient)
- From: (sender)
- Subject: (what it's about)
- Body: (the content)

MCP messages have:
- jsonrpc: "2.0" (protocol version)
- method: (what to do)
- params: (parameters)
- id: (message identifier)
""")

@dataclass
class MCPRequest:
    """Standard MCP request message"""
    jsonrpc: str  # Always "2.0"
    method: str   # What to do (e.g., "tools/call")
    params: Dict[str, Any]  # Parameters for the method
    id: int  # Message ID for matching responses

@dataclass
class MCPResponse:
    """Standard MCP response message"""
    jsonrpc: str  # Always "2.0"
    result: Optional[Any]  # Result if successful
    error: Optional[Dict]  # Error if failed
    id: int  # Matches the request ID

def create_tool_call_request(tool_name: str, arguments: dict, request_id: int) -> MCPRequest:
    """Helper to create a tool call request"""
    return MCPRequest(
        jsonrpc="2.0",
        method="tools/call",
        params={
            "name": tool_name,
            "arguments": arguments
        },
        id=request_id
    )

def create_success_response(result: Any, request_id: int) -> MCPResponse:
    """Helper to create a success response"""
    return MCPResponse(
        jsonrpc="2.0",
        result=result,
        error=None,
        id=request_id
    )

def create_error_response(error_code: int, error_message: str, request_id: int) -> MCPResponse:
    """Helper to create an error response"""
    return MCPResponse(
        jsonrpc="2.0",
        result=None,
        error={
            "code": error_code,
            "message": error_message
        },
        id=request_id
    )

print("\n▶ Creating MCP messages:")

# Create a request to read a file
request = create_tool_call_request(
    tool_name="read_file",
    arguments={"path": "/data/report.txt"},
    request_id=1
)

print(f"  📤 REQUEST:")
print(f"     Protocol: {request.jsonrpc}")
print(f"     Method: {request.method}")
print(f"     Tool: {request.params['name']}")
print(f"     Arguments: {request.params['arguments']}")
print(f"     ID: {request.id}")

# JSON representation (what actually gets sent)
request_json = json.dumps({
    "jsonrpc": request.jsonrpc,
    "method": request.method,
    "params": request.params,
    "id": request.id
}, indent=2)

print(f"\n  📋 As JSON (actual message):")
print(f"{request_json}")

# Create a success response
response = create_success_response(
    result={
        "content": "This is the file content...",
        "size": 1024,
        "encoding": "utf-8"
    },
    request_id=1
)

print(f"\n  📥 RESPONSE:")
print(f"     Protocol: {response.jsonrpc}")
print(f"     Result: {response.result}")
print(f"     ID: {response.id} (matches request)")

print("\n💡 KEY INSIGHT:")
print("   All MCP communication uses this standardized JSON-RPC format")
print("   Client and server both understand the structure")
print("   ID field links requests to responses")

# ==============================================================================
# EXAMPLE 2: Host-Client-Server Flow - Complete Interaction
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Complete MCP Flow - From User Request to Response")
print("=" * 80)
print("""
CONCEPT: Let's trace a complete interaction through all three components:
Host (user interface) → Client (protocol handler) → Server (capability provider)

SCENARIO: User asks Claude to read a file
""")

class MCPHost:
    """Simulates MCP Host (e.g., Claude Desktop)"""

    def __init__(self, name: str):
        self.name = name
        self.client = None

    def connect_client(self, client):
        """Connect to MCP client"""
        self.client = client
        print(f"  🖥️  [{self.name}] Connected to MCP client")

    def user_request(self, request: str) -> str:
        """Handle user's natural language request"""
        print(f"\n  👤 User: '{request}'")

        # Host determines what MCP call is needed
        if "read" in request.lower() and "file" in request.lower():
            # Extract file path (simplified)
            path = "/data/example.txt"

            print(f"  🖥️  [{self.name}] Determined action: read file '{path}'")

            # Ask user permission
            permission = self.ask_permission(f"Allow reading {path}?")

            if not permission:
                return "Permission denied by user"

            # Use client to make MCP call
            result = self.client.call_tool("read_file", {"path": path})

            return result
        else:
            return "I don't understand that request"

    def ask_permission(self, question: str) -> bool:
        """Ask user for permission (simplified - always yes for demo)"""
        print(f"  🖥️  [{self.name}] Asking user: {question}")
        print(f"  👤 User: Yes, allow")
        return True

class MCPClient:
    """Simulates MCP Client (protocol layer)"""

    def __init__(self):
        self.servers = {}
        self.request_id = 0

    def register_server(self, server_name: str, server):
        """Register an MCP server"""
        self.servers[server_name] = server
        print(f"  🔌 Client: Registered server '{server_name}'")

    def call_tool(self, tool_name: str, arguments: dict) -> Any:
        """Call a tool on an MCP server"""
        self.request_id += 1

        print(f"\n  📤 Client: Sending MCP request #{self.request_id}")
        print(f"     Tool: {tool_name}")
        print(f"     Arguments: {arguments}")

        # Create MCP request
        request = create_tool_call_request(tool_name, arguments, self.request_id)

        # Find appropriate server (simplified - just use first server)
        server = list(self.servers.values())[0]

        # Send to server
        response = server.handle_request(request)

        print(f"  📥 Client: Received response #{response.id}")

        if response.error:
            print(f"     ❌ Error: {response.error}")
            return None

        print(f"     ✅ Success: {response.result}")

        return response.result

class MCPServer:
    """Simulates MCP Server (provides capabilities)"""

    def __init__(self, name: str):
        self.name = name
        self.tools = {}

    def register_tool(self, tool_name: str, handler: Callable):
        """Register a tool handler"""
        self.tools[tool_name] = handler
        print(f"  🛠️  [{self.name}] Registered tool: {tool_name}")

    def handle_request(self, request: MCPRequest) -> MCPResponse:
        """Handle incoming MCP request"""
        print(f"\n  🖥️  [{self.name}] Received request #{request.id}")

        tool_name = request.params.get("name")
        arguments = request.params.get("arguments", {})

        print(f"     Executing tool: {tool_name}")

        # Execute the tool
        if tool_name in self.tools:
            try:
                result = self.tools[tool_name](arguments)
                return create_success_response(result, request.id)
            except Exception as e:
                return create_error_response(500, str(e), request.id)
        else:
            return create_error_response(
                404,
                f"Tool '{tool_name}' not found",
                request.id
            )

# Set up the complete MCP system
print("\n▶ Setting up MCP system:")

# Create server
file_server = MCPServer("FileOperations")

# Register tools on server
def read_file_handler(args: dict) -> dict:
    """Handle read_file tool"""
    path = args.get("path")
    # Simulate reading file
    time.sleep(0.1)
    return {
        "content": f"Contents of {path}:\nLine 1\nLine 2\nLine 3",
        "size": 24,
        "path": path
    }

file_server.register_tool("read_file", read_file_handler)

# Create client
client = MCPClient()
client.register_server("file_server", file_server)

# Create host
claude_desktop = MCPHost("Claude Desktop")
claude_desktop.connect_client(client)

# User interaction
print("\n" + "=" * 60)
print("COMPLETE USER INTERACTION:")
print("=" * 60)

result = claude_desktop.user_request("Read the file /data/example.txt and summarize it")

print(f"\n  🖥️  Claude Desktop: Received result from MCP")
print(f"  🤖 AI Processing result...")
print(f"  💬 Claude: 'I read the file. It contains 3 lines of text.'")

print("\n💡 KEY INSIGHT:")
print("   Host → Client → Server → Client → Host")
print("   Each layer has specific responsibility")
print("   User only sees the Host, MCP handles the rest!")

# ==============================================================================
# EXAMPLE 3: MCP Tool Definition - What Tools Look Like
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: MCP Tool Definition - Structure of a Tool")
print("=" * 80)
print("""
CONCEPT: Tools are THE way AI performs actions via MCP.
Each tool has a name, description, and parameter schema.

LOGIC:
- Tools are defined with JSON Schema
- Parameters specify what inputs the tool needs
- Return types can be defined
- AI uses tool metadata to know when/how to use it
""")

@dataclass
class ToolParameter:
    """Defines a tool parameter"""
    name: str
    type: str  # "string", "number", "boolean", "object", "array"
    description: str
    required: bool = True

@dataclass
class ToolDefinition:
    """Complete tool definition"""
    name: str
    description: str
    parameters: List[ToolParameter]
    returns: str  # Return type description

    def to_schema(self) -> dict:
        """Convert to JSON schema format"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": {
                "type": "object",
                "properties": {
                    param.name: {
                        "type": param.type,
                        "description": param.description
                    }
                    for param in self.parameters
                },
                "required": [p.name for p in self.parameters if p.required]
            }
        }

print("\n▶ Defining MCP tools:")

# Define read_file tool
read_file_tool = ToolDefinition(
    name="read_file",
    description="Read the complete contents of a file from the filesystem",
    parameters=[
        ToolParameter(
            name="path",
            type="string",
            description="Absolute or relative path to the file",
            required=True
        ),
        ToolParameter(
            name="encoding",
            type="string",
            description="File encoding (default: utf-8)",
            required=False
        )
    ],
    returns="string"
)

# Define write_file tool
write_file_tool = ToolDefinition(
    name="write_file",
    description="Write content to a file on the filesystem",
    parameters=[
        ToolParameter(
            name="path",
            type="string",
            description="Path where file will be written",
            required=True
        ),
        ToolParameter(
            name="content",
            type="string",
            description="Content to write to the file",
            required=True
        ),
        ToolParameter(
            name="create_dirs",
            type="boolean",
            description="Create parent directories if they don't exist",
            required=False
        )
    ],
    returns="boolean"
)

# Define web_search tool
web_search_tool = ToolDefinition(
    name="web_search",
    description="Search the internet for information",
    parameters=[
        ToolParameter(
            name="query",
            type="string",
            description="Search query string",
            required=True
        ),
        ToolParameter(
            name="max_results",
            type="number",
            description="Maximum number of results to return",
            required=False
        )
    ],
    returns="array"
)

# Display tool schemas
for tool in [read_file_tool, write_file_tool, web_search_tool]:
    print(f"\n  🛠️  Tool: {tool.name}")
    print(f"     Description: {tool.description}")
    print(f"     Parameters:")

    for param in tool.parameters:
        req = "required" if param.required else "optional"
        print(f"       • {param.name} ({param.type}, {req})")
        print(f"         {param.description}")

    print(f"     Returns: {tool.returns}")

# Show JSON schema
print(f"\n  📋 JSON Schema for 'read_file':")
schema = read_file_tool.to_schema()
print(json.dumps(schema, indent=2))

print("\n💡 KEY INSIGHT:")
print("   Tools are self-describing (AI knows what they do)")
print("   Parameters define what inputs are needed")
print("   This is how AI decides which tool to use!")

# ==============================================================================
# EXAMPLE 4: MCP Resources - Accessing Data
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: MCP Resources - Data Access Pattern")
print("=" * 80)
print("""
CONCEPT: Resources are READ-ONLY data that AI can access.
Unlike tools (which DO things), resources provide information.

EXAMPLES:
- File contents
- Database records
- API responses
- Documentation

LOGIC:
- Resources have URIs (like file://path or db://table)
- AI can list available resources
- AI can read resource contents
- Resources are passive (no side effects)
""")

@dataclass
class MCPResource:
    """Represents an MCP resource"""
    uri: str  # Unique identifier (file://path, db://table, etc.)
    name: str
    description: str
    mime_type: str  # "text/plain", "application/json", etc.

class ResourceServer:
    """MCP Server that provides resources"""

    def __init__(self):
        self.resources: Dict[str, Any] = {}

    def register_resource(self, resource: MCPResource, content: Any):
        """Register a resource"""
        self.resources[resource.uri] = {
            "metadata": resource,
            "content": content
        }
        print(f"  📚 Registered resource: {resource.uri}")

    def list_resources(self) -> List[MCPResource]:
        """List all available resources"""
        return [data["metadata"] for data in self.resources.values()]

    def read_resource(self, uri: str) -> Any:
        """Read resource content"""
        if uri not in self.resources:
            raise ValueError(f"Resource not found: {uri}")

        return self.resources[uri]["content"]

print("\n▶ Creating resource server:")

resource_server = ResourceServer()

# Register various resources
resources = [
    (
        MCPResource(
            uri="file:///data/config.json",
            name="Application Configuration",
            description="Main application settings",
            mime_type="application/json"
        ),
        {"host": "localhost", "port": 8080, "debug": True}
    ),
    (
        MCPResource(
            uri="file:///docs/api.md",
            name="API Documentation",
            description="API endpoint documentation",
            mime_type="text/markdown"
        ),
        "# API Docs\n\n## Endpoints\n- GET /users\n- POST /data"
    ),
    (
        MCPResource(
            uri="db://users/table",
            name="User Database Table",
            description="User records from database",
            mime_type="application/json"
        ),
        [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"}
        ]
    )
]

for resource, content in resources:
    resource_server.register_resource(resource, content)

# AI discovering resources
print("\n▶ AI discovering available resources:")

available = resource_server.list_resources()
print(f"\n  📋 Available resources ({len(available)}):")

for res in available:
    print(f"     • {res.name}")
    print(f"       URI: {res.uri}")
    print(f"       Type: {res.mime_type}")

# AI reading a resource
print("\n▶ AI reading a resource:")
config = resource_server.read_resource("file:///data/config.json")
print(f"  📖 Read config: {config}")

users = resource_server.read_resource("db://users/table")
print(f"  📖 Read users: {len(users)} records")

print("\n💡 KEY INSIGHT:")
print("   Resources = READ-ONLY data access")
print("   Tools = ACTIONS that can change things")
print("   Resources are discoverable (AI can list them)")

# ==============================================================================
# EXAMPLE 5: MCP Prompts - Template System
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: MCP Prompts - Reusable Conversation Templates")
print("=" * 80)
print("""
CONCEPT: Prompts are pre-built conversation starters that servers provide.
They help users quickly accomplish common tasks.

ANALOGY: Like templates in your email:
- "Meeting request" template
- "Follow-up" template
- "Thank you" template

MCP prompts:
- "Analyze this code"
- "Write tests for this function"
- "Explain this error"

LOGIC:
- Server provides prompt templates
- Templates can have arguments (placeholders)
- AI fills in the template with context
- User gets consistent, high-quality interactions
""")

@dataclass
class PromptTemplate:
    """MCP Prompt template"""
    name: str
    description: str
    arguments: List[Dict[str, str]]  # [{"name": "code", "description": "..."}]
    template: str  # The actual prompt text with placeholders

class PromptServer:
    """MCP Server that provides prompt templates"""

    def __init__(self):
        self.prompts: Dict[str, PromptTemplate] = {}

    def register_prompt(self, prompt: PromptTemplate):
        """Register a prompt template"""
        self.prompts[prompt.name] = prompt
        print(f"  📝 Registered prompt: {prompt.name}")

    def list_prompts(self) -> List[PromptTemplate]:
        """List all prompts"""
        return list(self.prompts.values())

    def get_prompt(self, name: str, arguments: dict) -> str:
        """Get filled prompt template"""
        if name not in self.prompts:
            raise ValueError(f"Prompt not found: {name}")

        prompt = self.prompts[name]

        # Fill in template
        filled = prompt.template
        for arg_name, arg_value in arguments.items():
            placeholder = f"{{{arg_name}}}"
            filled = filled.replace(placeholder, str(arg_value))

        return filled

print("\n▶ Creating prompt server:")

prompt_server = PromptServer()

# Register prompts
prompts = [
    PromptTemplate(
        name="analyze_code",
        description="Analyze code for quality and issues",
        arguments=[
            {"name": "code", "description": "Code to analyze"},
            {"name": "language", "description": "Programming language"}
        ],
        template="""Analyze this {language} code:

```{language}
{code}
```

Please review for:
1. Code quality
2. Potential bugs
3. Performance issues
4. Best practices
5. Suggestions for improvement"""
    ),
    PromptTemplate(
        name="write_tests",
        description="Generate unit tests for a function",
        arguments=[
            {"name": "function_code", "description": "Function to test"},
            {"name": "framework", "description": "Testing framework"}
        ],
        template="""Write unit tests for this function using {framework}:

```python
{function_code}
```

Include:
- Happy path tests
- Edge cases
- Error conditions
- Mock any external dependencies"""
    ),
    PromptTemplate(
        name="explain_error",
        description="Explain an error message and suggest fixes",
        arguments=[
            {"name": "error", "description": "Error message"},
            {"name": "context", "description": "Code context"}
        ],
        template="""Explain this error:

```
{error}
```

Context:
```
{context}
```

Please provide:
1. What the error means
2. Why it occurred
3. How to fix it
4. How to prevent it"""
    )
]

for prompt in prompts:
    prompt_server.register_prompt(prompt)

# Use prompts
print("\n▶ Using prompt templates:")

# Get analyze_code prompt
code_to_analyze = "def calc(x):\n    return x * 2"

filled_prompt = prompt_server.get_prompt(
    "analyze_code",
    {
        "code": code_to_analyze,
        "language": "python"
    }
)

print(f"\n  📝 Filled 'analyze_code' prompt:")
print(f"{filled_prompt[:150]}...")

# Get write_tests prompt
function_code = "def add(a, b):\n    return a + b"

test_prompt = prompt_server.get_prompt(
    "write_tests",
    {
        "function_code": function_code,
        "framework": "pytest"
    }
)

print(f"\n  📝 Filled 'write_tests' prompt:")
print(f"{test_prompt[:150]}...")

print("\n💡 KEY INSIGHT:")
print("   Prompts = Reusable templates for common tasks")
print("   Servers provide domain-specific prompts")
print("   Users get consistent, high-quality interactions")

# ==============================================================================
# EXAMPLE 6: Multiple MCP Servers - Ecosystem
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Multiple Servers - Building an Ecosystem")
print("=" * 80)
print("""
CONCEPT: One client can connect to MULTIPLE servers simultaneously.
Each server provides different capabilities. Together, they form
a powerful ecosystem!

SCENARIO: AI can access files, databases, and web - all at once!
""")

# We already have file_server, let's add more
database_server = MCPServer("DatabaseOperations")
web_server = MCPServer("WebOperations")

# Register tools on database server
def db_query_handler(args: dict) -> dict:
    """Simulate database query"""
    sql = args.get("query")
    print(f"      🗄️  Executing SQL: {sql}")
    time.sleep(0.2)
    return {
        "rows": [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ],
        "count": 2
    }

database_server.register_tool("db_query", db_query_handler)

# Register tools on web server
def web_search_handler(args: dict) -> dict:
    """Simulate web search"""
    query = args.get("query")
    print(f"      🌐 Searching: {query}")
    time.sleep(0.3)
    return {
        "results": [
            {"title": "Result 1", "url": "https://example.com/1"},
            {"title": "Result 2", "url": "https://example.com/2"}
        ],
        "count": 2
    }

web_server.register_tool("web_search", web_search_handler)

# Create client with multiple servers
multi_client = MCPClient()
multi_client.register_server("files", file_server)
multi_client.register_server("database", database_server)
multi_client.register_server("web", web_server)

print("\n▶ Client connected to multiple servers:")
print(f"  Connected servers: {list(multi_client.servers.keys())}")

# Use different servers
print("\n▶ Using tools from different servers:")

print("\n  1. File operation:")
file_result = multi_client.call_tool("read_file", {"path": "/data/test.txt"})

print("\n  2. Database operation:")
db_result = multi_client.call_tool("db_query", {"query": "SELECT * FROM users"})

print("\n  3. Web operation:")
web_result = multi_client.call_tool("web_search", {"query": "MCP protocol"})

print(f"\n  ✅ AI now has access to:")
print(f"     • File system ({len(file_server.tools)} tools)")
print(f"     • Database ({len(database_server.tools)} tools)")
print(f"     • Web ({len(web_server.tools)} tools)")

print("\n💡 KEY INSIGHT:")
print("   One client, multiple servers = powerful AI capabilities!")
print("   Each server specializes in one domain")
print("   Together they create a complete ecosystem")

# ==============================================================================
# EXAMPLE 10: Before MCP vs After MCP
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Impact Analysis - Before MCP vs After MCP")
print("=" * 80)
print("""
CONCEPT: Let's compare building an AI application the old way
vs the MCP way to see the concrete benefits.

SCENARIO: Build AI assistant that can:
- Read files
- Query database
- Search web
- Send emails
""")

print("\n📊 COMPARISON:")

print("\n" + "=" * 60)
print("BEFORE MCP (Custom Integration)")
print("=" * 60)

comparison_before = """
Code Required:
├── custom_file_handler.py         (200 lines)
│   ├── For GPT integration
│   └── Custom API wrapper
├── custom_db_handler.py            (300 lines)
│   ├── For GPT integration
│   └── SQL generation
├── custom_web_handler.py           (250 lines)
│   └── Web scraping + formatting
├── custom_email_handler.py         (150 lines)
│   └── Email sending logic
└── gpt_integration.py              (400 lines)
    └── Glue code connecting everything

If you switch from GPT to Claude:
└── Rewrite EVERYTHING for Claude! (1,300 lines again!)

Total Development Time: 3-4 weeks
Maintenance: High (multiple codebases)
Flexibility: Low (vendor lock-in)
"""

print(comparison_before)

print("\n" + "=" * 60)
print("AFTER MCP (Standardized)")
print("=" * 60)

comparison_after = """
Code Required:
├── Install existing MCP servers:
│   ├── mcp-file-server            (0 lines - install only!)
│   ├── mcp-database-server        (0 lines - install only!)
│   ├── mcp-web-server             (0 lines - install only!)
│   └── mcp-email-server           (0 lines - install only!)
│
└── Configure AI to use servers:
    └── config.json                 (~50 lines)

If you switch from GPT to Claude:
└── Update config.json (5 minutes!)

Total Development Time: 1-2 days
Maintenance: Low (server maintainers handle it)
Flexibility: High (switch AIs anytime)
Reusability: Servers work across all projects!
"""

print(comparison_after)

print("\n📈 METRICS:")

metrics = {
    "Development Time": {
        "Before MCP": "3-4 weeks",
        "After MCP": "1-2 days",
        "Improvement": "90% faster"
    },
    "Lines of Code": {
        "Before MCP": "~1,300 lines",
        "After MCP": "~50 lines",
        "Improvement": "96% less code"
    },
    "Switching AI Models": {
        "Before MCP": "3-4 weeks (rebuild everything)",
        "After MCP": "5 minutes (update config)",
        "Improvement": "99% faster"
    },
    "Maintenance Burden": {
        "Before MCP": "High (you maintain all code)",
        "After MCP": "Low (community maintains servers)",
        "Improvement": "Significantly reduced"
    }
}

for metric, data in metrics.items():
    print(f"\n  {metric}:")
    print(f"     Before: {data['Before MCP']}")
    print(f"     After:  {data['After MCP']}")
    print(f"     Impact: {data['Improvement']}")

print("\n💡 KEY INSIGHT:")
print("   MCP provides 90%+ time savings!")
print("   Code reduction: 96% less code to maintain")
print("   Flexibility: Switch AI models in minutes, not weeks")
print("   This is WHY MCP is revolutionary for AI development!")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 MODULE 00 COMPLETE - INTRODUCTION TO MCP")
print("=" * 80)

summary = """
What You've Learned:

✅ What MCP Is:
   • Standardized protocol for AI ↔ Tools communication
   • Like USB for AI - universal connector
   • Enables AI to access external capabilities

✅ Why MCP Exists:
   • Solve integration chaos
   • Avoid vendor lock-in
   • Enable code reuse
   • Provide security boundaries

✅ Three Components:
   • Host - User interface (Claude Desktop, VS Code)
   • Client - Protocol handler (sends/receives MCP messages)
   • Server - Capability provider (files, DB, web, etc.)

✅ Three Primitives:
   • Tools - Actions AI can execute (read_file, db_query)
   • Resources - Data AI can read (configs, docs)
   • Prompts - Templates for interactions

✅ Real Benefits:
   • 90% faster development
   • 96% less code
   • Switch AI models in minutes
   • Reusable across projects

Key Concepts to Remember:
─────────────────────────────────────────────────────
1. MCP = Standard protocol (like HTTP, USB)
2. Host → Client → Server (three-tier architecture)
3. Tools (actions), Resources (data), Prompts (templates)
4. JSON-RPC 2.0 message format
5. Security through user consent
6. Build once, use with any AI

You're Ready For:
─────────────────────────────────────────────────────
→ Module 01: Core Concepts (deep dive into protocol)
→ Understanding message flows
→ Learning transport mechanisms
→ Building your first MCP server!

Sources:
─────────────────────────────────────────────────────
• https://github.com/microsoft/mcp-for-beginners/tree/main/00-Introduction
• https://ai-native.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows/mcp-integration
• https://github.com/panaversity/claude-code-skills-lab
"""

print(summary)

print("\n" + "=" * 80)
print("📚 FURTHER READING:")
print("=" * 80)
print("""
Before Module 01, explore:

1. Review the three components (Host, Client, Server)
2. Think about what MCP servers YOU would build
3. Consider security implications (what should AI access?)
4. Explore existing MCP servers in the wild

Next Module: Core Concepts - How MCP Actually Works!
""")
