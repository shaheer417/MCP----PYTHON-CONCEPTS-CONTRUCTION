"""
PYDANTIC - 10 REAL-LIFE CODING EXAMPLES
=========================================

Source: https://github.com/panaversity/learn-modern-ai-python/tree/main/00_python_colab
Topic: Pydantic - Data Validation and Settings Management

This file contains 10 comprehensive examples showing how to use Pydantic
for automatic data validation, type conversion, and settings management
in AI/MCP development.

WHAT IS PYDANTIC?
Pydantic provides data validation and settings management using Python type
hints. It's like dataclasses but with AUTOMATIC VALIDATION and TYPE CONVERSION.

Key Differences from Dataclasses:
• Dataclasses: Structure only
• Pydantic: Structure + Validation + Parsing + Conversion

EXAMPLES:
1. Basic Model with Automatic Validation
2. Custom Validators and Field Validation
3. Automatic Type Conversion
4. Nested Models for Complex Data
5. Settings Management from Environment
6. API Request/Response with Validation
7. JSON Schema Generation
8. Model Configuration and Customization
9. Validators with Dependencies
10. Integration with FastAPI/MCP
"""

from pydantic import BaseModel, Field, validator, root_validator, ValidationError
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum
import json
import os

print("=" * 80)
print("PYDANTIC - 10 REAL-LIFE CODING EXAMPLES")
print("=" * 80)
print("Master data validation for production AI applications!")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: Basic Model with Automatic Validation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Automatic Validation - Catch Errors Early")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Building an MCP tool schema. You need to ensure all tool definitions
are valid BEFORE they're used. Pydantic validates on creation!

LOGIC:
- Define model with type hints
- Pydantic validates types automatically
- Invalid data raises ValidationError immediately
- No need for manual type checking
""")

class MCPTool(BaseModel):
    """MCP Tool definition with automatic validation"""
    name: str
    description: str
    category: str
    parameters: List[str]
    timeout: float
    enabled: bool

# Valid tool
print("\n▶ Creating VALID tool:")
try:
    tool = MCPTool(
        name="read_file",
        description="Read contents from a file",
        category="file_operations",
        parameters=["path", "encoding"],
        timeout=30.0,
        enabled=True
    )

    print(f"  ✓ Tool created: {tool.name}")
    print(f"     Parameters: {tool.parameters}")
    print(f"     Timeout: {tool.timeout}s")

except ValidationError as e:
    print(f"  ❌ Validation failed: {e}")

# Invalid tool (wrong types!)
print("\n▶ Creating INVALID tool (wrong types):")
try:
    bad_tool = MCPTool(
        name="bad_tool",
        description="Test",
        category="test",
        parameters="not a list",  # ❌ Should be List[str]!
        timeout="thirty",         # ❌ Should be float!
        enabled="yes"             # ❌ Should be bool!
    )

except ValidationError as e:
    print(f"  ❌ Validation error:")
    errors = e.errors()
    for error in errors:
        field = error['loc'][0]
        msg = error['msg']
        print(f"     • {field}: {msg}")

print("\n💡 KEY TAKEAWAY:")
print("   Pydantic validates types AUTOMATICALLY on creation")
print("   No manual isinstance() checks needed!")
print("   Catches errors before they cause bugs in production")

# ==============================================================================
# EXAMPLE 2: Custom Validators and Field Validation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Custom Validators - Business Logic Validation")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You need custom validation rules beyond type checking:
- Port numbers must be 1-65535
- Email format validation
- Tool names must be snake_case
- Descriptions must be meaningful (min length)

LOGIC:
- Use @validator decorator for custom validation
- Access field value and validate it
- Raise ValueError for invalid data
- Can transform/normalize data
""")

