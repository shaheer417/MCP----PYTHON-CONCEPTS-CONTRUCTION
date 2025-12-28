"""
DATACLASSES - 10 REAL-LIFE CODING EXAMPLES
============================================

Source: https://github.com/panaversity/learn-modern-ai-python/tree/main/00_python_colab
Topic: Dataclasses - Clean Data Structures with Automatic Boilerplate

This file contains 10 comprehensive examples showing how to use dataclasses
to create clean, maintainable data structures for AI/MCP development.

WHAT ARE DATACLASSES?
Dataclasses automatically generate common methods (__init__, __repr__, __eq__,
etc.) from type-annotated class attributes. This reduces boilerplate and
improves code quality.

Auto-generated:
• __init__() - Constructor
• __repr__() - String representation
• __eq__() - Equality comparison
• __hash__() - Hash (if frozen)
• And more!

EXAMPLES:
1. Basic MCP Message Structures
2. Immutable Configuration with frozen=True
3. Default Values and Factory Functions
4. Post-Initialization Processing
5. Inheritance and Field Overriding
6. Dataclass with Validation
7. Nested Dataclasses for Complex Data
8. Dataclass for API Request/Response
9. Converting to/from JSON and Dicts
10. Ordering and Comparison Operations
"""

from dataclasses import dataclass, field, asdict, astuple, fields
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
from enum import Enum
import json

print("=" * 80)
print("DATACLASSES - 10 REAL-LIFE CODING EXAMPLES")
print("=" * 80)
print("Master clean data structures for AI-native development!")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: Basic MCP Message Structures
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: MCP Protocol Messages - Request and Response")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Building MCP (Model Context Protocol) message structures. Instead of
manually writing __init__, __repr__, and __eq__ for each message type,
dataclasses generate them automatically!

LOGIC:
- Define fields with type annotations
- Dataclass decorator auto-generates methods
- Clean, readable code with less boilerplate
""")

@dataclass
class MCPRequest:
    """Represents an MCP request message"""
    jsonrpc: str
    method: str
    params: Dict[str, Any]
    id: int

    # No __init__ needed! Auto-generated from fields above.

@dataclass
class MCPResponse:
    """Represents an MCP response message"""
    jsonrpc: str
    result: Optional[Any]
    error: Optional[Dict[str, Any]]
    id: int

@dataclass
class MCPError:
    """Represents an MCP error"""
    code: int
    message: str
    data: Optional[Dict[str, Any]] = None  # Optional field with default

print("\n▶ Creating MCP messages:")

# Create request - all fields required
request = MCPRequest(
    jsonrpc="2.0",
    method="tools/list",
    params={},
    id=1
)

print(f"  Request: {request}")
print(f"  Type: {type(request)}")

# Create response
response = MCPResponse(
    jsonrpc="2.0",
    result={"tools": ["read_file", "write_file"]},
    error=None,
    id=1
)

print(f"\n  Response: {response}")

# Create error
error = MCPError(
    code=404,
    message="Tool not found",
    data={"requested_tool": "unknown_tool"}
)

print(f"\n  Error: {error}")

# Test equality (auto-generated __eq__)
print("\n▶ Testing equality:")
request2 = MCPRequest("2.0", "tools/list", {}, 1)
print(f"  request == request2: {request == request2}")

# Test repr (auto-generated __repr__)
print("\n▶ String representation:")
print(f"  {repr(request)}")

print("\n💡 KEY TAKEAWAY:")
print("   Dataclass auto-generates: __init__, __repr__, __eq__")
print("   Perfect for protocol messages, DTOs, and data containers!")
print("   Clean syntax: just type annotations and default values.")

# ==============================================================================
# EXAMPLE 2: Immutable Configuration with frozen=True
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Immutable Configuration - Thread-Safe Settings")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Configuration objects should NOT be modified after creation to prevent
bugs. Use frozen=True to make dataclass immutable!

LOGIC:
- frozen=True makes all fields read-only
- Attempting to modify raises FrozenInstanceError
- Makes object hashable (can use as dict key or in sets)
- Thread-safe by default
""")

