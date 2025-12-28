"""
METACLASSES - 10 REAL-LIFE CODING EXAMPLES
============================================

Source: https://github.com/panaversity/learn-modern-ai-python/tree/main/00_python_colab
Topic: Metaclasses - Class Factories for Advanced Python Programming

This file contains 10 comprehensive examples showing how to use metaclasses
to create powerful, self-configuring class systems for AI/MCP development.

WHAT ARE METACLASSES?
A metaclass is a "class of a class" - it defines how classes behave.
Just as a class creates instances, a metaclass creates classes.

Hierarchy: Metaclass → Creates → Class → Creates → Instance

EXAMPLES:
1. Auto-Registration System for MCP Tools
2. Singleton Pattern with Metaclass
3. Auto-Property Generation for Models
4. Validation Metaclass for API Schemas
5. ORM-Style Model Metaclass
6. Plugin Architecture with Auto-Discovery
7. Interface Enforcement Metaclass
8. Automatic Documentation Generator
9. Method Timing Decorator via Metaclass
10. Factory Pattern with Metaclass Registry
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any, Callable, Optional, Type
import inspect
import time
from dataclasses import dataclass
import json

print("=" * 80)
print("METACLASSES - 10 REAL-LIFE CODING EXAMPLES")
print("=" * 80)
print("Master class factories for advanced AI-native development!")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: Auto-Registration System for MCP Tools
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Auto-Registration System for MCP Tools")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
In an MCP server, you have dozens of tools (read_file, write_file, etc.).
Instead of manually registering each tool in a central registry, use a
metaclass to automatically register every tool class when it's defined!

LOGIC:
- Metaclass.__new__() is called when creating a class
- We intercept class creation and add the class to a registry
- Tools are automatically discovered without manual registration
""")

class ToolRegistryMeta(type):
    """Metaclass that auto-registers all MCP tools"""

    # Class-level registry (shared by all classes using this metaclass)
    _registry: Dict[str, Type] = {}
    _categories: Dict[str, List[str]] = {}

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """
        Called when creating a new class.

        Parameters:
        - mcs: The metaclass itself (like 'self' but for classes)
        - name: Name of the class being created
        - bases: Base classes (inheritance)
        - attrs: Dictionary of class attributes and methods
        """
        print(f"  🔧 Metaclass creating class: {name}")

        # Create the class using parent's __new__
        cls = super().__new__(mcs, name, bases, attrs)

        # Don't register abstract base classes
        if name == 'BaseTool' or inspect.isabstract(cls):
            print(f"     ↳ Skipping registration (base class)")
            return cls

        # Extract metadata from class attributes
        tool_name = attrs.get('tool_name', name.lower())
        category = attrs.get('category', 'general')
        description = attrs.get('description', 'No description')

        # Register the tool
        mcs._registry[tool_name] = cls

        # Add to category
        if category not in mcs._categories:
            mcs._categories[category] = []
        mcs._categories[category].append(tool_name)

        print(f"     ✓ Registered: {tool_name} (category: {category})")

        # Add metadata as class attribute
        cls._tool_metadata = {
            'name': tool_name,
            'category': category,
            'description': description
        }

        return cls

    @classmethod
    def get_tool(mcs, name: str) -> Optional[Type]:
        """Get a tool class by name"""
        return mcs._registry.get(name)

    @classmethod
    def list_all_tools(mcs) -> List[str]:
        """List all registered tool names"""
        return list(mcs._registry.keys())

    @classmethod
    def list_by_category(mcs, category: str) -> List[str]:
        """List tools in a specific category"""
        return mcs._categories.get(category, [])

    @classmethod
    def get_all_categories(mcs) -> List[str]:
        """Get all categories"""
        return list(mcs._categories.keys())

class BaseTool(metaclass=ToolRegistryMeta):
    """Base class for all MCP tools"""

    tool_name: str = ""
    category: str = "general"
    description: str = ""

    @abstractmethod
    def execute(self, **kwargs) -> Any:
        """Execute the tool with given parameters"""
        raise NotImplementedError

    @classmethod
    def get_metadata(cls) -> dict:
        """Get tool metadata"""
        return getattr(cls, '_tool_metadata', {})

# Now let's define some tools - they'll auto-register!
print("\n▶ Defining MCP Tools (automatic registration):")

class ReadFileTool(BaseTool):
    """Read contents from a file"""
    tool_name = "read_file"
    category = "file_operations"
    description = "Read and return file contents"

    def execute(self, path: str) -> str:
        return f"Contents of {path}"

class WriteFileTool(BaseTool):
    """Write contents to a file"""
    tool_name = "write_file"
    category = "file_operations"
    description = "Write data to a file"

    def execute(self, path: str, content: str) -> bool:
        return True

class ExecuteBashTool(BaseTool):
    """Execute a bash command"""
    tool_name = "execute_bash"
    category = "system"
    description = "Run bash commands"

    def execute(self, command: str) -> str:
        return f"Executed: {command}"

class WebSearchTool(BaseTool):
    """Search the web"""
    tool_name = "web_search"
    category = "web"
    description = "Search the internet"

    def execute(self, query: str) -> List[str]:
        return [f"Result for: {query}"]