class MCPServerConfig(BaseModel):
    """MCP Server configuration with custom validation"""
    name: str = Field(..., min_length=3, max_length=50)
    host: str
    port: int
    max_connections: int
    api_key: str
    allowed_origins: List[str]

    @validator('name')
    def validate_name(cls, v):
        """Ensure name is snake_case"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Name must be alphanumeric (underscores/hyphens allowed)')

        # Normalize to lowercase
        return v.lower()

    @validator('port')
    def validate_port(cls, v):
        """Ensure port is in valid range"""
        if not (1 <= v <= 65535):
            raise ValueError(f'Port must be between 1-65535, got {v}')
        return v

    @validator('max_connections')
    def validate_max_connections(cls, v):
        """Ensure reasonable connection limit"""
        if v < 1:
            raise ValueError('max_connections must be >= 1')

        if v > 10000:
            raise ValueError('max_connections seems too high (max: 10000)')

        return v

    @validator('api_key')
    def validate_api_key(cls, v):
        """Ensure API key has minimum security"""
        if len(v) < 16:
            raise ValueError('API key must be at least 16 characters')

        return v

    @validator('allowed_origins')
    def validate_origins(cls, v):
        """Ensure at least one origin is allowed"""
        if not v:
            raise ValueError('Must specify at least one allowed origin')

        # Normalize origins
        return [origin.lower() for origin in v]

print("\n▶ Testing custom validators:")

# Valid config
print("\n  Creating VALID config:")
try:
    config = MCPServerConfig(
        name="My_MCP_Server",
        host="localhost",
        port=8080,
        max_connections=100,
        api_key="super-secret-key-12345",
        allowed_origins=["http://localhost:3000", "https://example.com"]
    )

    print(f"  ✓ Config created: {config.name}")
    print(f"     Host: {config.host}:{config.port}")
    print(f"     Origins: {config.allowed_origins}")

except ValidationError as e:
    print(f"  ❌ Error: {e}")

# Invalid port
print("\n  Testing invalid port:")
try:
    bad_config = MCPServerConfig(
        name="test",
        host="localhost",
        port=99999,  # ❌ Invalid!
        max_connections=10,
        api_key="valid-key-1234567890",
        allowed_origins=["http://localhost"]
    )
except ValidationError as e:
    print(f"  ❌ Caught: {e.errors()[0]['msg']}")

# Invalid API key
print("\n  Testing short API key:")
try:
    bad_config = MCPServerConfig(
        name="test",
        host="localhost",
        port=8080,
        max_connections=10,
        api_key="short",  # ❌ Too short!
        allowed_origins=["http://localhost"]
    )
except ValidationError as e:
    print(f"  ❌ Caught: {e.errors()[0]['msg']}")

print("\n💡 KEY TAKEAWAY:")
print("   @validator for custom validation logic")
print("   Can validate AND transform data")
print("   Runs automatically on model creation")

# ==============================================================================
# EXAMPLE 3: Automatic Type Conversion
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Type Coercion - Automatic Type Conversion")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Data from JSON, environment variables, or user input comes as strings.
Pydantic automatically converts to correct types!

LOGIC:
- Pydantic tries to convert values to expected type
- "42" → 42 (string to int)
- "true" → True (string to bool)
- "3.14" → 3.14 (string to float)
- Fails if conversion impossible
""")

class AIModelSettings(BaseModel):
    """AI model settings with automatic type conversion"""
    model_name: str
    max_tokens: int
    temperature: float
    top_p: float
    stream: bool
    stop_sequences: List[str]

print("\n▶ Creating from string values (simulating JSON/env vars):")

# Data from JSON (all strings!)
json_data = {
    "model_name": "claude-3-opus",
    "max_tokens": "4096",        # String!
    "temperature": "0.7",        # String!
    "top_p": "1.0",              # String!
    "stream": "true",            # String!
    "stop_sequences": ["\\n\\n", "Human:", "Assistant:"]
}

settings = AIModelSettings(**json_data)

print(f"  ✓ Model created from strings!")
print(f"     max_tokens: {settings.max_tokens} (type: {type(settings.max_tokens).__name__})")
print(f"     temperature: {settings.temperature} (type: {type(settings.temperature).__name__})")
print(f"     stream: {settings.stream} (type: {type(settings.stream).__name__})")

# Pydantic handles various boolean formats
print("\n▶ Boolean conversion flexibility:")

bool_tests = [
    {"stream": "true"},
    {"stream": "True"},
    {"stream": "1"},
    {"stream": "yes"},
    {"stream": True},
]

for i, data in enumerate(bool_tests):
    full_data = {**json_data, **data}
    model = AIModelSettings(**full_data)
    print(f"  Input: {data['stream']} → Output: {model.stream} (bool)")