@dataclass(frozen=True)
class ServerConfig:
    """Immutable server configuration"""
    host: str
    port: int
    max_connections: int
    timeout_seconds: float
    enable_logging: bool

    def __post_init__(self):
        """Validate configuration (runs BEFORE freezing)"""
        if not (1 <= self.port <= 65535):
            raise ValueError(f"Invalid port: {self.port}")

        if self.max_connections < 1:
            raise ValueError("max_connections must be >= 1")

        if self.timeout_seconds <= 0:
            raise ValueError("timeout must be positive")

@dataclass(frozen=True)
class MCPServerConfig:
    """Immutable MCP server configuration"""
    server: ServerConfig
    tools_enabled: List[str]
    api_key: str

    def get_url(self) -> str:
        """Get full server URL"""
        return f"{self.server.host}:{self.server.port}"

print("\n▶ Creating immutable configurations:")

# Create nested configs
server_cfg = ServerConfig(
    host="localhost",
    port=8080,
    max_connections=100,
    timeout_seconds=30.0,
    enable_logging=True
)

mcp_cfg = MCPServerConfig(
    server=server_cfg,
    tools_enabled=["read_file", "write_file", "execute_bash"],
    api_key="secret-key-123"
)

print(f"  Config: {mcp_cfg.get_url()}")
print(f"  Tools: {', '.join(mcp_cfg.tools_enabled)}")

# Try to modify (will fail!)
print("\n▶ Attempting to modify frozen config:")
try:
    mcp_cfg.api_key = "new-key"
except Exception as e:
    print(f"  ❌ Error: {type(e).__name__}: {e}")
    print(f"  ✓ Config is immutable (as intended)!")

# Frozen dataclasses are hashable!
print("\n▶ Frozen dataclasses are hashable:")
config_set = {server_cfg, mcp_cfg}
print(f"  Created set with {len(config_set)} configs")

config_dict = {server_cfg: "primary", mcp_cfg: "backup"}
print(f"  Used as dict keys: {list(config_dict.values())}")

print("\n💡 KEY TAKEAWAY:")
print("   frozen=True makes dataclasses immutable and hashable")
print("   Use for: Configs, constants, cache keys, thread-safe data")
print("   __post_init__ runs BEFORE freezing for validation")

# ==============================================================================
# EXAMPLE 3: Default Values and Factory Functions
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Default Values - Avoiding Mutable Default Pitfalls")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You want fields with default values (empty lists, dicts, timestamps).
DANGER: Never use mutable defaults directly! Use default_factory instead.

LOGIC:
- Simple defaults: field = value (for immutable types)
- Mutable defaults: field = field(default_factory=list)
- Each instance gets its own mutable object
""")

@dataclass
class ToolExecution:
    """Record of a tool execution"""
    tool_name: str
    params: Dict[str, Any] = field(default_factory=dict)  # ✓ Correct!
    results: List[str] = field(default_factory=list)      # ✓ Correct!
    timestamp: datetime = field(default_factory=datetime.now)  # ✓ Correct!
    success: bool = True  # ✓ Immutable default OK
    retry_count: int = 0  # ✓ Immutable default OK

    # WRONG way (don't do this!):
    # params: Dict[str, Any] = {}  # ❌ Shared across instances!
    # results: List[str] = []      # ❌ Shared across instances!

@dataclass
class AIModelConfig:
    """Configuration for AI model"""
    model_name: str
    max_tokens: int = 4096
    temperature: float = 0.7
    top_p: float = 1.0
    frequency_penalty: float = 0.0
    presence_penalty: float = 0.0
    stop_sequences: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

print("\n▶ Testing default values:")

# Create instances with defaults
exec1 = ToolExecution(tool_name="read_file")
exec2 = ToolExecution(tool_name="write_file")

print(f"  Execution 1: {exec1.tool_name}")
print(f"  Execution 2: {exec2.tool_name}")

# Modify one instance
exec1.results.append("result1")
exec1.params["path"] = "/data/file.txt"

print(f"\n▶ After modifying exec1:")
print(f"  exec1.results: {exec1.results}")
print(f"  exec2.results: {exec2.results}")
print(f"  ✓ Separate lists (each instance has its own)!")

# Test with AI config
print("\n▶ AI Model configurations:")

config1 = AIModelConfig("gpt-4")
config2 = AIModelConfig("claude-3", temperature=0.9, max_tokens=8000)

print(f"  Config 1: {config1.model_name}, temp={config1.temperature}")
print(f"  Config 2: {config2.model_name}, temp={config2.temperature}")

# Each has separate metadata
config1.metadata["user"] = "alice"
config2.metadata["user"] = "bob"

print(f"  Config 1 metadata: {config1.metadata}")
print(f"  Config 2 metadata: {config2.metadata}")
print(f"  ✓ Independent metadata dicts!")

print("\n💡 KEY TAKEAWAY:")
print("   Use field(default_factory=...) for mutable defaults")
print("   Each instance gets its own list/dict/object")
print("   Prevents shared mutable state bugs!")

# ==============================================================================
# EXAMPLE 4: Post-Initialization Processing
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: Post-Init Processing - Validation and Computed Fields")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
After dataclass creates the instance, you need to:
- Validate field values
- Compute derived fields
- Normalize data
- Set up relationships

LOGIC:
- __post_init__() is called after __init__()
- Perform validation, transformations, computations
- Can modify fields (unless frozen=True)
""")