class DatabaseQueryTool(BaseTool):
    """Query database"""
    tool_name = "db_query"
    category = "database"
    description = "Execute database queries"

    def execute(self, sql: str) -> List[dict]:
        return [{"result": "data"}]

# Now use the registry!
print("\n▶ Using the Tool Registry:")

print("\n  📚 All registered tools:")
for tool_name in ToolRegistryMeta.list_all_tools():
    tool_class = ToolRegistryMeta.get_tool(tool_name)
    metadata = tool_class.get_metadata()
    print(f"     • {tool_name}: {metadata['description']}")

print("\n  📁 Tools by category:")
for category in ToolRegistryMeta.get_all_categories():
    tools = ToolRegistryMeta.list_by_category(category)
    print(f"     {category}: {', '.join(tools)}")

print("\n  🎯 Dynamic tool usage:")
tool_name = "read_file"
tool_class = ToolRegistryMeta.get_tool(tool_name)
if tool_class:
    tool_instance = tool_class()
    result = tool_instance.execute(path="/data/test.txt")
    print(f"     {tool_name} result: {result}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass.__new__() intercepts class creation for auto-registration.")
print("   MCP servers use this pattern for automatic tool discovery!")
print("   No manual registry.add() needed - just define the class!")

# ==============================================================================
# EXAMPLE 2: Singleton Pattern with Metaclass
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Singleton Pattern - One Instance Per Class")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Some objects should only have ONE instance (database connections, config
managers, MCP client connections). Metaclass enforces singleton pattern.

LOGIC:
- Metaclass stores instances in a dictionary
- __call__() is invoked when you create an instance: MyClass()
- We override __call__() to return existing instance if it exists
""")

class SingletonMeta(type):
    """Metaclass that implements singleton pattern"""

    _instances: Dict[Type, Any] = {}

    def __call__(cls, *args, **kwargs):
        """
        Called when someone tries to create an instance: MyClass()

        This is AFTER the class is created, when creating an instance.
        """
        if cls not in cls._instances:
            print(f"  🔨 Creating new instance of {cls.__name__}")

            # Create the instance using parent's __call__
            instance = super().__call__(*args, **kwargs)

            # Store it
            cls._instances[cls] = instance
        else:
            print(f"  ♻️  Returning existing instance of {cls.__name__}")

        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    """Database connection (should be singleton)"""

    def __init__(self, host: str = "localhost", port: int = 5432):
        print(f"     → Initializing connection to {host}:{port}")
        self.host = host
        self.port = port
        self.connection_id = id(self)

    def query(self, sql: str):
        return f"Query result from connection-{self.connection_id}"

class MCPClientConnection(metaclass=SingletonMeta):
    """MCP client connection (should be singleton)"""

    def __init__(self, server_url: str = "localhost:8080"):
        print(f"     → Connecting to MCP server: {server_url}")
        self.server_url = server_url
        self.session_id = f"session-{id(self)}"

    def call_tool(self, tool_name: str):
        return f"Tool result from {self.session_id}"

print("\n▶ Testing Singleton Pattern:")

# First access - creates instance
print("\n  1st access:")
db1 = DatabaseConnection("localhost", 5432)
print(f"     Instance ID: {id(db1)}")

# Second access - returns same instance!
print("\n  2nd access:")
db2 = DatabaseConnection("different_host", 9999)  # Args ignored!
print(f"     Instance ID: {id(db2)}")

print(f"\n  Are they the same object? {db1 is db2}")
print(f"  db1.host: {db1.host}")
print(f"  db2.host: {db2.host}")  # Same as db1!

# Test with MCP client
print("\n  Testing MCP Client Singleton:")
client1 = MCPClientConnection("server1.com")
client2 = MCPClientConnection("server2.com")  # Same instance!

print(f"  Same client? {client1 is client2}")
print(f"  Session ID: {client1.session_id}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass.__call__() controls instance creation.")
print("   Singleton ensures only one instance exists (shared state).")
print("   Use for: Database pools, config managers, MCP connections!")

# ==============================================================================
# EXAMPLE 3: Auto-Property Generation for Models
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Auto-Property Generation - Getters and Setters")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You want all model attributes to have getters/setters automatically,
with validation. Instead of writing @property for each field, use
a metaclass to generate them automatically!

LOGIC:
- Metaclass scans class attributes for type annotations
- For each typed attribute, generates getter/setter properties
- Adds validation logic automatically
""")

