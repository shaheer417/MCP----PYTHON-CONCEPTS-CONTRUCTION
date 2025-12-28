"""
OBJECT-ORIENTED PROGRAMMING (OOP) - ADVANCED LEVEL
===================================================

Expert-level OOP concepts for MCP mastery - Part 3

Topics Covered:
1. Metaclasses
2. Class Decorators
3. Advanced Descriptors
4. Context Managers (Advanced)
5. Slots for Memory Optimization
6. Weakref and Memory Management
7. Custom Exceptions
8. Generic Classes
9. Protocol Composition
10. Dependency Injection

These advanced concepts are critical for building production MCP servers!
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, TypeVar, Protocol, cast
from dataclasses import dataclass, field
from functools import wraps
from weakref import WeakValueDictionary
import time
from contextlib import contextmanager

# ============================================================================
# EXAMPLE 1: Metaclasses Basics
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 1: Introduction to Metaclasses")
print("="*70)

class SingletonMeta(type):
    """Metaclass that creates Singleton classes"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        print(f"Creating connection to: {connection_string}")

# Test singleton behavior
db1 = DatabaseConnection("postgresql://localhost")
db2 = DatabaseConnection("mysql://localhost")  # Won't create new instance
print(f"db1 is db2: {db1 is db2}")  # True
print(f"Connection string: {db1.connection_string}")


# ============================================================================
# EXAMPLE 2: Metaclass for Automatic Registration
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 2: Auto-Registration Metaclass")
print("="*70)

class PluginRegistry(type):
    """Metaclass that automatically registers plugins"""
    plugins = {}

    def __new__(mcs, name, bases, attrs):
        cls = super().__new__(mcs, name, bases, attrs)
        if name != 'Plugin':  # Don't register base class
            mcs.plugins[name] = cls
        return cls

class Plugin(metaclass=PluginRegistry):
    """Base plugin class"""
    pass

class EmailPlugin(Plugin):
    def send(self, message):
        return f"Email: {message}"

class SMSPlugin(Plugin):
    def send(self, message):
        return f"SMS: {message}"

class PushPlugin(Plugin):
    def send(self, message):
        return f"Push: {message}"

print("Registered plugins:")
for name, plugin_class in PluginRegistry.plugins.items():
    print(f"  - {name}: {plugin_class}")

# Dynamic plugin instantiation
for name, plugin_class in PluginRegistry.plugins.items():
    plugin = plugin_class()
    print(plugin.send(f"Hello from {name}"))


# ============================================================================
# EXAMPLE 3: Metaclass for Validation
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 3: Validation Metaclass")
print("="*70)

class ValidatedMeta(type):
    """Metaclass that ensures required methods are implemented"""
    def __new__(mcs, name, bases, attrs):
        if 'required_methods' in attrs:
            required = attrs['required_methods']
            for method in required:
                if method not in attrs:
                    raise TypeError(f"{name} must implement {method}()")
        return super().__new__(mcs, name, bases, attrs)

class APIEndpoint(metaclass=ValidatedMeta):
    required_methods = ['get', 'post']

    def get(self):
        return "GET method"

    def post(self):
        return "POST method"

try:
    class BadEndpoint(metaclass=ValidatedMeta):
        required_methods = ['get', 'post']
        def get(self):  # Missing post()
            return "GET"
except TypeError as e:
    print(f"Error creating BadEndpoint: {e}")


# ============================================================================
# EXAMPLE 4: Class Decorators
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 4: Class Decorators")
print("="*70)

def add_logging(cls):
    """Decorator that adds logging to all methods"""
    for name, method in cls.__dict__.items():
        if callable(method):
            setattr(cls, name, logged_method(method))
    return cls

def logged_method(method):
    @wraps(method)
    def wrapper(*args, **kwargs):
        print(f"Calling {method.__name__}")
        result = method(*args, **kwargs)
        print(f"Finished {method.__name__}")
        return result
    return wrapper

@add_logging
class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

calc = Calculator()
result = calc.add(5, 3)
print(f"Result: {result}")