@dataclass
class MCPTool:
    """MCP Tool with validation and normalization"""
    name: str
    description: str
    parameters: List[str]
    category: str
    enabled: bool = True

    def __post_init__(self):
        """Validate and normalize after initialization"""

        # Validation
        if not self.name:
            raise ValueError("Tool name cannot be empty")

        if len(self.description) < 10:
            raise ValueError("Description must be at least 10 characters")

        # Normalization
        self.name = self.name.lower().replace(" ", "_")
        self.category = self.category.lower()

        # Computed/derived fields
        self.parameter_count = len(self.parameters)

        print(f"  ✓ Tool '{self.name}' initialized and validated")

@dataclass
class User:
    """User with automatic computed fields"""
    first_name: str
    last_name: str
    email: str
    age: int

    # These will be computed in __post_init__
    full_name: str = field(init=False)  # Not in __init__
    email_domain: str = field(init=False)
    is_adult: bool = field(init=False)

    def __post_init__(self):
        """Compute derived fields"""

        # Validation
        if self.age < 0:
            raise ValueError("Age cannot be negative")

        if "@" not in self.email:
            raise ValueError("Invalid email")

        # Compute derived fields
        self.full_name = f"{self.first_name} {self.last_name}"
        self.email_domain = self.email.split("@")[1]
        self.is_adult = self.age >= 18

        print(f"  ✓ User '{self.full_name}' created")

print("\n▶ Testing post-init validation:")

# Valid tool
try:
    tool = MCPTool(
        name="Read File",
        description="Read contents from a file on the filesystem",
        parameters=["path", "encoding"],
        category="File Operations"
    )

    print(f"     Name: {tool.name}")
    print(f"     Category: {tool.category}")
    print(f"     Parameter count: {tool.parameter_count}")

except ValueError as e:
    print(f"  ❌ Error: {e}")

# Invalid tool (description too short)
print("\n  Testing invalid tool:")
try:
    bad_tool = MCPTool(
        name="bad",
        description="short",  # Too short!
        parameters=[],
        category="test"
    )
except ValueError as e:
    print(f"  ❌ Caught validation error: {e}")

# Test user with computed fields
print("\n▶ Testing computed fields:")

user = User(
    first_name="Alice",
    last_name="Smith",
    email="alice@example.com",
    age=25
)

print(f"     Full name: {user.full_name}")
print(f"     Email domain: {user.email_domain}")
print(f"     Is adult: {user.is_adult}")

print("\n💡 KEY TAKEAWAY:")
print("   __post_init__() for validation and computed fields")
print("   field(init=False) excludes fields from __init__()")
print("   Great for data integrity and derived properties!")

# ==============================================================================
# EXAMPLE 5: Inheritance and Field Overriding
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: Dataclass Inheritance - Building Class Hierarchies")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build a hierarchy of related dataclasses (e.g., base Message class
with specific message types). Child classes inherit and extend fields.