class AutoPropertyMeta(type):
    """Metaclass that auto-generates properties with validation"""

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Generate properties for all type-annotated attributes"""

        # Get type annotations
        annotations = attrs.get('__annotations__', {})

        print(f"  🔧 Creating {name} with auto-properties for: {list(annotations.keys())}")

        # Storage for actual values (private attributes)
        for attr_name, attr_type in annotations.items():
            private_name = f'_{attr_name}'

            # Create getter
            def make_getter(attr):
                def getter(self):
                    return getattr(self, f'_{attr}', None)
                return getter

            # Create setter with type checking
            def make_setter(attr, expected_type):
                def setter(self, value):
                    # Type validation
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{attr} must be {expected_type.__name__}, "
                            f"got {type(value).__name__}"
                        )
                    setattr(self, f'_{attr}', value)
                return setter

            # Add property to class
            attrs[attr_name] = property(
                make_getter(attr_name),
                make_setter(attr_name, attr_type)
            )

            print(f"     ✓ Generated property: {attr_name} ({attr_type.__name__})")

        return super().__new__(mcs, name, bases, attrs)

class MCPToolSchema(metaclass=AutoPropertyMeta):
    """MCP Tool Schema with auto-generated properties"""

    # Type annotations trigger property generation
    name: str
    description: str
    timeout: float
    retry_count: int

    def __init__(self, name: str, description: str,
                 timeout: float = 30.0, retry_count: int = 3):
        # Set via properties (will be validated!)
        self.name = name
        self.description = description
        self.timeout = timeout
        self.retry_count = retry_count

class UserModel(metaclass=AutoPropertyMeta):
    """User model with auto-validated properties"""

    username: str
    age: int
    email: str

    def __init__(self, username: str, age: int, email: str):
        self.username = username
        self.age = age
        self.email = email

print("\n▶ Testing Auto-Generated Properties:")

# Valid usage
print("\n  Creating valid tool schema:")
tool = MCPToolSchema("read_file", "Read a file", timeout=10.0, retry_count=5)
print(f"     Tool name: {tool.name}")
print(f"     Timeout: {tool.timeout}")

# Modification works
print("\n  Modifying properties:")
tool.timeout = 20.0
print(f"     New timeout: {tool.timeout}")

# Type validation works!
print("\n  Testing type validation:")
try:
    tool.timeout = "invalid"  # Should fail!
except TypeError as e:
    print(f"     ✓ Validation caught error: {e}")

# Test with user model
print("\n  Testing UserModel:")
user = UserModel("alice", 25, "alice@example.com")
print(f"     User: {user.username}, age {user.age}")

try:
    user.age = "twenty"  # Should fail!
except TypeError as e:
    print(f"     ✓ Validation caught error: {e}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass can generate methods/properties automatically.")
print("   Reduces boilerplate and ensures consistent validation.")
print("   Used in ORMs like SQLAlchemy and validation libraries!")

# ==============================================================================
# EXAMPLE 4: Validation Metaclass for API Schemas
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: API Schema Validation at Class Definition Time")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You're defining API schemas for MCP requests/responses. You want to
validate that schemas are correctly defined AT CLASS DEFINITION TIME,
not at runtime. Catch errors early!

LOGIC:
- Metaclass validates class definition during class creation
- Checks required methods exist
- Validates attribute types and constraints
- Fails fast if schema is invalid
""")

class APISchemaValidationMeta(type):
    """Metaclass that validates API schemas at definition time"""

    REQUIRED_METHODS = ['to_dict', 'validate']
    REQUIRED_ATTRS = ['schema_version']

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Validate schema class at definition time"""

        # Skip validation for base classes
        if name == 'BaseAPISchema':
            return super().__new__(mcs, name, bases, attrs)

        print(f"  🔍 Validating API schema: {name}")

        # Check required methods
        for method_name in mcs.REQUIRED_METHODS:
            if method_name not in attrs:
                raise TypeError(
                    f"API Schema '{name}' must implement '{method_name}' method"
                )
            print(f"     ✓ Has required method: {method_name}")

        # Check required attributes
        for attr_name in mcs.REQUIRED_ATTRS:
            if attr_name not in attrs:
                raise TypeError(
                    f"API Schema '{name}' must define '{attr_name}' attribute"
                )
            print(f"     ✓ Has required attribute: {attr_name}")

        # Validate field types if specified
        if 'fields' in attrs:
            mcs._validate_fields(name, attrs['fields'])

        print(f"     ✅ Schema {name} is valid!")

        return super().__new__(mcs, name, bases, attrs)

    @staticmethod
    def _validate_fields(schema_name: str, fields: dict):
        """Validate field definitions"""
        for field_name, field_def in fields.items():
            if not isinstance(field_def, dict):
                raise TypeError(
                    f"Field '{field_name}' in {schema_name} must be a dict"
                )

            if 'type' not in field_def:
                raise TypeError(
                    f"Field '{field_name}' in {schema_name} must specify 'type'"
                )

class BaseAPISchema(metaclass=APISchemaValidationMeta):
    """Base class for API schemas"""
    pass

# Valid schema
print("\n▶ Defining VALID API Schema:")

class MCPRequestSchema(BaseAPISchema):
    """Valid MCP request schema"""

    schema_version = "1.0"

    fields = {
        'method': {'type': str, 'required': True},
        'params': {'type': dict, 'required': False},
        'timeout': {'type': float, 'required': False}
    }

    def to_dict(self) -> dict:
        return {'schema': 'MCPRequest'}

    def validate(self, data: dict) -> bool:
        return True

print("  ✓ Schema created successfully!")

# Invalid schema (missing method)
print("\n▶ Attempting to define INVALID schema (missing 'validate' method):")

try:
    class InvalidSchema(BaseAPISchema):
        schema_version = "1.0"
        fields = {}

        def to_dict(self) -> dict:
            return {}

        # Missing validate() method!

except TypeError as e:
    print(f"  ❌ Caught error at class definition: {e}")

# Invalid schema (missing attribute)
print("\n▶ Attempting to define INVALID schema (missing 'schema_version'):")

try:
    class InvalidSchema2(BaseAPISchema):
        # Missing schema_version!

        fields = {}

        def to_dict(self) -> dict:
            return {}

        def validate(self, data: dict) -> bool:
            return True

except TypeError as e:
    print(f"  ❌ Caught error at class definition: {e}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass can validate class definitions IMMEDIATELY.")
print("   Catch errors at import time, not runtime!")
print("   Enforces contracts and prevents bugs early.")

# ==============================================================================
# EXAMPLE 5: ORM-Style Model Metaclass
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: ORM-Style Model - Like Django or SQLAlchemy")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build a simple ORM where model classes automatically map to database
tables. Metaclass handles field discovery, table naming, and query
generation.

LOGIC:
- Metaclass collects field definitions
- Auto-generates table name from class name
- Creates methods for common queries (save, find, etc.)
""")