# Test conversion failures
print("\n▶ Testing conversion failures:")
try:
    bad_settings = AIModelSettings(
        model_name="test",
        max_tokens="not_a_number",  # Can't convert!
        temperature=0.5,
        top_p=1.0,
        stream=True,
        stop_sequences=[]
    )
except ValidationError as e:
    print(f"  ❌ Caught: {e.errors()[0]['msg']}")

print("\n💡 KEY TAKEAWAY:")
print("   Pydantic auto-converts compatible types")
print("   Perfect for: JSON APIs, env vars, user input")
print("   Saves manual parsing and conversion code")

# ==============================================================================
# EXAMPLE 4: Nested Models for Complex Data
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: Nested Validation - Complex Data Structures")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Model complex nested data (API responses, configuration files).
Pydantic validates ENTIRE structure recursively!

LOGIC:
- Use Pydantic models as field types
- Validation cascades down the tree
- Each level is validated independently
- Type-safe navigation through structure
""")

class ToolParameter(BaseModel):
    """Parameter definition for a tool"""
    name: str = Field(..., min_length=1)
    type: str = Field(..., regex="^(string|number|boolean|object|array)$")
    description: str = Field(..., min_length=5)
    required: bool = True
    default: Optional[Any] = None

    @validator('default')
    def validate_default(cls, v, values):
        """Ensure optional parameters have defaults"""
        if not values.get('required') and v is None:
            raise ValueError("Optional parameters must have a default value")
        return v

class ToolMetadata(BaseModel):
    """Tool metadata"""
    version: str = Field(..., regex=r"^\d+\.\d+\.\d+$")  # Semver
    author: str
    license: str
    tags: List[str]

    @validator('tags')
    def validate_tags(cls, v):
        """Ensure tags are non-empty and unique"""
        if not v:
            raise ValueError("Must have at least one tag")

        if len(v) != len(set(v)):
            raise ValueError("Tags must be unique")

        return v

class CompleteToolDefinition(BaseModel):
    """Complete tool definition with nested validation"""
    name: str = Field(..., regex="^[a-z][a-z0-9_]*$")
    description: str = Field(..., min_length=20)
    parameters: List[ToolParameter]
    metadata: ToolMetadata
    returns: str

    @validator('parameters')
    def validate_parameters(cls, v):
        """Ensure parameter names are unique"""
        names = [p.name for p in v]

        if len(names) != len(set(names)):
            raise ValueError("Parameter names must be unique")

        return v

print("\n▶ Creating nested validated structure:")

try:
    tool = CompleteToolDefinition(
        name="read_file",
        description="Read the complete contents of a file from the filesystem",
        parameters=[
            ToolParameter(
                name="path",
                type="string",
                description="Path to the file to read",
                required=True
            ),
            ToolParameter(
                name="encoding",
                type="string",
                description="File encoding (e.g., utf-8)",
                required=False,
                default="utf-8"
            ),
            ToolParameter(
                name="max_size_mb",
                type="number",
                description="Maximum file size to read",
                required=False,
                default=10
            )
        ],
        metadata=ToolMetadata(
            version="1.2.3",
            author="Claude",
            license="MIT",
            tags=["file", "io", "filesystem"]
        ),
        returns="string"
    )

    print(f"  ✓ Complete tool created: {tool.name}")
    print(f"     Parameters: {len(tool.parameters)}")
    print(f"     Version: {tool.metadata.version}")
    print(f"     Tags: {', '.join(tool.metadata.tags)}")

except ValidationError as e:
    print(f"  ❌ Validation failed:")
    for error in e.errors():
        print(f"     {error}")

# Test nested validation failure
print("\n▶ Testing nested validation (invalid version format):")
try:
    bad_tool = CompleteToolDefinition(
        name="test_tool",
        description="This is a test tool with enough description length",
        parameters=[],
        metadata=ToolMetadata(
            version="1.2",  # ❌ Invalid semver!
            author="Test",
            license="MIT",
            tags=["test"]
        ),
        returns="string"
    )
except ValidationError as e:
    print(f"  ❌ Caught nested validation error:")
    print(f"     {e.errors()[0]['loc']}: {e.errors()[0]['msg']}")

print("\n💡 KEY TAKEAWAY:")
print("   Nested models are validated recursively")
print("   Entire data structure is type-safe and validated")
print("   Perfect for complex API schemas!")

# ==============================================================================
# EXAMPLE 5: Settings Management from Environment Variables
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: Settings Management - Load from Environment")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Load application settings from environment variables (12-factor app pattern).
Pydantic handles parsing, validation, and type conversion automatically!

LOGIC:
- Use BaseSettings (from pydantic)
- Reads from environment variables
- Auto-converts types
- Validates configuration
""")