LOGIC:
- Child dataclasses inherit fields from parent
- Can add new fields
- Can override parent field defaults
- Parent __post_init__ is called first
""")

@dataclass
class BaseMessage:
    """Base message with common fields"""
    message_id: str
    timestamp: datetime
    sender: str

    def __post_init__(self):
        print(f"  🔧 BaseMessage.__post_init__ called")

@dataclass
class RequestMessage(BaseMessage):
    """Request message with method and params"""
    method: str
    params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()  # Call parent
        print(f"  🔧 RequestMessage.__post_init__ called")

        # Validate method name
        if not self.method:
            raise ValueError("Method cannot be empty")

@dataclass
class ResponseMessage(BaseMessage):
    """Response message with result or error"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None

    def __post_init__(self):
        super().__post_init__()
        print(f"  🔧 ResponseMessage.__post_init__ called")

        # Validate response consistency
        if self.success and self.error:
            raise ValueError("Success response cannot have error")

        if not self.success and not self.error:
            raise ValueError("Failed response must have error message")

@dataclass
class Tool:
    """Base tool class"""
    name: str
    category: str
    enabled: bool = True

@dataclass
class FileTool(Tool):
    """File operation tool"""
    supported_extensions: List[str] = field(default_factory=list)
    max_file_size_mb: int = 100

@dataclass
class WebTool(Tool):
    """Web operation tool"""
    allowed_domains: List[str] = field(default_factory=list)
    timeout_seconds: int = 30

print("\n▶ Testing inheritance:")

# Create request (inherits from BaseMessage)
request = RequestMessage(
    message_id="req-001",
    timestamp=datetime.now(),
    sender="client-1",
    method="read_file",
    params={"path": "/data/test.txt"}
)

print(f"\n  Request:")
print(f"     ID: {request.message_id}")
print(f"     Method: {request.method}")
print(f"     Sender: {request.sender}")

# Create response
response = ResponseMessage(
    message_id="resp-001",
    timestamp=datetime.now(),
    sender="server",
    success=True,
    result="File contents here"
)

print(f"\n  Response:")
print(f"     Success: {response.success}")
print(f"     Result: {response.result}")

# Test tool inheritance
print("\n▶ Tool hierarchy:")

file_tool = FileTool(
    name="read_text",
    category="file",
    supported_extensions=[".txt", ".md", ".csv"],
    max_file_size_mb=50
)

web_tool = WebTool(
    name="fetch_url",
    category="web",
    allowed_domains=["example.com", "test.com"],
    timeout_seconds=60
)

print(f"  File tool: {file_tool.name} (enabled: {file_tool.enabled})")
print(f"  Web tool: {web_tool.name} (timeout: {web_tool.timeout_seconds}s)")

print("\n💡 KEY TAKEAWAY:")
print("   Dataclasses support inheritance naturally")
print("   Child inherits parent fields + adds new ones")
print("   __post_init__ chain: call super().__post_init__()")

# ==============================================================================
# EXAMPLE 6: Dataclass with Custom Validation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Advanced Validation - Business Rules and Constraints")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Implement complex validation rules that check relationships between
fields, enforce business logic, and ensure data consistency.