# ============================================================================
# EXAMPLE 5: Advanced Descriptors with Type Checking
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 5: Type-Checking Descriptor")
print("="*70)

class TypedDescriptor:
    """Descriptor with type checking"""
    def __init__(self, name, expected_type):
        self.name = name
        self.expected_type = expected_type

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name)

    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"{self.name} must be {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        obj.__dict__[self.name] = value

class Person:
    name = TypedDescriptor("name", str)
    age = TypedDescriptor("age", int)
    email = TypedDescriptor("email", str)

    def __init__(self, name, age, email):
        self.name = name
        self.age = age
        self.email = email

person = Person("John", 30, "john@example.com")
print(f"Person: {person.name}, {person.age}, {person.email}")

try:
    person.age = "thirty"  # Will raise TypeError
except TypeError as e:
    print(f"Error: {e}")


# ============================================================================
# EXAMPLE 6: Cached Property Descriptor
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 6: Cached Property")
print("="*70)

class CachedProperty:
    """Descriptor that caches computed values"""
    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Cache the value in instance dict
        if self.name not in obj.__dict__:
            obj.__dict__[self.name] = self.func(obj)
        return obj.__dict__[self.name]

class DataProcessor:
    def __init__(self, data):
        self.data = data

    @CachedProperty
    def expensive_computation(self):
        print("Computing... (this should only print once)")
        time.sleep(0.1)  # Simulate expensive operation
        return sum(self.data)

processor = DataProcessor([1, 2, 3, 4, 5])
print(f"First call: {processor.expensive_computation}")
print(f"Second call: {processor.expensive_computation}")  # Uses cached value
print(f"Third call: {processor.expensive_computation}")   # Uses cached value


# ============================================================================
# EXAMPLE 7: __slots__ for Memory Optimization
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 7: Using __slots__ for Memory Efficiency")
print("="*70)

class Point:
    """Regular class with __dict__"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointWithSlots:
    """Memory-efficient class with __slots__"""
    __slots__ = ['x', 'y']

    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys

regular_point = Point(1, 2)
slotted_point = PointWithSlots(1, 2)

print(f"Regular Point size: {sys.getsizeof(regular_point)} bytes")
print(f"Slotted Point size: {sys.getsizeof(slotted_point)} bytes")

# Try adding dynamic attribute
try:
    slotted_point.z = 3  # Will raise AttributeError
except AttributeError as e:
    print(f"Cannot add dynamic attributes to slotted class: {e}")


# ============================================================================
# EXAMPLE 8: WeakRef for Memory Management
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 8: WeakRef for Cache Management")
print("="*70)

class ObjectCache:
    """Cache using weak references"""
    def __init__(self):
        self._cache = WeakValueDictionary()

    def add(self, key, obj):
        self._cache[key] = obj
        print(f"Added {key} to cache")

    def get(self, key):
        return self._cache.get(key)

    def size(self):
        return len(self._cache)

class CachedObject:
    def __init__(self, name):
        self.name = name

cache = ObjectCache()

# Add objects to cache
obj1 = CachedObject("Object 1")
obj2 = CachedObject("Object 2")
cache.add("obj1", obj1)
cache.add("obj2", obj2)

print(f"Cache size: {cache.size()}")
print(f"Retrieved: {cache.get('obj1').name}")

# Delete obj1 - weak reference allows garbage collection
del obj1
print(f"After deleting obj1, cache size: {cache.size()}")


# ============================================================================
# EXAMPLE 9: Custom Exception Hierarchy
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 9: Custom Exception Hierarchy")
print("="*70)

class MCPError(Exception):
    """Base exception for MCP"""
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.error_code = error_code
        self.timestamp = time.time()

class MCPConnectionError(MCPError):
    """Raised when connection fails"""
    pass

class MCPToolNotFoundError(MCPError):
    """Raised when requested tool doesn't exist"""
    pass

class MCPValidationError(MCPError):
    """Raised when validation fails"""
    def __init__(self, message, field_name, invalid_value):
        super().__init__(message, error_code="VALIDATION_ERROR")
        self.field_name = field_name
        self.invalid_value = invalid_value