# Note: Using BaseModel here since BaseSettings requires pydantic-settings package
# In real projects: from pydantic_settings import BaseSettings

class AppSettings(BaseModel):
    """Application settings (simulates environment loading)"""

    # API Configuration
    api_host: str = "localhost"
    api_port: int = 8080
    api_key: str = ""

    # Database Configuration
    database_url: str = "postgresql://localhost/db"
    database_pool_size: int = 10

    # AI Model Configuration
    ai_model: str = "claude-3-opus"
    ai_max_tokens: int = 4096
    ai_temperature: float = 0.7

    # Feature Flags
    enable_caching: bool = True
    enable_logging: bool = True
    debug_mode: bool = False

    class Config:
        env_prefix = "APP_"  # Look for APP_API_HOST, APP_API_PORT, etc.
        case_sensitive = False

print("\n▶ Loading settings (simulated):")

# Simulate environment variables
env_settings = {
    "api_host": "production.example.com",
    "api_port": "9000",           # String will be converted to int!
    "api_key": "prod-key-123",
    "database_pool_size": "20",   # String to int
    "ai_temperature": "0.9",      # String to float
    "enable_caching": "true",     # String to bool
    "debug_mode": "false"         # String to bool
}

settings = AppSettings(**env_settings)

print(f"  ✓ Settings loaded:")
print(f"     API: {settings.api_host}:{settings.api_port}")
print(f"     Database pool: {settings.database_pool_size}")
print(f"     AI temp: {settings.ai_temperature}")
print(f"     Caching: {settings.enable_caching}")
print(f"     Debug: {settings.debug_mode}")

# Verify types were converted
print(f"\n  Type conversions:")
print(f"     port type: {type(settings.api_port).__name__}")
print(f"     temperature type: {type(settings.ai_temperature).__name__}")
print(f"     caching type: {type(settings.enable_caching).__name__}")

print("\n💡 KEY TAKEAWAY:")
print("   Pydantic perfect for loading environment configurations")
print("   Auto-converts types from strings")
print("   Use pydantic-settings for real environment integration")

# ==============================================================================
# EXAMPLE 6: API Request/Response with Validation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: API Schemas - Type-Safe Request/Response")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Define request and response schemas for an API. Pydantic ensures
all requests are valid BEFORE processing and all responses conform
to the schema BEFORE sending.