LOGIC:
- Use __post_init__ for validation
- Raise descriptive errors
- Validate field relationships (not just individual fields)
""")

@dataclass
class APIRateLimitConfig:
    """Rate limiting configuration with validation"""
    requests_per_minute: int
    requests_per_hour: int
    burst_size: int
    enabled: bool = True

    def __post_init__(self):
        """Validate rate limit configuration"""

        # Individual field validation
        if self.requests_per_minute < 1:
            raise ValueError("requests_per_minute must be >= 1")

        if self.requests_per_hour < 1:
            raise ValueError("requests_per_hour must be >= 1")

        if self.burst_size < 1:
            raise ValueError("burst_size must be >= 1")

        # Relational validation
        if self.requests_per_minute > self.requests_per_hour:
            raise ValueError(
                "requests_per_minute cannot exceed requests_per_hour"
            )

        # Business logic validation
        max_burst = self.requests_per_minute * 2
        if self.burst_size > max_burst:
            raise ValueError(
                f"burst_size ({self.burst_size}) too large. "
                f"Max allowed: {max_burst}"
            )

        print(f"  ✓ Valid rate limit config: "
              f"{self.requests_per_minute}/min, {self.requests_per_hour}/hour")

@dataclass
class DateRange:
    """Date range with validation"""
    start_date: datetime
    end_date: datetime
    label: str = "Date Range"

    def __post_init__(self):
        """Validate date range"""

        if self.end_date <= self.start_date:
            raise ValueError(
                f"end_date ({self.end_date}) must be after "
                f"start_date ({self.start_date})"
            )

        # Compute duration
        self.duration_days = (self.end_date - self.start_date).days

        print(f"  ✓ Valid date range: {self.duration_days} days")

print("\n▶ Testing validation:")

# Valid rate limit config
try:
    config = APIRateLimitConfig(
        requests_per_minute=60,
        requests_per_hour=3600,
        burst_size=100
    )
    print(f"     Config created successfully")

except ValueError as e:
    print(f"  ❌ Error: {e}")

# Invalid config (minute > hour)
print("\n  Testing invalid config:")
try:
    bad_config = APIRateLimitConfig(
        requests_per_minute=100,
        requests_per_hour=50,  # Invalid!
        burst_size=10
    )
except ValueError as e:
    print(f"  ❌ Caught error: {e}")

# Valid date range
print("\n▶ Testing date range:")
date_range = DateRange(
    start_date=datetime(2024, 1, 1),
    end_date=datetime(2024, 12, 31),
    label="Full Year 2024"
)

print(f"     Duration: {date_range.duration_days} days")

print("\n💡 KEY TAKEAWAY:")
print("   Validate relationships between fields in __post_init__")
print("   Enforce business rules and constraints")
print("   Fail fast with descriptive error messages!")

# ==============================================================================
# EXAMPLE 7: Nested Dataclasses for Complex Data
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 7: Nested Structures - Composing Complex Data Models")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Model complex nested data structures (API responses, configuration files,
database records). Dataclasses compose naturally.

LOGIC:
- Use dataclasses as field types
- Create nested structures
- Each level is type-safe and well-defined
""")

@dataclass
class Address:
    """Address information"""
    street: str
    city: str
    state: str
    zip_code: str
    country: str = "USA"

@dataclass
class ContactInfo:
    """Contact information"""
    email: str
    phone: str
    address: Address

@dataclass
class Organization:
    """Organization details"""
    name: str
    website: str
    contact: ContactInfo

@dataclass
class ToolMetadata:
    """Metadata for an MCP tool"""
    version: str
    author: str
    organization: Organization
    tags: List[str]

@dataclass
class MCPToolDefinition:
    """Complete MCP tool definition"""
    name: str
    description: str
    parameters: List[str]
    metadata: ToolMetadata
    created_at: datetime = field(default_factory=datetime.now)

print("\n▶ Building nested structure:")

# Build from inside out
address = Address(
    street="123 Main St",
    city="San Francisco",
    state="CA",
    zip_code="94102"
)

contact = ContactInfo(
    email="contact@anthropic.com",
    phone="555-0123",
    address=address
)

org = Organization(
    name="Anthropic",
    website="https://anthropic.com",
    contact=contact
)

metadata = ToolMetadata(
    version="1.0.0",
    author="Claude",
    organization=org,
    tags=["file", "io", "utility"]
)

tool = MCPToolDefinition(
    name="read_file",
    description="Read contents from a file",
    parameters=["path", "encoding"],
    metadata=metadata
)

print(f"  Tool: {tool.name}")
print(f"  Version: {tool.metadata.version}")
print(f"  Author: {tool.metadata.author}")
print(f"  Organization: {tool.metadata.organization.name}")
print(f"  Location: {tool.metadata.organization.contact.address.city}")
print(f"  Tags: {', '.join(tool.metadata.tags)}")

# Access nested data easily
print(f"\n▶ Navigating nested structure:")
print(f"  Email: {tool.metadata.organization.contact.email}")
print(f"  Address: {tool.metadata.organization.contact.address.street}")

print("\n💡 KEY TAKEAWAY:")
print("   Dataclasses compose naturally for nested data")
print("   Type-safe navigation through structure")
print("   Perfect for: API responses, configs, complex models")

# ==============================================================================
# EXAMPLE 8: Dataclass for API Request/Response
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 8: API Communication - Type-Safe Request/Response")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Define request and response schemas for API communication. Dataclasses
provide type safety and automatic serialization.