class Field:
    """Represents a database field"""

    def __init__(self, field_type: type, required: bool = True,
                 default: Any = None):
        self.field_type = field_type
        self.required = required
        self.default = default

    def __repr__(self):
        return f"Field({self.field_type.__name__})"

class ORMModelMeta(type):
    """Metaclass for ORM models"""

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Create ORM model with database mapping"""

        # Skip base class
        if name == 'Model':
            return super().__new__(mcs, name, bases, attrs)

        print(f"  🗄️  Creating ORM model: {name}")

        # Collect field definitions
        fields = {}
        for attr_name, attr_value in list(attrs.items()):
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
                # Remove field definition, replace with None
                attrs[attr_name] = None
                print(f"     ✓ Field discovered: {attr_name} ({attr_value.field_type.__name__})")

        # Store field metadata
        attrs['_fields'] = fields

        # Auto-generate table name (snake_case from class name)
        table_name = mcs._to_snake_case(name)
        attrs['_table_name'] = table_name
        print(f"     ✓ Table name: {table_name}")

        # Create the class
        cls = super().__new__(mcs, name, bases, attrs)

        # Add ORM methods
        cls.save = mcs._make_save_method()
        cls.to_dict = mcs._make_to_dict_method()

        return cls

    @staticmethod
    def _to_snake_case(name: str) -> str:
        """Convert CamelCase to snake_case"""
        import re
        name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()

    @staticmethod
    def _make_save_method():
        """Generate save method"""
        def save(self):
            table = self._table_name
            data = self.to_dict()
            return f"INSERT INTO {table} VALUES {data}"
        return save

    @staticmethod
    def _make_to_dict_method():
        """Generate to_dict method"""
        def to_dict(self):
            return {
                field_name: getattr(self, field_name)
                for field_name in self._fields
            }
        return to_dict

class Model(metaclass=ORMModelMeta):
    """Base model class"""

    def __init__(self, **kwargs):
        for field_name in self._fields:
            value = kwargs.get(field_name)
            setattr(self, field_name, value)

# Define models
print("\n▶ Defining ORM Models:")

class User(Model):
    """User model"""
    username = Field(str, required=True)
    email = Field(str, required=True)
    age = Field(int, required=False, default=0)

class MCPTool(Model):
    """MCP Tool model"""
    tool_name = Field(str, required=True)
    category = Field(str, required=True)
    enabled = Field(bool, required=False, default=True)

# Use models
print("\n▶ Using ORM Models:")

user = User(username="alice", email="alice@example.com", age=25)
print(f"\n  User instance:")
print(f"     username: {user.username}")
print(f"     Table: {user._table_name}")
print(f"     Dict: {user.to_dict()}")
print(f"     SQL: {user.save()}")

tool = MCPTool(tool_name="read_file", category="file_ops", enabled=True)
print(f"\n  Tool instance:")
print(f"     tool_name: {tool.tool_name}")
print(f"     Table: {tool._table_name}")
print(f"     Dict: {tool.to_dict()}")
print(f"     SQL: {tool.save()}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass can inspect class definitions and generate code.")
print("   ORMs like Django and SQLAlchemy use this extensively!")
print("   Automatic table mapping, query generation, and more.")

# ==============================================================================
# EXAMPLE 6: Plugin Architecture with Auto-Discovery
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Plugin System - Auto-Discovery and Loading")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build an extensible plugin system where plugins are automatically
discovered and loaded. Users can add new plugins by just creating
a class - no manual registration needed!

LOGIC:
- Metaclass maintains a plugin registry
- Plugins are categorized by type
- Auto-generates plugin interface validation
""")