LOGIC:
- Define separate Request and Response models
- Validate incoming requests
- Ensure outgoing responses are valid
- Auto-generate API documentation from schemas
""")

class ToolCallRequest(BaseModel):
    """Request to call an MCP tool"""
    tool_name: str = Field(..., regex="^[a-z][a-z0-9_]*$")
    arguments: Dict[str, Any]
    timeout: float = Field(default=30.0, gt=0, le=300)
    retry_count: int = Field(default=0, ge=0, le=5)

    @validator('arguments')
    def validate_arguments(cls, v):
        """Ensure arguments is not empty"""
        if not v:
            raise ValueError("Arguments cannot be empty")
        return v

class ToolCallResponse(BaseModel):
    """Response from tool execution"""
    success: bool
    result: Optional[Any] = None
    error: Optional[str] = None
    execution_time_ms: float = Field(..., ge=0)
    retry_count: int = 0

    @root_validator
    def validate_response_consistency(cls, values):
        """Cross-field validation"""
        success = values.get('success')
        result = values.get('result')
        error = values.get('error')

        if success and error:
            raise ValueError("Success response cannot have error")

        if not success and not error:
            raise ValueError("Failed response must have error message")

        if success and result is None:
            raise ValueError("Success response should have result")

        return values

print("\n▶ Creating API request:")

request = ToolCallRequest(
    tool_name="read_file",
    arguments={"path": "/data/test.txt", "encoding": "utf-8"},
    timeout=10.0
)

print(f"  ✓ Request: {request.tool_name}")
print(f"     Arguments: {request.arguments}")
print(f"     Timeout: {request.timeout}s")

# Valid successful response
print("\n▶ Creating successful response:")
success_response = ToolCallResponse(
    success=True,
    result="File contents here...",
    execution_time_ms=45.3
)

print(f"  ✓ Response: success={success_response.success}")
print(f"     Result: {success_response.result}")

# Valid error response
print("\n▶ Creating error response:")
error_response = ToolCallResponse(
    success=False,
    error="File not found: /missing.txt",
    execution_time_ms=5.1
)

print(f"  ✓ Response: success={error_response.success}")
print(f"     Error: {error_response.error}")

# Invalid response (success but with error)
print("\n▶ Testing invalid response (success=True but has error):")
try:
    invalid_response = ToolCallResponse(
        success=True,
        result="data",
        error="This shouldn't be here!",  # ❌ Contradictory!
        execution_time_ms=10.0
    )
except ValidationError as e:
    print(f"  ❌ Caught: {e.errors()[0]['msg']}")

print("\n💡 KEY TAKEAWAY:")
print("   @root_validator for cross-field validation")
print("   Ensures logical consistency across fields")
print("   Use for API contracts and protocol messages")

# ==============================================================================
# EXAMPLE 7: JSON Schema Generation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 7: JSON Schema Generation - Automatic API Documentation")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Generate OpenAPI/JSON Schema documentation from Pydantic models.
No manual documentation needed - schema is generated from code!

LOGIC:
- model.schema() generates JSON Schema
- model.schema_json() returns JSON string
- Includes: types, descriptions, constraints
- Perfect for API documentation tools
""")

class UserProfile(BaseModel):
    """User profile information"""

    # Field() allows adding descriptions and constraints
    user_id: str = Field(..., description="Unique user identifier")
    username: str = Field(..., min_length=3, max_length=30,
                         description="Username for login")
    email: str = Field(..., description="User email address")
    age: Optional[int] = Field(None, ge=0, le=150,
                              description="User age in years")
    roles: List[str] = Field(default_factory=list,
                            description="User roles and permissions")

    class Config:
        schema_extra = {
            "example": {
                "user_id": "usr-12345",
                "username": "alice",
                "email": "alice@example.com",
                "age": 25,
                "roles": ["user", "admin"]
            }
        }

print("\n▶ Generating JSON Schema:")

# Get schema as dict
schema = UserProfile.schema()

print(f"  ✓ Schema generated for: {schema['title']}")
print(f"     Properties: {list(schema['properties'].keys())}")
print(f"     Required: {schema.get('required', [])}")

# Show schema details
print(f"\n  📋 Field Schemas:")
for field_name, field_schema in schema['properties'].items():
    print(f"     {field_name}:")
    print(f"       Type: {field_schema.get('type')}")
    print(f"       Description: {field_schema.get('description', 'N/A')}")

# Get as JSON
schema_json = UserProfile.schema_json(indent=2)
print(f"\n  📄 Full JSON Schema (first 200 chars):")
print(f"     {schema_json[:200]}...")

print("\n💡 KEY TAKEAWAY:")
print("   .schema() generates JSON Schema automatically")
print("   Use Field() to add descriptions and constraints")
print("   Perfect for: OpenAPI docs, API documentation")

# ==============================================================================
# EXAMPLE 8: Model Configuration and Customization
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 8: Model Config - Customizing Pydantic Behavior")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Customize how Pydantic handles your models:
- Allow extra fields or forbid them
- Make fields immutable
- Validate on assignment
- Custom JSON encoders