LOGIC:
- Define request/response as dataclasses
- Use for type hints in functions
- Easy serialization/deserialization
""")

class HTTPMethod(Enum):
    """HTTP methods"""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"

@dataclass
class HTTPHeaders:
    """HTTP headers"""
    content_type: str = "application/json"
    authorization: Optional[str] = None
    user_agent: str = "MCP-Client/1.0"
    custom_headers: Dict[str, str] = field(default_factory=dict)

@dataclass
class APIRequest:
    """Generic API request"""
    method: HTTPMethod
    endpoint: str
    headers: HTTPHeaders
    body: Optional[Dict[str, Any]] = None
    timeout: int = 30

    def to_curl(self) -> str:
        """Generate curl command"""
        cmd = f"curl -X {self.method.value} {self.endpoint}"

        if self.headers.authorization:
            cmd += f" -H 'Authorization: {self.headers.authorization}'"

        cmd += f" -H 'Content-Type: {self.headers.content_type}'"

        if self.body:
            cmd += f" -d '{json.dumps(self.body)}'"

        return cmd

@dataclass
class APIResponse:
    """Generic API response"""
    status_code: int
    headers: Dict[str, str]
    body: Any
    latency_ms: float

    @property
    def is_success(self) -> bool:
        """Check if response is successful"""
        return 200 <= self.status_code < 300

    @property
    def is_error(self) -> bool:
        """Check if response is error"""
        return self.status_code >= 400

@dataclass
class ToolCallRequest(APIRequest):
    """Specific request for calling MCP tool"""
    tool_name: str = ""
    tool_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Set up tool-specific request"""
        if not self.body:
            self.body = {
                "tool": self.tool_name,
                "parameters": self.tool_params
            }

print("\n▶ Creating API requests:")

# Generic API request
headers = HTTPHeaders(
    authorization="Bearer secret-token-123",
    custom_headers={"X-Client-ID": "client-001"}
)

request = APIRequest(
    method=HTTPMethod.POST,
    endpoint="https://api.example.com/v1/tools",
    headers=headers,
    body={"action": "list_tools"}
)

print(f"  Request: {request.method.value} {request.endpoint}")
print(f"  Curl: {request.to_curl()[:80]}...")

# Tool-specific request
tool_request = ToolCallRequest(
    method=HTTPMethod.POST,
    endpoint="https://mcp-server.com/execute",
    headers=headers,
    tool_name="read_file",
    tool_params={"path": "/data/test.txt"}
)

print(f"\n  Tool Request: {tool_request.tool_name}")
print(f"  Body: {tool_request.body}")

# Create response
response = APIResponse(
    status_code=200,
    headers={"content-type": "application/json"},
    body={"result": "File contents"},
    latency_ms=45.2
)

print(f"\n  Response:")
print(f"     Status: {response.status_code}")
print(f"     Success: {response.is_success}")
print(f"     Latency: {response.latency_ms}ms")

print("\n💡 KEY TAKEAWAY:")
print("   Dataclasses perfect for API request/response schemas")
print("   Type-safe, self-documenting, easy to serialize")
print("   Add methods for utilities (to_curl, is_success, etc.)")

# ==============================================================================
# EXAMPLE 9: Converting to/from JSON and Dicts
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 9: Serialization - JSON and Dict Conversion")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Convert dataclasses to/from JSON for API communication, file storage,
or network transmission. Use asdict() and custom from_dict() methods.

LOGIC:
- asdict() converts dataclass to dict
- json.dumps() for JSON string
- Custom from_dict() classmethod for deserialization
""")

@dataclass
class AIModel:
    """AI model configuration"""
    model_id: str
    model_name: str
    provider: str
    max_tokens: int
    temperature: float
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'AIModel':
        """Create instance from dictionary"""
        return cls(**data)

    @classmethod
    def from_json(cls, json_str: str) -> 'AIModel':
        """Create instance from JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)