class PluginMeta(type):
    """Metaclass for plugin system"""

    _plugins: Dict[str, Dict[str, Type]] = {}  # {plugin_type: {name: class}}

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Register plugin automatically"""

        cls = super().__new__(mcs, name, bases, attrs)

        # Skip base classes
        if name in ['Plugin', 'BasePlugin']:
            return cls

        # Get plugin metadata
        plugin_type = attrs.get('plugin_type', 'unknown')
        plugin_name = attrs.get('plugin_name', name.lower())

        print(f"  🔌 Discovered plugin: {plugin_name} (type: {plugin_type})")

        # Validate required methods
        required_methods = ['initialize', 'execute']
        for method in required_methods:
            if method not in attrs:
                print(f"     ⚠️  Warning: Plugin {name} missing '{method}' method")

        # Register plugin
        if plugin_type not in mcs._plugins:
            mcs._plugins[plugin_type] = {}

        mcs._plugins[plugin_type][plugin_name] = cls

        print(f"     ✓ Registered: {plugin_name} → {plugin_type}")

        return cls

    @classmethod
    def get_plugins_by_type(mcs, plugin_type: str) -> Dict[str, Type]:
        """Get all plugins of a specific type"""
        return mcs._plugins.get(plugin_type, {})

    @classmethod
    def get_all_plugin_types(mcs) -> List[str]:
        """Get all plugin types"""
        return list(mcs._plugins.keys())

    @classmethod
    def load_plugin(mcs, plugin_type: str, plugin_name: str):
        """Load and instantiate a plugin"""
        plugins = mcs._plugins.get(plugin_type, {})
        plugin_class = plugins.get(plugin_name)

        if plugin_class:
            return plugin_class()
        return None

class Plugin(metaclass=PluginMeta):
    """Base plugin class"""

    plugin_type = "base"
    plugin_name = "base"

    def initialize(self):
        pass

    def execute(self, *args, **kwargs):
        pass

# Define various plugins
print("\n▶ Defining Plugins (auto-discovery):")

class FileReaderPlugin(Plugin):
    """Plugin for reading files"""
    plugin_type = "io"
    plugin_name = "file_reader"

    def initialize(self):
        print("     FileReader initialized")

    def execute(self, path: str):
        return f"Reading: {path}"

class WebScraperPlugin(Plugin):
    """Plugin for web scraping"""
    plugin_type = "web"
    plugin_name = "web_scraper"

    def initialize(self):
        print("     WebScraper initialized")

    def execute(self, url: str):
        return f"Scraping: {url}"

class ImageProcessorPlugin(Plugin):
    """Plugin for image processing"""
    plugin_type = "media"
    plugin_name = "image_processor"

    def initialize(self):
        print("     ImageProcessor initialized")

    def execute(self, image_path: str):
        return f"Processing: {image_path}"

class DataTransformerPlugin(Plugin):
    """Plugin for data transformation"""
    plugin_type = "io"
    plugin_name = "data_transformer"

    def initialize(self):
        print("     DataTransformer initialized")

    def execute(self, data: dict):
        return f"Transforming: {data}"

# Use plugin system
print("\n▶ Using Plugin System:")

print("\n  📋 All plugin types:")
for plugin_type in PluginMeta.get_all_plugin_types():
    print(f"     • {plugin_type}")

print("\n  📦 Plugins by type:")
for plugin_type in PluginMeta.get_all_plugin_types():
    plugins = PluginMeta.get_plugins_by_type(plugin_type)
    print(f"     {plugin_type}:")
    for name in plugins.keys():
        print(f"       - {name}")

print("\n  🚀 Loading and using plugins:")
plugin = PluginMeta.load_plugin("io", "file_reader")
if plugin:
    plugin.initialize()
    result = plugin.execute("/data/file.txt")
    print(f"     Result: {result}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass enables powerful plugin architectures.")
print("   Plugins are auto-discovered - just define the class!")
print("   Used in: Web frameworks, IDEs, MCP servers with extensions.")

# ==============================================================================
# EXAMPLE 7: Interface Enforcement Metaclass
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 7: Interface Enforcement - Compile-Time Contract Checking")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Enforce that all implementing classes follow a specific interface/contract.
Unlike ABC (abstract base class), this happens at class definition time
with clearer error messages.

LOGIC:
- Metaclass checks that required methods are implemented
- Validates method signatures match the interface
- Fails immediately if contract is violated
""")