LOGIC:
- Inner Config class controls model behavior
- Various options for different use cases
""")

class StrictAPIRequest(BaseModel):
    """API request with strict validation"""
    endpoint: str
    method: str
    params: Dict[str, Any]

    class Config:
        # Forbid extra fields
        extra = 'forbid'

        # Validate when fields are assigned (not just on creation)
        validate_assignment = True

        # Custom JSON encoding
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class FlexibleConfig(BaseModel):
    """Config that allows extra fields"""
    required_field: str

    class Config:
        # Allow extra fields
        extra = 'allow'

class ImmutableModel(BaseModel):
    """Model that cannot be modified after creation"""
    data: str
    value: int

    class Config:
        # Make immutable
        allow_mutation = False

print("\n▶ Testing strict validation (extra='forbid'):")

# Valid request
strict_req = StrictAPIRequest(
    endpoint="/api/tools",
    method="POST",
    params={"tool": "read_file"}
)
print(f"  ✓ Valid request created")

# Invalid request (extra field!)
print("\n  Testing with extra field:")
try:
    bad_req = StrictAPIRequest(
        endpoint="/api/tools",
        method="POST",
        params={},
        extra_field="not allowed"  # ❌ Extra field!
    )
except ValidationError as e:
    print(f"  ❌ Caught: {e.errors()[0]['msg']}")

# Test flexible config
print("\n▶ Testing flexible config (extra='allow'):")
flexible = FlexibleConfig(
    required_field="value",
    extra_1="allowed",
    extra_2="also allowed",
    whatever="fine"
)

print(f"  ✓ Extra fields allowed: {flexible.__dict__}")

# Test immutable model
print("\n▶ Testing immutable model:")
immutable = ImmutableModel(data="test", value=42)
print(f"  Created: {immutable.data}")

try:
    immutable.data = "modified"  # ❌ Not allowed!
except ValidationError as e:
    print(f"  ❌ Cannot modify: {e.errors()[0]['msg']}")

# Test validate_assignment
print("\n▶ Testing validate_assignment:")
try:
    strict_req.method = "INVALID_METHOD"  # Validated!
    strict_req.endpoint = ""  # Validated!
except ValidationError as e:
    print(f"  ❌ Assignment validation caught error")

print("\n💡 KEY TAKEAWAY:")
print("   Config class customizes Pydantic behavior")
print("   extra='forbid' for strict APIs")
print("   validate_assignment=True for runtime safety")

# ==============================================================================
# EXAMPLE 9: Validators with Dependencies
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 9: Dependent Validators - Cross-Field Validation")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Some validation rules depend on multiple fields:
- End date must be after start date
- Max value must be greater than min value
- Conditional requirements

LOGIC:
- @validator can access other field values via 'values' parameter
- @root_validator sees ALL fields
- Enforce complex business rules
""")

class DateRangeFilter(BaseModel):
    """Date range filter with dependent validation"""
    start_date: datetime
    end_date: datetime
    include_weekends: bool = True
    max_days: int = 365

    @validator('end_date')
    def validate_end_after_start(cls, v, values):
        """Ensure end_date is after start_date"""
        start = values.get('start_date')

        if start and v <= start:
            raise ValueError(
                f"end_date ({v}) must be after start_date ({start})"
            )

        return v

    @root_validator
    def validate_date_range(cls, values):
        """Validate entire date range"""
        start = values.get('start_date')
        end = values.get('end_date')
        max_days = values.get('max_days')

        if start and end:
            duration = (end - start).days

            if duration > max_days:
                raise ValueError(
                    f"Date range ({duration} days) exceeds maximum ({max_days} days)"
                )

            # Add computed field
            values['duration_days'] = duration

        return values

class PriceRange(BaseModel):
    """Price range with validation"""
    min_price: float = Field(..., ge=0)
    max_price: float = Field(..., ge=0)
    currency: str = "USD"

    @validator('max_price')
    def validate_max_greater_than_min(cls, v, values):
        """Ensure max > min"""
        min_price = values.get('min_price')

        if min_price and v < min_price:
            raise ValueError(
                f"max_price ({v}) must be >= min_price ({min_price})"
            )

        return v

class ConditionalRequired(BaseModel):
    """Model with conditional requirements"""
    has_shipping: bool
    shipping_address: Optional[str] = None

    @root_validator
    def validate_shipping(cls, values):
        """If has_shipping=True, shipping_address is required"""
        has_shipping = values.get('has_shipping')
        address = values.get('shipping_address')

        if has_shipping and not address:
            raise ValueError(
                "shipping_address is required when has_shipping=True"
            )

        return values

print("\n▶ Testing date range validation:")