@dataclass
class Execution:
    """Execution record"""
    execution_id: str
    tool_name: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    result: Optional[Any] = None

    def to_dict(self) -> dict:
        """Convert to dict with datetime serialization"""
        data = asdict(self)

        # Convert datetimes to ISO format
        data['started_at'] = self.started_at.isoformat()

        if self.completed_at:
            data['completed_at'] = self.completed_at.isoformat()

        return data

    def to_json(self) -> str:
        """Convert to JSON"""
        return json.dumps(self.to_dict(), indent=2)

    @classmethod
    def from_dict(cls, data: dict) -> 'Execution':
        """Create from dict with datetime parsing"""
        # Parse datetime strings
        data['started_at'] = datetime.fromisoformat(data['started_at'])

        if data.get('completed_at'):
            data['completed_at'] = datetime.fromisoformat(data['completed_at'])

        return cls(**data)

print("\n▶ Serialization examples:")

# Create model
model = AIModel(
    model_id="model-001",
    model_name="Claude-3-Opus",
    provider="Anthropic",
    max_tokens=4096,
    temperature=0.7,
    tags=["large", "capable", "creative"]
)

# Convert to dict
model_dict = model.to_dict()
print(f"  Dictionary:")
print(f"     {model_dict}")

# Convert to JSON
model_json = model.to_json()
print(f"\n  JSON:")
print(f"     {model_json[:100]}...")

# Deserialize from JSON
print("\n▶ Deserialization:")
restored_model = AIModel.from_json(model_json)
print(f"  Restored model: {restored_model.model_name}")
print(f"  Tags: {restored_model.tags}")
print(f"  Original == Restored: {model == restored_model}")

# Test with datetime handling
print("\n▶ DateTime serialization:")

execution = Execution(
    execution_id="exec-001",
    tool_name="read_file",
    started_at=datetime.now(),
    completed_at=datetime.now(),
    result="Success"
)

exec_json = execution.to_json()
print(f"  JSON (with datetimes):")
print(f"     {exec_json[:150]}...")

restored_exec = Execution.from_dict(json.loads(exec_json))
print(f"\n  Restored execution: {restored_exec.execution_id}")
print(f"  Started: {restored_exec.started_at}")

print("\n💡 KEY TAKEAWAY:")
print("   asdict() for dict conversion")
print("   Custom to_json/from_json for serialization")
print("   Handle special types (datetime) in conversions")

# ==============================================================================
# EXAMPLE 10: Ordering and Comparison Operations
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Comparison and Ordering - Sortable Dataclasses")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Need to sort dataclasses by specific fields (priority, timestamp, score).
Use order=True to auto-generate comparison methods.