class InterfaceEnforcementMeta(type):
    """Metaclass that enforces interface contracts"""

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Enforce interface contracts"""

        # Skip interface definitions themselves
        if attrs.get('_is_interface', False):
            return super().__new__(mcs, name, bases, attrs)

        # Check if this class implements an interface
        for base in bases:
            if hasattr(base, '_is_interface') and base._is_interface:
                mcs._enforce_interface(name, base, attrs)

        return super().__new__(mcs, name, bases, attrs)

    @staticmethod
    def _enforce_interface(impl_name: str, interface: Type, attrs: dict):
        """Enforce that implementation follows interface"""

        print(f"  🔍 Checking {impl_name} implements {interface.__name__}")

        required_methods = getattr(interface, '_required_methods', {})

        for method_name, method_spec in required_methods.items():
            # Check method exists
            if method_name not in attrs:
                raise TypeError(
                    f"Class '{impl_name}' must implement method '{method_name}' "
                    f"from interface '{interface.__name__}'"
                )

            method = attrs[method_name]

            # Check it's callable
            if not callable(method):
                raise TypeError(
                    f"'{method_name}' in '{impl_name}' must be a callable method"
                )

            # Check signature (simplified - real impl would be more robust)
            sig = inspect.signature(method)
            expected_params = method_spec.get('params', [])

            actual_params = list(sig.parameters.keys())
            if 'self' in actual_params:
                actual_params.remove('self')

            if len(actual_params) < len(expected_params):
                raise TypeError(
                    f"Method '{method_name}' in '{impl_name}' must accept "
                    f"parameters: {expected_params}, got: {actual_params}"
                )

            print(f"     ✓ Method '{method_name}' correctly implemented")

def interface(cls):
    """Decorator to mark a class as an interface"""
    cls._is_interface = True

    # Collect required methods
    required_methods = {}
    for name, value in inspect.getmembers(cls):
        if callable(value) and not name.startswith('_'):
            sig = inspect.signature(value)
            params = [p for p in sig.parameters.keys() if p != 'self']
            required_methods[name] = {'params': params}

    cls._required_methods = required_methods

    return cls

# Define interface
@interface
class MCPToolInterface(metaclass=InterfaceEnforcementMeta):
    """Interface for MCP tools"""

    def get_name(self) -> str:
        """Get tool name"""
        pass

    def get_description(self) -> str:
        """Get tool description"""
        pass

    def execute(self, params: dict) -> Any:
        """Execute the tool"""
        pass

# Valid implementation
print("\n▶ Creating VALID implementation:")

class ValidTool(MCPToolInterface):
    """Valid tool implementation"""

    def get_name(self) -> str:
        return "valid_tool"

    def get_description(self) -> str:
        return "A valid tool"

    def execute(self, params: dict) -> Any:
        return "executed"

print("  ✓ Implementation accepted!")

# Invalid implementation (missing method)
print("\n▶ Attempting INVALID implementation (missing 'execute'):")

try:
    class InvalidTool(MCPToolInterface):
        def get_name(self) -> str:
            return "invalid"

        def get_description(self) -> str:
            return "Missing execute method!"

        # Missing execute()!

except TypeError as e:
    print(f"  ❌ Caught error: {e}")

print("\n💡 KEY TAKEAWAY:")
print("   Enforce contracts at class definition time!")
print("   Better error messages than ABC.")
print("   Ensures all implementations follow the interface.")

# ==============================================================================
# EXAMPLE 8: Automatic Documentation Generator
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 8: Auto-Documentation - Generate Docs from Code")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Automatically generate API documentation from class definitions.
Metaclass extracts docstrings, type hints, and method signatures
to build documentation.

LOGIC:
- Metaclass inspects methods and their signatures
- Extracts docstrings and type annotations
- Generates structured documentation
""")

class DocumentedMeta(type):
    """Metaclass that auto-generates documentation"""

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Generate documentation for the class"""

        cls = super().__new__(mcs, name, bases, attrs)

        # Skip base classes
        if name == 'Documented':
            return cls

        print(f"  📝 Generating documentation for: {name}")

        # Collect documentation
        docs = {
            'class_name': name,
            'description': inspect.getdoc(cls) or "No description",
            'methods': []
        }

        # Document each method
        for method_name, method in inspect.getmembers(cls, inspect.isfunction):
            if method_name.startswith('_'):
                continue  # Skip private methods

            sig = inspect.signature(method)
            method_doc = {
                'name': method_name,
                'signature': str(sig),
                'docstring': inspect.getdoc(method) or "No documentation",
                'parameters': {}
            }

            # Document parameters
            for param_name, param in sig.parameters.items():
                if param_name == 'self':
                    continue

                method_doc['parameters'][param_name] = {
                    'annotation': str(param.annotation) if param.annotation != inspect.Parameter.empty else 'Any',
                    'default': str(param.default) if param.default != inspect.Parameter.empty else 'required'
                }

            docs['methods'].append(method_doc)

        # Store documentation
        cls._documentation = docs

        # Print documentation
        mcs._print_documentation(docs)

        return cls

    @staticmethod
    def _print_documentation(docs: dict):
        """Pretty print documentation"""
        print(f"\n     📖 Documentation for {docs['class_name']}")
        print(f"     {'-' * 50}")
        print(f"     Description: {docs['description']}")

        for method in docs['methods']:
            print(f"\n     Method: {method['name']}{method['signature']}")
            print(f"       {method['docstring']}")

            if method['parameters']:
                print(f"       Parameters:")
                for param_name, param_info in method['parameters'].items():
                    print(f"         • {param_name}: {param_info['annotation']} "
                          f"(default: {param_info['default']})")

class Documented(metaclass=DocumentedMeta):
    """Base class with auto-documentation"""
    pass

# Create documented class
print("\n▶ Creating documented MCP tool:")

class SearchTool(Documented):
    """
    A tool for searching the web.
    Supports multiple search engines and result filtering.
    """

    def search(self, query: str, limit: int = 10) -> List[str]:
        """
        Search the web for a query.

        Args:
            query: The search query string
            limit: Maximum number of results to return
        """
        return [f"Result {i}" for i in range(limit)]

    def filter_results(self, results: List[str], keyword: str) -> List[str]:
        """
        Filter search results by keyword.

        Args:
            results: List of search results
            keyword: Keyword to filter by
        """
        return [r for r in results if keyword in r]

print("\n  ✓ Documentation generated and stored in _documentation attribute")

# Access generated documentation
doc = SearchTool._documentation
print(f"\n  📋 Quick access to docs:")
print(f"     Class: {doc['class_name']}")
print(f"     Methods: {[m['name'] for m in doc['methods']]}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass can auto-generate API documentation!")
print("   Extract info from docstrings, signatures, annotations.")
print("   Use for: API docs, OpenAPI schemas, help systems.")

# ==============================================================================
# EXAMPLE 9: Method Timing Decorator via Metaclass
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 9: Auto-Performance Monitoring - Time All Methods")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You want to monitor performance of all methods in certain classes
without adding @timer decorator to each method manually. Metaclass
wraps all methods automatically!

LOGIC:
- Metaclass wraps each method with timing logic
- Tracks execution times
- Generates performance reports
""")