try:
    date_range = DateRangeFilter(
        start_date=datetime(2024, 1, 1),
        end_date=datetime(2024, 12, 31),
        max_days=400
    )

    print(f"  ✓ Valid range: {date_range.duration_days} days")

except ValidationError as e:
    print(f"  ❌ Error: {e}")

# Test invalid range (end before start)
print("\n  Testing invalid range:")
try:
    bad_range = DateRangeFilter(
        start_date=datetime(2024, 12, 31),
        end_date=datetime(2024, 1, 1),  # ❌ Before start!
        max_days=365
    )
except ValidationError as e:
    print(f"  ❌ Caught: {e.errors()[0]['msg']}")

# Test price range
print("\n▶ Testing price range:")
price_range = PriceRange(min_price=10.0, max_price=100.0)
print(f"  ✓ Price range: ${price_range.min_price} - ${price_range.max_price}")

# Test conditional requirement
print("\n▶ Testing conditional requirement:")
try:
    order = ConditionalRequired(
        has_shipping=True,
        shipping_address=None  # ❌ Required when has_shipping=True!
    )
except ValidationError as e:
    print(f"  ❌ Caught: {e.errors()[0]['msg']}")

print("\n💡 KEY TAKEAWAY:")
print("   @validator(field) for dependent validation")
print("   @root_validator for cross-field validation")
print("   Access other field values via 'values' parameter")

# ==============================================================================
# EXAMPLE 10: Integration with FastAPI/MCP Servers
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Real Integration - Building an MCP Tool Registry")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build a complete MCP tool registry system using Pydantic for validation.
This shows how everything comes together in a real application.

LOGIC:
- Use Pydantic for all data structures
- Automatic validation at every level
- Type-safe operations
- Easy serialization for API responses
""")

class ToolStatus(str, Enum):
    """Tool status enumeration"""
    ACTIVE = "active"
    DISABLED = "disabled"
    DEPRECATED = "deprecated"

class ToolParameter(BaseModel):
    """Tool parameter definition"""
    name: str
    type: str
    description: str
    required: bool = True
    default: Optional[Any] = None

class ToolRegistryEntry(BaseModel):
    """Complete tool registry entry"""
    tool_id: str = Field(..., regex="^tool-[0-9]+$")
    name: str = Field(..., regex="^[a-z][a-z0-9_]*$")
    description: str = Field(..., min_length=10)
    category: str
    parameters: List[ToolParameter]
    status: ToolStatus = ToolStatus.ACTIVE
    version: str = Field(..., regex=r"^\d+\.\d+\.\d+$")
    created_at: datetime
    updated_at: datetime

    @validator('updated_at')
    def validate_updated_after_created(cls, v, values):
        """Ensure updated_at >= created_at"""
        created = values.get('created_at')

        if created and v < created:
            raise ValueError("updated_at cannot be before created_at")

        return v

class ToolRegistry(BaseModel):
    """Complete tool registry"""
    registry_version: str
    tools: List[ToolRegistryEntry] = Field(default_factory=list)

    def add_tool(self, tool: ToolRegistryEntry):
        """Add tool to registry"""
        # Check for duplicates
        if any(t.tool_id == tool.tool_id for t in self.tools):
            raise ValueError(f"Tool {tool.tool_id} already exists")

        self.tools.append(tool)

    def get_tool(self, tool_id: str) -> Optional[ToolRegistryEntry]:
        """Get tool by ID"""
        return next((t for t in self.tools if t.tool_id == tool_id), None)

    def list_by_category(self, category: str) -> List[ToolRegistryEntry]:
        """List tools in category"""
        return [t for t in self.tools if t.category == category]

    def list_active_tools(self) -> List[ToolRegistryEntry]:
        """List only active tools"""
        return [t for t in self.tools if t.status == ToolStatus.ACTIVE]

    def to_api_response(self) -> dict:
        """Convert to API response format"""
        return {
            "version": self.registry_version,
            "tool_count": len(self.tools),
            "active_count": len(self.list_active_tools()),
            "tools": [t.dict() for t in self.tools]
        }

print("\n▶ Building MCP Tool Registry:")

# Create registry
registry = ToolRegistry(registry_version="1.0.0")

# Add tools
tools_to_add = [
    ToolRegistryEntry(
        tool_id="tool-001",
        name="read_file",
        description="Read contents from a file on the filesystem",
        category="file_operations",
        parameters=[
            ToolParameter(name="path", type="string", description="File path", required=True),
            ToolParameter(name="encoding", type="string", description="File encoding",
                         required=False, default="utf-8")
        ],
        version="1.0.0",
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    ToolRegistryEntry(
        tool_id="tool-002",
        name="write_file",
        description="Write contents to a file on the filesystem",
        category="file_operations",
        parameters=[
            ToolParameter(name="path", type="string", description="File path", required=True),
            ToolParameter(name="content", type="string", description="Content to write", required=True)
        ],
        version="1.0.0",
        status=ToolStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    ),
    ToolRegistryEntry(
        tool_id="tool-003",
        name="web_search",
        description="Search the internet for information",
        category="web_operations",
        parameters=[
            ToolParameter(name="query", type="string", description="Search query", required=True)
        ],
        version="2.1.0",
        status=ToolStatus.ACTIVE,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
]

for tool in tools_to_add:
    registry.add_tool(tool)
    print(f"  ✓ Added: {tool.name} ({tool.tool_id})")

# Query registry
print(f"\n▶ Querying registry:")
print(f"  Total tools: {len(registry.tools)}")
print(f"  Active tools: {len(registry.list_active_tools())}")

file_tools = registry.list_by_category("file_operations")
print(f"  File operation tools: {[t.name for t in file_tools]}")

# Get API response
api_response = registry.to_api_response()
print(f"\n  📡 API Response:")
print(f"     Version: {api_response['version']}")
print(f"     Tool count: {api_response['tool_count']}")

# Serialize to JSON
registry_json = registry.json(indent=2)
print(f"\n  📄 Full registry as JSON (first 200 chars):")
print(f"     {registry_json[:200]}...")

print("\n💡 KEY TAKEAWAY:")
print("   Pydantic models combine perfectly for real applications")
print("   Complete validation + serialization + documentation")
print("   Production-ready for APIs and MCP servers!")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 ALL 10 PYDANTIC EXAMPLES COMPLETED!")
print("=" * 80)

summary = """
What You've Mastered:

1. ✅ Basic Validation - Automatic type validation
2. ✅ Custom Validators - Business logic validation
3. ✅ Type Conversion - Automatic type coercion
4. ✅ Nested Models - Complex hierarchical validation
5. ✅ Settings Management - Load from environment
6. ✅ API Schemas - Type-safe request/response
7. ✅ JSON Schema - Auto-generate documentation
8. ✅ Model Config - Customize behavior
9. ✅ Dependent Validators - Cross-field validation
10. ✅ Real Integration - Complete MCP tool registry

Key Pydantic Features:
────────────────────────────────────────────────
• Automatic validation on creation
• Type conversion (strings → correct types)
• Custom validators (@validator, @root_validator)
• Nested model validation
• JSON schema generation
• Settings from environment
• Immutability options
• FastAPI integration

Pydantic vs Dataclasses:
────────────────────────────────────────────────
Dataclasses:          Pydantic:
• Structure only      • Structure + Validation
• No parsing          • Auto type conversion
• Manual validation   • Automatic validation
• Faster              • More features
• Standard library    • External package

When to Use Pydantic:
────────────────────────────────────────────────
✓ API request/response validation
✓ Configuration management
✓ Data parsing from external sources
✓ When you need JSON schema
✓ FastAPI applications
✓ MCP server tool definitions
✓ Any time validation is critical

Common Decorators:
────────────────────────────────────────────────
• @validator('field') - Validate single field
• @root_validator - Validate entire model
• Field(...) - Add constraints and metadata
• model.dict() - Convert to dictionary
• model.json() - Convert to JSON
• model.schema() - Generate JSON schema

Next: Move to Generics examples! 🚀
"""

print(summary)

print("\n" + "=" * 80)
print("📝 PRACTICE SUGGESTIONS:")
print("=" * 80)
print("""
1. Build an API with Pydantic request/response models
2. Create a settings system loading from .env files
3. Validate complex nested data structures
4. Generate OpenAPI documentation from Pydantic models
5. Build an MCP tool validator using Pydantic

Ready for Generics? Run: 06_Generics_10_Examples.py
""")