LOGIC:
- order=True generates __lt__, __le__, __gt__, __ge__
- Compares based on field order (top to bottom)
- Enable sorting and comparisons
""")

@dataclass(order=True)
class Priority:
    """Priority with ordering"""
    level: int  # Primary sort key
    name: str = field(compare=False)  # Don't use in comparison

@dataclass(order=True)
class Task:
    """Task with priority ordering"""
    priority: int  # Primary sort key
    created_at: datetime = field(compare=False)  # Don't compare
    name: str = field(compare=False)  # Don't compare
    description: str = field(compare=False)  # Don't compare

    def __str__(self):
        return f"Task(priority={self.priority}, name='{self.name}')"

@dataclass(order=True)
class Score:
    """AI model score with ordering"""
    accuracy: float  # Primary
    speed: float     # Secondary
    cost: float      # Tertiary
    model_name: str = field(compare=False)  # Don't compare

print("\n▶ Testing ordering:")

# Create priorities
p1 = Priority(level=1, name="High")
p2 = Priority(level=2, name="Medium")
p3 = Priority(level=1, name="High-2")  # Same level as p1

print(f"  p1 < p2: {p1 < p2}")
print(f"  p1 == p3: {p1 == p3}")  # Same level!
print(f"  p2 > p1: {p2 > p1}")

# Create and sort tasks
print("\n▶ Sorting tasks by priority:")

tasks = [
    Task(priority=3, created_at=datetime.now(), name="Low priority",
         description="Can wait"),
    Task(priority=1, created_at=datetime.now(), name="Critical bug",
         description="Fix immediately"),
    Task(priority=2, created_at=datetime.now(), name="Feature request",
         description="Nice to have"),
    Task(priority=1, created_at=datetime.now(), name="Security issue",
         description="Fix ASAP"),
]

print("  Before sorting:")
for task in tasks:
    print(f"     {task}")

sorted_tasks = sorted(tasks)

print("\n  After sorting (by priority):")
for task in sorted_tasks:
    print(f"     {task}")

# Test with scores
print("\n▶ Sorting model scores:")

scores = [
    Score(accuracy=0.95, speed=100.0, cost=0.01, model_name="Model-A"),
    Score(accuracy=0.95, speed=150.0, cost=0.02, model_name="Model-B"),  # Faster, same accuracy
    Score(accuracy=0.90, speed=200.0, cost=0.005, model_name="Model-C"),
    Score(accuracy=0.95, speed=100.0, cost=0.008, model_name="Model-D"),  # Same as A but cheaper
]

print("  Unsorted:")
for score in scores:
    print(f"     {score.model_name}: acc={score.accuracy}, "
          f"speed={score.speed}, cost=${score.cost}")

sorted_scores = sorted(scores, reverse=True)  # Highest first

print("\n  Sorted (accuracy > speed > cost):")
for score in sorted_scores:
    print(f"     {score.model_name}: acc={score.accuracy}, "
          f"speed={score.speed}, cost=${score.cost}")

# Manual comparisons
print("\n▶ Manual comparisons:")
print(f"  Model-A == Model-D (same fields): {scores[0] == scores[3]}")
print(f"  Model-A > Model-C (better accuracy): {scores[0] > scores[2]}")
print(f"  Model-B > Model-A (same accuracy, faster): {scores[1] > scores[0]}")

print("\n💡 KEY TAKEAWAY:")
print("   order=True for automatic ordering/comparison")
print("   field(compare=False) excludes fields from comparison")
print("   Fields compared top-to-bottom (priority order)")
print("   Use for: Sorting, priority queues, rankings")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 ALL 10 DATACLASS EXAMPLES COMPLETED!")
print("=" * 80)

summary = """
What You've Mastered:

1. ✅ Basic Structures - MCP messages with auto-generated methods
2. ✅ Immutable Config - frozen=True for thread-safe data
3. ✅ Default Values - field(default_factory) for mutable defaults
4. ✅ Post-Init - Validation and computed fields
5. ✅ Inheritance - Building class hierarchies
6. ✅ Custom Validation - Complex business rules
7. ✅ Nested Structures - Composing complex models
8. ✅ API Schemas - Type-safe request/response
9. ✅ Serialization - JSON and dict conversion
10. ✅ Ordering - Sortable dataclasses with comparisons

Key Dataclass Features:
────────────────────────────────────────────────
• Auto-generated: __init__, __repr__, __eq__, __hash__
• frozen=True → Immutable + hashable
• field(default_factory=list) → Mutable defaults
• field(init=False) → Exclude from __init__
• field(compare=False) → Exclude from comparisons
• order=True → Auto-generate < > <= >=
• __post_init__() → Validation and computed fields

Common Parameters:
────────────────────────────────────────────────
@dataclass(
    frozen=True,      # Make immutable
    order=True,       # Enable ordering
    eq=True,          # Generate __eq__ (default)
    repr=True,        # Generate __repr__ (default)
    init=True         # Generate __init__ (default)
)

Best Practices:
────────────────────────────────────────────────
✓ Use for data containers, DTOs, messages
✓ Use frozen=True for configs and immutable data
✓ Use field(default_factory) for lists/dicts
✓ Validate in __post_init__()
✓ Type annotate all fields
✓ Use for API schemas and protocol messages

When to Use Dataclasses:
────────────────────────────────────────────────
✓ Data structures (not business logic)
✓ API request/response models
✓ Configuration objects
✓ Protocol messages (MCP, JSON-RPC)
✓ Database records/ORM models
✓ Simple value objects

Next: Move to Pydantic examples! 🚀
"""

print(summary)

print("\n" + "=" * 80)
print("📝 PRACTICE SUGGESTIONS:")
print("=" * 80)
print("""
1. Convert existing classes to dataclasses
2. Build an API schema using dataclasses
3. Create a configuration system with frozen dataclasses
4. Implement a message protocol (like MCP)
5. Build nested data models for complex domains

Ready for Pydantic? Run: 05_Pydantic_10_Examples.py
""")