def call_tool(tool_name):
    if tool_name not in ["read_file", "write_file"]:
        raise MCPToolNotFoundError(
            f"Tool '{tool_name}' not found",
            error_code="TOOL_NOT_FOUND"
        )

try:
    call_tool("invalid_tool")
except MCPToolNotFoundError as e:
    print(f"Error: {e}")
    print(f"Error code: {e.error_code}")
    print(f"Timestamp: {e.timestamp}")


# ============================================================================
# EXAMPLE 10: Generic Classes
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 10: Generic Classes")
print("="*70)

T = TypeVar('T')

class Stack(Generic[T]):
    """Generic stack implementation"""
    def __init__(self):
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        if not self._items:
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self) -> T:
        if not self._items:
            raise IndexError("Peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

# Type-safe stacks
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
int_stack.push(3)

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")

print(f"Int stack top: {int_stack.peek()}")
print(f"String stack top: {str_stack.peek()}")
print(f"Int stack size: {int_stack.size()}")


# ============================================================================
# EXAMPLE 11: Protocol Composition
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 11: Composing Protocols")
print("="*70)

class Readable(Protocol):
    def read(self) -> str: ...

class Writable(Protocol):
    def write(self, data: str) -> int: ...

class Closeable(Protocol):
    def close(self) -> None: ...

class ReadWritable(Readable, Writable, Protocol):
    """Composed protocol"""
    pass

class File:
    """Implements multiple protocols"""
    def __init__(self, filename):
        self.filename = filename
        self.position = 0

    def read(self) -> str:
        return f"Reading from {self.filename}"

    def write(self, data: str) -> int:
        return len(data)

    def close(self) -> None:
        print(f"Closing {self.filename}")

def process_file(f: ReadWritable) -> None:
    """Function accepting ReadWritable protocol"""
    content = f.read()
    f.write("processed data")
    print(f"Processed file")

file = File("data.txt")
process_file(file)


# ============================================================================
# EXAMPLE 12: Advanced Context Managers
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 12: Advanced Context Manager")
print("="*70)

class Transaction:
    """Transaction context manager with rollback"""
    def __init__(self, name):
        self.name = name
        self.committed = False

    def __enter__(self):
        print(f"Starting transaction: {self.name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"Rolling back transaction: {self.name} (Error: {exc_val})")
            return False  # Propagate exception
        elif not self.committed:
            print(f"Auto-committing transaction: {self.name}")
        return True

    def commit(self):
        self.committed = True
        print(f"Committed transaction: {self.name}")

    def execute(self, query):
        print(f"Executing: {query}")

# Successful transaction
with Transaction("txn1") as txn:
    txn.execute("INSERT INTO users VALUES (...)")
    txn.commit()

# Failed transaction
try:
    with Transaction("txn2") as txn:
        txn.execute("INSERT INTO users VALUES (...)")
        raise ValueError("Something went wrong!")
except ValueError:
    pass


# ============================================================================
# EXAMPLE 13: Context Manager as Generator
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 13: Context Manager with contextmanager Decorator")
print("="*70)

@contextmanager
def timer(name):
    """Context manager to measure execution time"""
    start = time.time()
    print(f"Starting {name}...")
    try:
        yield
    finally:
        elapsed = time.time() - start
        print(f"{name} took {elapsed:.4f} seconds")

with timer("Database query"):
    time.sleep(0.1)  # Simulate work

with timer("API call"):
    time.sleep(0.05)  # Simulate work


# ============================================================================
# EXAMPLE 14: Dependency Injection Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 14: Dependency Injection")
print("="*70)

class EmailService(Protocol):
    def send(self, to: str, message: str) -> bool: ...

class SMTPEmailService:
    def send(self, to: str, message: str) -> bool:
        print(f"SMTP: Sending email to {to}")
        return True

class MockEmailService:
    def send(self, to: str, message: str) -> bool:
        print(f"MOCK: Email to {to} (not actually sent)")
        return True

class UserService:
    """Service with dependency injection"""
    def __init__(self, email_service: EmailService):
        self.email_service = email_service

    def register_user(self, email: str, name: str) -> bool:
        # Business logic
        print(f"Registering user: {name}")

        # Send welcome email via injected service
        return self.email_service.send(
            email,
            f"Welcome {name}!"
        )

# Production
prod_user_service = UserService(SMTPEmailService())
prod_user_service.register_user("user@example.com", "John")

# Testing
test_user_service = UserService(MockEmailService())
test_user_service.register_user("test@example.com", "Test User")


# ============================================================================
# EXAMPLE 15: Builder Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 15: Builder Pattern")
print("="*70)

@dataclass
class Server:
    host: str
    port: int
    protocol: str = "http"
    timeout: int = 30
    max_connections: int = 100
    ssl_enabled: bool = False

class ServerBuilder:
    """Builder for complex Server configuration"""
    def __init__(self):
        self._host = "localhost"
        self._port = 8000
        self._protocol = "http"
        self._timeout = 30
        self._max_connections = 100
        self._ssl_enabled = False

    def with_host(self, host: str) -> 'ServerBuilder':
        self._host = host
        return self

    def with_port(self, port: int) -> 'ServerBuilder':
        self._port = port
        return self

    def with_https(self) -> 'ServerBuilder':
        self._protocol = "https"
        self._ssl_enabled = True
        self._port = 443
        return self

    def with_timeout(self, seconds: int) -> 'ServerBuilder':
        self._timeout = seconds
        return self

    def with_max_connections(self, count: int) -> 'ServerBuilder':
        self._max_connections = count
        return self

    def build(self) -> Server:
        return Server(
            host=self._host,
            port=self._port,
            protocol=self._protocol,
            timeout=self._timeout,
            max_connections=self._max_connections,
            ssl_enabled=self._ssl_enabled
        )

# Building servers with fluent interface
server1 = (ServerBuilder()
    .with_host("api.example.com")
    .with_port(8080)
    .with_timeout(60)
    .build())

server2 = (ServerBuilder()
    .with_host("secure.example.com")
    .with_https()
    .with_max_connections(500)
    .build())

print(f"Server 1: {server1}")
print(f"Server 2: {server2}")


# ============================================================================
# EXAMPLE 16: Chain of Responsibility Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 16: Chain of Responsibility")
print("="*70)

class Handler(ABC):
    """Abstract handler in chain"""
    def __init__(self):
        self._next_handler: Optional['Handler'] = None

    def set_next(self, handler: 'Handler') -> 'Handler':
        self._next_handler = handler
        return handler

    @abstractmethod
    def handle(self, request: dict) -> Optional[str]:
        pass

    def handle_next(self, request: dict) -> Optional[str]:
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

class AuthenticationHandler(Handler):
    def handle(self, request: dict) -> Optional[str]:
        if 'token' not in request:
            return "Authentication failed: No token"
        print("Authentication passed")
        return self.handle_next(request)

class AuthorizationHandler(Handler):
    def handle(self, request: dict) -> Optional[str]:
        if request.get('role') != 'admin':
            return "Authorization failed: Not an admin"
        print("Authorization passed")
        return self.handle_next(request)

class ValidationHandler(Handler):
    def handle(self, request: dict) -> Optional[str]:
        if 'data' not in request:
            return "Validation failed: No data"
        print("Validation passed")
        return self.handle_next(request)

class ProcessHandler(Handler):
    def handle(self, request: dict) -> Optional[str]:
        print("Processing request")
        return "Request processed successfully"

# Build chain
auth = AuthenticationHandler()
authz = AuthorizationHandler()
valid = ValidationHandler()
process = ProcessHandler()

auth.set_next(authz).set_next(valid).set_next(process)

# Test requests
request1 = {"token": "abc123", "role": "admin", "data": "test"}
result = auth.handle(request1)
print(f"Result: {result}\n")

request2 = {"token": "abc123", "role": "user", "data": "test"}
result = auth.handle(request2)
print(f"Result: {result}")


# ============================================================================
# EXAMPLE 17: Memento Pattern (State Snapshot)
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 17: Memento Pattern")
print("="*70)

@dataclass
class EditorMemento:
    """Snapshot of editor state"""
    content: str
    cursor_position: int

class TextEditor:
    """Text editor with undo capability"""
    def __init__(self):
        self.content = ""
        self.cursor_position = 0

    def write(self, text: str):
        self.content += text
        self.cursor_position = len(self.content)

    def save(self) -> EditorMemento:
        """Save current state"""
        return EditorMemento(self.content, self.cursor_position)

    def restore(self, memento: EditorMemento):
        """Restore from memento"""
        self.content = memento.content
        self.cursor_position = memento.cursor_position

    def __str__(self):
        return f"Content: '{self.content}', Cursor: {self.cursor_position}"

class History:
    """Manages mementos"""
    def __init__(self):
        self._mementos: list[EditorMemento] = []

    def push(self, memento: EditorMemento):
        self._mementos.append(memento)

    def pop(self) -> Optional[EditorMemento]:
        if self._mementos:
            return self._mementos.pop()
        return None

# Usage
editor = TextEditor()
history = History()

editor.write("Hello ")
history.push(editor.save())

editor.write("World")
history.push(editor.save())

editor.write("!")
print(f"Current: {editor}")

# Undo
editor.restore(history.pop())
print(f"After undo: {editor}")

editor.restore(history.pop())
print(f"After undo: {editor}")


# ============================================================================
# EXAMPLE 18: Visitor Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 18: Visitor Pattern")
print("="*70)

class NodeVisitor(ABC):
    """Abstract visitor"""
    @abstractmethod
    def visit_file(self, file): ...

    @abstractmethod
    def visit_directory(self, directory): ...

class FileSystemNode(ABC):
    """Abstract node in file system"""
    @abstractmethod
    def accept(self, visitor: NodeVisitor): ...

class File(FileSystemNode):
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_file(self)

class Directory(FileSystemNode):
    def __init__(self, name: str):
        self.name = name
        self.children: list[FileSystemNode] = []

    def add(self, node: FileSystemNode):
        self.children.append(node)

    def accept(self, visitor: NodeVisitor):
        return visitor.visit_directory(self)

class SizeCalculatorVisitor(NodeVisitor):
    """Visitor that calculates total size"""
    def visit_file(self, file: File) -> int:
        return file.size

    def visit_directory(self, directory: Directory) -> int:
        total = 0
        for child in directory.children:
            total += child.accept(self)
        return total

class PrintVisitor(NodeVisitor):
    """Visitor that prints file system structure"""
    def __init__(self):
        self.indent = 0

    def visit_file(self, file: File):
        print("  " * self.indent + f"File: {file.name} ({file.size} bytes)")

    def visit_directory(self, directory: Directory):
        print("  " * self.indent + f"Directory: {directory.name}")
        self.indent += 1
        for child in directory.children:
            child.accept(self)
        self.indent -= 1

# Build file system
root = Directory("root")
root.add(File("file1.txt", 100))
root.add(File("file2.txt", 200))

sub_dir = Directory("documents")
sub_dir.add(File("doc1.pdf", 500))
sub_dir.add(File("doc2.pdf", 300))
root.add(sub_dir)

# Use visitors
print_visitor = PrintVisitor()
root.accept(print_visitor)

size_calculator = SizeCalculatorVisitor()
total_size = root.accept(size_calculator)
print(f"\nTotal size: {total_size} bytes")


# ============================================================================
# EXAMPLE 19: Proxy Pattern
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 19: Proxy Pattern")
print("="*70)

class DatabaseInterface(Protocol):
    def query(self, sql: str) -> list: ...

class RealDatabase:
    """Expensive resource"""
    def __init__(self):
        print("Connecting to real database (expensive operation)...")
        time.sleep(0.1)

    def query(self, sql: str) -> list:
        print(f"Executing: {sql}")
        return [{"id": 1, "name": "Result"}]

class DatabaseProxy:
    """Lazy-loading proxy with caching"""
    def __init__(self):
        self._database: Optional[RealDatabase] = None
        self._cache: dict[str, list] = {}

    def query(self, sql: str) -> list:
        # Lazy initialization
        if self._database is None:
            self._database = RealDatabase()

        # Check cache
        if sql in self._cache:
            print(f"Returning cached result for: {sql}")
            return self._cache[sql]

        # Execute and cache
        result = self._database.query(sql)
        self._cache[sql] = result
        return result

# Using proxy
proxy = DatabaseProxy()
print("Proxy created (database not connected yet)\n")

result1 = proxy.query("SELECT * FROM users")
print(f"Result: {result1}\n")

result2 = proxy.query("SELECT * FROM users")  # Uses cache
print(f"Result: {result2}")


# ============================================================================
# EXAMPLE 20: Complete MCP Server Architecture
# ============================================================================
print("\n" + "="*70)
print("EXAMPLE 20: Production-Ready MCP Server Architecture")
print("="*70)

class MCPTool(ABC):
    """Abstract MCP tool"""
    @abstractmethod
    async def execute(self, params: dict) -> dict:
        pass

    @abstractmethod
    def get_schema(self) -> dict:
        pass

class ReadFileTool(MCPTool):
    async def execute(self, params: dict) -> dict:
        filepath = params.get('filepath')
        # Simulate file reading
        return {
            "success": True,
            "content": f"Contents of {filepath}",
            "size": 1024
        }

    def get_schema(self) -> dict:
        return {
            "name": "read_file",
            "description": "Read contents of a file",
            "parameters": {
                "filepath": {"type": "string", "required": True}
            }
        }

class MCPServer:
    """Production MCP Server with full features"""
    def __init__(self, name: str):
        self.name = name
        self._tools: dict[str, MCPTool] = {}
        self._middleware: list[Callable] = []

    def register_tool(self, name: str, tool: MCPTool):
        """Register a tool"""
        self._tools[name] = tool
        print(f"Registered tool: {name}")

    def add_middleware(self, middleware: Callable):
        """Add middleware for request processing"""
        self._middleware.append(middleware)

    async def call_tool(self, tool_name: str, params: dict) -> dict:
        """Call a tool with middleware support"""
        if tool_name not in self._tools:
            raise MCPToolNotFoundError(f"Tool '{tool_name}' not found")

        # Run middleware
        for middleware in self._middleware:
            params = middleware(params)

        # Execute tool
        tool = self._tools[tool_name]
        return await tool.execute(params)

    def list_tools(self) -> list[dict]:
        """List all available tools"""
        return [
            tool.get_schema()
            for tool in self._tools.values()
        ]

# Middleware functions
def logging_middleware(params: dict) -> dict:
    print(f"[Middleware] Processing request with params: {params}")
    return params

def validation_middleware(params: dict) -> dict:
    if not params:
        raise MCPValidationError("Empty parameters", "params", params)
    return params

# Create server
server = MCPServer("FileServer")
server.add_middleware(logging_middleware)
server.add_middleware(validation_middleware)
server.register_tool("read_file", ReadFileTool())

print(f"\nAvailable tools:")
for tool_schema in server.list_tools():
    print(f"  - {tool_schema['name']}: {tool_schema['description']}")


# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*70)
print("ADVANCED OOP CONCEPTS - SUMMARY")
print("="*70)
print("""
You've mastered:
✅ 1.  Metaclasses (Singleton, Registry, Validation)
✅ 2.  Class decorators
✅ 3.  Advanced descriptors (Type checking, Caching)
✅ 4.  Advanced context managers
✅ 5.  __slots__ for memory optimization
✅ 6.  WeakRef for memory management
✅ 7.  Custom exception hierarchies
✅ 8.  Generic classes
✅ 9.  Protocol composition
✅ 10. Dependency injection
✅ 11. Builder pattern
✅ 12. Chain of responsibility
✅ 13. Memento pattern
✅ 14. Visitor pattern
✅ 15. Proxy pattern
✅ 16. Context manager generators
✅ 17. Advanced typing
✅ 18. Production patterns
✅ 19. MCP architecture patterns
✅ 20. Complete server implementation

You are now ready to build production MCP servers! 🚀
""")