class TimedMethodsMeta(type):
    """Metaclass that adds timing to all methods"""

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Wrap all methods with timing"""

        # Skip base class
        if name == 'Timed':
            return super().__new__(mcs, name, bases, attrs)

        print(f"  ⏱️  Adding timing to: {name}")

        # Create timing storage
        attrs['_timings'] = {}

        # Wrap each method
        for attr_name, attr_value in list(attrs.items()):
            if callable(attr_value) and not attr_name.startswith('_'):
                # Wrap the method
                wrapped = mcs._wrap_with_timing(attr_name, attr_value)
                attrs[attr_name] = wrapped
                print(f"     ✓ Wrapped method: {attr_name}")

        # Add reporting method
        attrs['get_performance_report'] = mcs._make_report_method()

        return super().__new__(mcs, name, bases, attrs)

    @staticmethod
    def _wrap_with_timing(method_name: str, method: Callable):
        """Wrap a method with timing logic"""

        def timed_method(self, *args, **kwargs):
            start = time.time()

            # Execute original method
            result = method(self, *args, **kwargs)

            # Record timing
            duration = time.time() - start

            if method_name not in self._timings:
                self._timings[method_name] = []

            self._timings[method_name].append(duration)

            return result

        return timed_method

    @staticmethod
    def _make_report_method():
        """Generate performance report method"""

        def get_performance_report(self) -> dict:
            """Get performance statistics for all methods"""
            report = {}

            for method_name, timings in self._timings.items():
                if timings:
                    report[method_name] = {
                        'calls': len(timings),
                        'total_time': sum(timings),
                        'avg_time': sum(timings) / len(timings),
                        'min_time': min(timings),
                        'max_time': max(timings)
                    }

            return report

        return get_performance_report

class Timed(metaclass=TimedMethodsMeta):
    """Base class with automatic timing"""
    pass

# Create class with timed methods
print("\n▶ Creating class with auto-timing:")

class DataProcessor(Timed):
    """Data processor with performance monitoring"""

    def load_data(self, size: int):
        """Simulate loading data"""
        time.sleep(0.1 * size)
        return [i for i in range(size * 100)]

    def process_data(self, data: List[int]):
        """Simulate processing data"""
        time.sleep(0.05)
        return sum(data)

    def save_results(self, results: Any):
        """Simulate saving results"""
        time.sleep(0.03)
        return True

# Use the class
print("\n▶ Using timed class:")
processor = DataProcessor()

print("\n  Running operations...")
data = processor.load_data(2)
result = processor.process_data(data)
processor.save_results(result)

# Run again for multiple measurements
data = processor.load_data(1)
result = processor.process_data(data)

# Get performance report
print("\n  📊 Performance Report:")
report = processor.get_performance_report()

for method_name, stats in report.items():
    print(f"\n     {method_name}:")
    print(f"       Calls: {stats['calls']}")
    print(f"       Total time: {stats['total_time']:.3f}s")
    print(f"       Avg time: {stats['avg_time']:.3f}s")
    print(f"       Min time: {stats['min_time']:.3f}s")
    print(f"       Max time: {stats['max_time']:.3f}s")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass can add monitoring/debugging to all methods!")
print("   No manual decorator needed on each method.")
print("   Use for: Performance monitoring, logging, debugging.")

# ==============================================================================
# EXAMPLE 10: Factory Pattern with Metaclass Registry
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Factory Pattern - Smart Object Creation")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Implement a factory pattern where objects are created based on type
strings. Metaclass maintains a registry and provides a factory method
for creating instances.

LOGIC:
- Metaclass registers all classes with their type identifiers
- Provides factory method to create instances by type
- Handles configuration and initialization automatically
""")

class FactoryMeta(type):
    """Metaclass that implements factory pattern"""

    _registry: Dict[str, Type] = {}

    def __new__(mcs, name: str, bases: tuple, attrs: dict):
        """Register class for factory creation"""

        cls = super().__new__(mcs, name, bases, attrs)

        # Skip base class
        if name == 'Creatable':
            return cls

        # Get type identifier
        type_id = attrs.get('type_id', name.lower())

        # Register
        mcs._registry[type_id] = cls
        print(f"  🏭 Factory registered: {type_id} → {name}")

        return cls

    @classmethod
    def create(mcs, type_id: str, **kwargs) -> Any:
        """Factory method to create instances by type"""

        if type_id not in mcs._registry:
            available = ', '.join(mcs._registry.keys())
            raise ValueError(
                f"Unknown type '{type_id}'. Available: {available}"
            )

        cls = mcs._registry[type_id]
        instance = cls(**kwargs)

        print(f"  ✓ Created {cls.__name__} instance via factory")

        return instance

    @classmethod
    def list_available_types(mcs) -> List[str]:
        """List all registered types"""
        return list(mcs._registry.keys())

class Creatable(metaclass=FactoryMeta):
    """Base class for factory-creatable objects"""

    type_id = "base"

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

# Define creatable classes
print("\n▶ Registering factory types:")

class FileStorage(Creatable):
    """File-based storage"""
    type_id = "file"

    def __init__(self, path: str, **kwargs):
        super().__init__(**kwargs)
        self.path = path

    def save(self, data: Any):
        return f"Saved to {self.path}"

class DatabaseStorage(Creatable):
    """Database storage"""
    type_id = "database"

    def __init__(self, connection_string: str, **kwargs):
        super().__init__(**kwargs)
        self.connection_string = connection_string

    def save(self, data: Any):
        return f"Saved to {self.connection_string}"

class CloudStorage(Creatable):
    """Cloud storage"""
    type_id = "cloud"

    def __init__(self, bucket: str, region: str = "us-east-1", **kwargs):
        super().__init__(**kwargs)
        self.bucket = bucket
        self.region = region

    def save(self, data: Any):
        return f"Saved to {self.bucket} in {self.region}"

# Use factory
print("\n▶ Using factory pattern:")

print("\n  📋 Available types:")
for type_id in FactoryMeta.list_available_types():
    print(f"     • {type_id}")

print("\n  🏗️  Creating instances via factory:")

# Create different storage types
storage1 = FactoryMeta.create("file", path="/data/storage")
print(f"     {storage1.save('data')}")

storage2 = FactoryMeta.create("database", connection_string="postgresql://localhost")
print(f"     {storage2.save('data')}")

storage3 = FactoryMeta.create("cloud", bucket="my-bucket", region="eu-west-1")
print(f"     {storage3.save('data')}")

# Configuration-based creation
print("\n  ⚙️  Configuration-based creation:")
config = {
    'storage_type': 'cloud',
    'bucket': 'ai-models',
    'region': 'us-west-2'
}

storage_type = config.pop('storage_type')
storage = FactoryMeta.create(storage_type, **config)
print(f"     Created from config: {storage.__class__.__name__}")
print(f"     {storage.save('model_weights')}")

print("\n💡 KEY TAKEAWAY:")
print("   Metaclass enables elegant factory patterns!")
print("   Objects created by type string (great for configs, APIs).")
print("   Used in: Dependency injection, plugin systems, ORMs.")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 ALL 10 METACLASS EXAMPLES COMPLETED!")
print("=" * 80)

summary = """
What You've Mastered:

1. ✅ Auto-Registration - Tools automatically register themselves
2. ✅ Singleton Pattern - Enforce single instance per class
3. ✅ Auto-Properties - Generate getters/setters automatically
4. ✅ Schema Validation - Validate at class definition time
5. ✅ ORM Models - Database mapping like Django/SQLAlchemy
6. ✅ Plugin System - Auto-discover and load plugins
7. ✅ Interface Enforcement - Compile-time contract checking
8. ✅ Auto-Documentation - Generate docs from code
9. ✅ Performance Monitoring - Auto-time all methods
10. ✅ Factory Pattern - Create objects from type strings

Key Metaclass Methods:
────────────────────────────────────────────────
• __new__(mcs, name, bases, attrs)
  ↳ Called when CREATING a class
  ↳ Use for: Modify class definition, register classes

• __call__(cls, *args, **kwargs)
  ↳ Called when CREATING an instance: MyClass()
  ↳ Use for: Control instantiation (singleton, factory)

• __init__(cls, name, bases, attrs)
  ↳ Called after class is created
  ↳ Less common, usually use __new__

Real-World Uses:
────────────────────────────────────────────────
✓ ORMs (Django, SQLAlchemy) - Model → table mapping
✓ Validation libraries (Pydantic) - Auto-validation
✓ Testing frameworks (pytest) - Auto-discover tests
✓ Plugin systems - Auto-register plugins
✓ MCP servers - Auto-discover tools
✓ API frameworks - Auto-generate docs/schemas

When to Use Metaclasses:
────────────────────────────────────────────────
✓ When you need to modify CLASS behavior (not instance)
✓ When you want automatic registration/discovery
✓ When you need class-level validation
✓ When building frameworks or libraries
✗ For simple cases, use decorators or class methods instead

Next: Move to Dataclasses examples! 🚀
"""

print(summary)

print("\n" + "=" * 80)
print("📝 PRACTICE SUGGESTIONS:")
print("=" * 80)
print("""
1. Build your own ORM with metaclasses
2. Create a plugin system for a real project
3. Implement auto-documentation for your API
4. Build a validation framework with metaclasses
5. Combine metaclasses with decorators for powerful patterns

Ready for Dataclasses? Run: 04_Dataclasses_10_Examples.py
""")
