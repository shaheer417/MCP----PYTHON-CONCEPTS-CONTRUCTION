"""
GENERICS - 10 REAL-LIFE CODING EXAMPLES
=========================================

Source: https://github.com/panaversity/learn-modern-ai-python/tree/main/00_python_colab
Topic: Generics - Type-Safe Flexible Code with TypeVar and Generic

This file contains 10 comprehensive examples showing how to use generics
to write type-safe, flexible, and reusable code for AI/MCP development.

WHAT ARE GENERICS?
Generics allow you to write code that works with MULTIPLE types while
maintaining TYPE SAFETY. Type checkers understand what types you're
working with, preventing bugs at development time.

Key Components:
• TypeVar - Define a generic type variable
• Generic[T] - Make a class generic
• List[T], Dict[K, V] - Generic built-in types
• Protocol - Structural subtyping

EXAMPLES:
1. Generic Functions - Type-Safe Utilities
2. Generic Container Class
3. Generic Response Wrapper
4. Generic Repository Pattern
5. Generic Cache Implementation
6. Generic Event System
7. Generic Pipeline Builder
8. Protocol for Duck Typing
9. Generic Async Operations
10. Complex Generic Types and Bounds
"""

from typing import TypeVar, Generic, List, Dict, Any, Optional, Protocol, Callable
from typing import Union, Tuple, Iterator, Type
from dataclasses import dataclass
from abc import ABC, abstractmethod
import asyncio
import time

print("=" * 80)
print("GENERICS - 10 REAL-LIFE CODING EXAMPLES")
print("=" * 80)
print("Master type-safe flexible programming!")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: Generic Functions - Type-Safe Utilities
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Generic Functions - Reusable with Type Safety")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Write utility functions that work with ANY type but maintain type safety.
Type checkers know what type is returned based on input!

LOGIC:
- Define TypeVar for generic type
- Use it in function signature
- Type checker infers return type from input
""")

T = TypeVar('T')

def get_first_item(items: List[T]) -> T:
    """Get first item from list (type-safe)"""
    if not items:
        raise ValueError("List is empty")
    return items[0]

def get_last_item(items: List[T]) -> T:
    """Get last item from list (type-safe)"""
    if not items:
        raise ValueError("List is empty")
    return items[-1]

def filter_none(items: List[Optional[T]]) -> List[T]:
    """Filter out None values (type-safe)"""
    return [item for item in items if item is not None]

def group_by_key(items: List[T], key_func: Callable[[T], str]) -> Dict[str, List[T]]:
    """Group items by a key function (type-safe)"""
    groups: Dict[str, List[T]] = {}

    for item in items:
        key = key_func(item)

        if key not in groups:
            groups[key] = []

        groups[key].append(item)

    return groups

print("\n▶ Testing generic functions:")

# Works with integers
int_list = [1, 2, 3, 4, 5]
first_int = get_first_item(int_list)
last_int = get_last_item(int_list)

print(f"  Integers: first={first_int}, last={last_int}")
print(f"     Types: {type(first_int).__name__}, {type(last_int).__name__}")

# Works with strings
str_list = ["hello", "world", "generics", "rock"]
first_str = get_first_item(str_list)
last_str = get_last_item(str_list)

print(f"\n  Strings: first='{first_str}', last='{last_str}'")
print(f"     Types: {type(first_str).__name__}, {type(last_str).__name__}")

# Filter None values
mixed_list: List[Optional[int]] = [1, None, 2, None, 3, 4, None]
filtered = filter_none(mixed_list)

print(f"\n  Filter None:")
print(f"     Input: {mixed_list}")
print(f"     Output: {filtered}")

# Group by key
@dataclass
class Tool:
    name: str
    category: str

tools = [
    Tool("read_file", "file"),
    Tool("write_file", "file"),
    Tool("web_search", "web"),
    Tool("db_query", "database"),
    Tool("list_dir", "file")
]

grouped = group_by_key(tools, lambda t: t.category)

print(f"\n  Grouped by category:")
for category, category_tools in grouped.items():
    print(f"     {category}: {[t.name for t in category_tools]}")

print("\n💡 KEY TAKEAWAY:")
print("   Generic functions work with ANY type")
print("   Type checker knows return type from input")
print("   Write once, use with any type safely!")

# ==============================================================================
# EXAMPLE 2: Generic Container Class
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: Generic Container - Type-Safe Data Structures")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build generic container classes (Box, Optional, Result) that work
with any type. Type checker ensures you don't mix types!

LOGIC:
- Define class with Generic[T]
- Methods return/accept type T
- Each instance is type-specific
""")

T = TypeVar('T')

class Box(Generic[T]):
    """Generic box container"""

    def __init__(self, value: T):
        self._value = value

    def get(self) -> T:
        """Get the value"""
        return self._value

    def set(self, value: T) -> None:
        """Set the value"""
        self._value = value

    def map(self, func: Callable[[T], Any]) -> 'Box':
        """Transform the value"""
        return Box(func(self._value))

    def __repr__(self):
        return f"Box({self._value})"

class Result(Generic[T]):
    """Generic Result type (success or error)"""

    def __init__(self, success: bool, value: T = None, error: str = None):
        self.success = success
        self.value = value
        self.error = error

    def is_ok(self) -> bool:
        """Check if result is successful"""
        return self.success

    def is_err(self) -> bool:
        """Check if result is error"""
        return not self.success

    def unwrap(self) -> T:
        """Get value or raise error"""
        if not self.success:
            raise RuntimeError(f"Called unwrap on error: {self.error}")
        return self.value

    def unwrap_or(self, default: T) -> T:
        """Get value or return default"""
        return self.value if self.success else default

    def __repr__(self):
        if self.success:
            return f"Ok({self.value})"
        return f"Err({self.error})"

print("\n▶ Testing Box container:")

# Box with integer
int_box = Box[int](42)
print(f"  Int box: {int_box}")
print(f"  Value: {int_box.get()}")

# Box with string
str_box = Box[str]("hello")
print(f"\n  String box: {str_box}")
print(f"  Value: {str_box.get()}")

# Map operation
doubled_box = int_box.map(lambda x: x * 2)
print(f"\n  Mapped (x2): {doubled_box}")

upper_box = str_box.map(lambda s: s.upper())
print(f"  Mapped (upper): {upper_box}")

# Test Result type
print("\n▶ Testing Result type:")

# Success result
success_result: Result[str] = Result(success=True, value="File contents")
print(f"  Success: {success_result}")
print(f"  Is OK: {success_result.is_ok()}")
print(f"  Value: {success_result.unwrap()}")

# Error result
error_result: Result[str] = Result(success=False, error="File not found")
print(f"\n  Error: {error_result}")
print(f"  Is Error: {error_result.is_err()}")
print(f"  With default: {error_result.unwrap_or('default value')}")

# Try to unwrap error (will fail)
print(f"\n  Attempting to unwrap error:")
try:
    error_result.unwrap()
except RuntimeError as e:
    print(f"  ❌ Caught: {e}")

print("\n💡 KEY TAKEAWAY:")
print("   Generic[T] makes classes work with any type")
print("   Type-safe: Box[int] != Box[str]")
print("   Build reusable containers for any data type!")

# ==============================================================================
# EXAMPLE 3: Generic Response Wrapper for MCP
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Generic MCP Response - Type-Safe Tool Results")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
MCP tools return different types of data:
- read_file → string
- list_directory → List[string]
- execute_bash → Dict[str, Any]

Use generic Response to wrap ALL tool results type-safely!

LOGIC:
- Response[T] where T is the data type
- Type checker knows what type of data is inside
- Safe unwrapping and error handling
""")

T = TypeVar('T')

class MCPResponse(Generic[T]):
    """Generic MCP response wrapper"""

    def __init__(self, success: bool, data: T = None,
                 error: Optional[str] = None,
                 execution_time_ms: float = 0):
        self.success = success
        self.data = data
        self.error = error
        self.execution_time_ms = execution_time_ms

    def is_success(self) -> bool:
        return self.success

    def get_data(self) -> T:
        """Get data or raise error"""
        if not self.success:
            raise RuntimeError(f"Response error: {self.error}")
        return self.data

    def get_or_default(self, default: T) -> T:
        """Get data or return default"""
        return self.data if self.success else default

    def map(self, func: Callable[[T], Any]) -> 'MCPResponse':
        """Transform data if success"""
        if self.success and self.data is not None:
            return MCPResponse(True, func(self.data), None, self.execution_time_ms)
        return MCPResponse(False, None, self.error, self.execution_time_ms)

    def __repr__(self):
        if self.success:
            return f"MCPResponse(success, data={self.data}, time={self.execution_time_ms}ms)"
        return f"MCPResponse(error={self.error}, time={self.execution_time_ms}ms)"

# Different response types
@dataclass
class FileContents:
    path: str
    content: str
    size_bytes: int

@dataclass
class DirectoryListing:
    path: str
    files: List[str]
    directories: List[str]

@dataclass
class BashResult:
    command: str
    stdout: str
    stderr: str
    exit_code: int

print("\n▶ Creating type-specific responses:")

# Response with FileContents
file_response: MCPResponse[FileContents] = MCPResponse(
    success=True,
    data=FileContents(
        path="/data/test.txt",
        content="Hello, World!",
        size_bytes=13
    ),
    execution_time_ms=45.2
)

print(f"  File response: {file_response}")
print(f"  Data: {file_response.get_data().path}")

# Response with DirectoryListing
dir_response: MCPResponse[DirectoryListing] = MCPResponse(
    success=True,
    data=DirectoryListing(
        path="/data",
        files=["file1.txt", "file2.txt"],
        directories=["subdir1", "subdir2"]
    ),
    execution_time_ms=12.5
)

print(f"\n  Directory response: {dir_response}")
print(f"  Files: {dir_response.get_data().files}")

# Error response
error_response: MCPResponse[FileContents] = MCPResponse(
    success=False,
    error="Permission denied: /restricted/file.txt",
    execution_time_ms=2.1
)

print(f"\n  Error response: {error_response}")
print(f"  With default: {error_response.get_or_default(FileContents('', '', 0))}")

# Map operation
print("\n▶ Transforming responses with map():")

# Extract just the size
size_response = file_response.map(lambda fc: fc.size_bytes)
print(f"  Original: {file_response.data}")
print(f"  Mapped to size: {size_response.data}")

# Count files
count_response = dir_response.map(lambda dl: len(dl.files))
print(f"  Mapped to count: {count_response.data}")

print("\n💡 KEY TAKEAWAY:")
print("   Generic[T] for type-safe wrappers")
print("   Each tool returns MCPResponse[SpecificType]")
print("   Type checker prevents mixing types!")

# ==============================================================================
# EXAMPLE 4: Generic Repository Pattern
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: Generic Repository - Database Access Layer")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build a generic repository for database operations. Works with any
model type (User, Tool, Config) but maintains type safety.

LOGIC:
- Repository[T] where T is the model type
- Methods return type T (not just 'Any')
- Reusable for all database models
""")

T = TypeVar('T')

class Repository(Generic[T]):
    """Generic repository for database operations"""

    def __init__(self, model_type: Type[T]):
        self.model_type = model_type
        self._storage: Dict[str, T] = {}

    def save(self, id: str, entity: T) -> T:
        """Save entity to repository"""
        self._storage[id] = entity
        print(f"  💾 Saved {self.model_type.__name__}: {id}")
        return entity

    def find_by_id(self, id: str) -> Optional[T]:
        """Find entity by ID"""
        return self._storage.get(id)

    def find_all(self) -> List[T]:
        """Get all entities"""
        return list(self._storage.values())

    def delete(self, id: str) -> bool:
        """Delete entity by ID"""
        if id in self._storage:
            del self._storage[id]
            print(f"  🗑️  Deleted {self.model_type.__name__}: {id}")
            return True
        return False

    def count(self) -> int:
        """Count entities"""
        return len(self._storage)

    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """Filter entities by predicate"""
        return [entity for entity in self._storage.values()
                if predicate(entity)]

# Define models
@dataclass
class User:
    username: str
    email: str
    age: int

@dataclass
class MCPTool:
    name: str
    category: str
    enabled: bool

print("\n▶ Creating type-specific repositories:")

# User repository
user_repo = Repository[User](User)

user1 = user_repo.save("user-1", User("alice", "alice@example.com", 25))
user2 = user_repo.save("user-2", User("bob", "bob@example.com", 30))

print(f"     User count: {user_repo.count()}")

# Tool repository
tool_repo = Repository[MCPTool](MCPTool)

tool1 = tool_repo.save("tool-1", MCPTool("read_file", "file_ops", True))
tool2 = tool_repo.save("tool-2", MCPTool("web_search", "web", True))

print(f"     Tool count: {tool_repo.count()}")

# Type-safe retrieval
print("\n▶ Type-safe retrieval:")

found_user = user_repo.find_by_id("user-1")
if found_user:
    print(f"  User found: {found_user.username}, age {found_user.age}")

found_tool = tool_repo.find_by_id("tool-1")
if found_tool:
    print(f"  Tool found: {found_tool.name}, category {found_tool.category}")

# Filter operation (type-safe!)
print("\n▶ Filtering:")

adults = user_repo.filter(lambda u: u.age >= 18)
print(f"  Adults: {[u.username for u in adults]}")

enabled_tools = tool_repo.filter(lambda t: t.enabled)
print(f"  Enabled tools: {[t.name for t in enabled_tools]}")

print("\n💡 KEY TAKEAWAY:")
print("   Generic repository pattern for database access")
print("   Type-safe CRUD operations")
print("   Reusable across all model types!")

# ==============================================================================
# EXAMPLE 5: Generic Cache Implementation
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: Generic Cache - Type-Safe Caching Layer")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build a caching layer for expensive operations (API calls, computations).
Cache works with any type while maintaining type safety.

LOGIC:
- Cache[K, V] where K is key type, V is value type
- Generic over both key and value
- Type-safe get/set operations
""")

K = TypeVar('K')
V = TypeVar('V')

class Cache(Generic[K, V]):
    """Generic cache with TTL support"""

    def __init__(self, ttl_seconds: float = 300):
        self.ttl_seconds = ttl_seconds
        self._cache: Dict[K, Tuple[V, float]] = {}  # (value, expiry_time)

    def set(self, key: K, value: V) -> None:
        """Set cache entry"""
        expiry = time.time() + self.ttl_seconds
        self._cache[key] = (value, expiry)
        print(f"  📥 Cached: {key}")

    def get(self, key: K) -> Optional[V]:
        """Get cache entry (None if expired or missing)"""
        if key not in self._cache:
            print(f"  ❌ Cache miss: {key}")
            return None

        value, expiry = self._cache[key]

        # Check if expired
        if time.time() > expiry:
            print(f"  ⏰ Cache expired: {key}")
            del self._cache[key]
            return None

        print(f"  ✓ Cache hit: {key}")
        return value

    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
        print(f"  🧹 Cache cleared")

    def size(self) -> int:
        """Get cache size"""
        return len(self._cache)

# Different cache types
print("\n▶ Creating typed caches:")

# String → String cache (for API responses)
api_cache = Cache[str, str](ttl_seconds=10)

# Int → Dict cache (for database queries)
db_cache = Cache[int, Dict[str, Any]](ttl_seconds=20)

# Tuple → List cache (for search results)
search_cache = Cache[Tuple[str, str], List[str]](ttl_seconds=5)

print("\n▶ Using API cache:")
api_cache.set("api.example.com/users", "User data from API")
api_cache.set("api.example.com/posts", "Post data from API")

result1 = api_cache.get("api.example.com/users")
print(f"     Retrieved: {result1}")

# Test DB cache
print("\n▶ Using DB cache:")
db_cache.set(1, {"name": "Alice", "age": 25})
db_cache.set(2, {"name": "Bob", "age": 30})

user_data = db_cache.get(1)
print(f"     User data: {user_data}")

# Test search cache
print("\n▶ Using search cache:")
search_key = ("python", "asyncio")
search_cache.set(search_key, ["Result 1", "Result 2", "Result 3"])

search_results = search_cache.get(search_key)
print(f"     Search results: {search_results}")

# Test expiration
print("\n▶ Testing cache expiration:")
short_cache = Cache[str, int](ttl_seconds=1)
short_cache.set("key", 100)

print("  Waiting 2 seconds...")
time.sleep(2)

expired_value = short_cache.get("key")
print(f"  Value after expiration: {expired_value}")

print("\n💡 KEY TAKEAWAY:")
print("   Generic[K, V] for key-value stores")
print("   Type-safe caching for any data type")
print("   Use for: API caching, memoization, query caching")

# ==============================================================================
# EXAMPLE 6: Generic Event System
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Generic Event System - Type-Safe Pub/Sub")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build an event system where publishers emit events and subscribers
receive them. Each event type is strongly typed!

LOGIC:
- EventBus[T] where T is the event type
- Subscribers receive events of type T
- Type-safe event handling
""")

T = TypeVar('T')

class EventBus(Generic[T]):
    """Generic event bus for publish/subscribe"""

    def __init__(self, event_type_name: str):
        self.event_type_name = event_type_name
        self._subscribers: List[Callable[[T], None]] = []

    def subscribe(self, callback: Callable[[T], None]) -> None:
        """Subscribe to events"""
        self._subscribers.append(callback)
        print(f"  📡 Subscriber added to {self.event_type_name} bus")

    def publish(self, event: T) -> None:
        """Publish event to all subscribers"""
        print(f"  📢 Publishing {self.event_type_name} event to {len(self._subscribers)} subscribers")

        for subscriber in self._subscribers:
            try:
                subscriber(event)
            except Exception as e:
                print(f"  ⚠️ Subscriber error: {e}")

    def subscriber_count(self) -> int:
        """Get number of subscribers"""
        return len(self._subscribers)

# Define event types
@dataclass
class ToolExecutedEvent:
    tool_name: str
    execution_time_ms: float
    success: bool

@dataclass
class UserLoginEvent:
    user_id: str
    timestamp: datetime
    ip_address: str

@dataclass
class ErrorEvent:
    error_code: int
    message: str
    severity: str

print("\n▶ Creating event buses:")

# Tool execution events
tool_bus = EventBus[ToolExecutedEvent]("ToolExecution")

# User login events
login_bus = EventBus[UserLoginEvent]("UserLogin")

# Error events
error_bus = EventBus[ErrorEvent]("Error")

# Add subscribers
print("\n▶ Adding subscribers:")

def log_tool_execution(event: ToolExecutedEvent):
    """Log tool execution"""
    status = "✓" if event.success else "✗"
    print(f"    [Logger] Tool {event.tool_name} {status} ({event.execution_time_ms}ms)")

def monitor_tool_execution(event: ToolExecutedEvent):
    """Monitor tool performance"""
    if event.execution_time_ms > 100:
        print(f"    [Monitor] ⚠️ Slow tool: {event.tool_name}")

def handle_user_login(event: UserLoginEvent):
    """Handle user login"""
    print(f"    [Auth] User {event.user_id} logged in from {event.ip_address}")

def handle_error(event: ErrorEvent):
    """Handle error events"""
    print(f"    [Error Handler] {event.severity}: {event.message}")

tool_bus.subscribe(log_tool_execution)
tool_bus.subscribe(monitor_tool_execution)

login_bus.subscribe(handle_user_login)

error_bus.subscribe(handle_error)

# Publish events
print("\n▶ Publishing events:")

print("\n  Tool execution event:")
tool_bus.publish(ToolExecutedEvent(
    tool_name="read_file",
    execution_time_ms=45.5,
    success=True
))

print("\n  Slow tool event:")
tool_bus.publish(ToolExecutedEvent(
    tool_name="web_search",
    execution_time_ms=150.0,
    success=True
))

print("\n  User login event:")
login_bus.publish(UserLoginEvent(
    user_id="user-123",
    timestamp=datetime.now(),
    ip_address="192.168.1.1"
))

print("\n  Error event:")
error_bus.publish(ErrorEvent(
    error_code=500,
    message="Database connection failed",
    severity="CRITICAL"
))

print("\n💡 KEY TAKEAWAY:")
print("   Generic event bus for type-safe pub/sub")
print("   Different event types, separate buses")
print("   Subscribers are type-safe!")

# ==============================================================================
# EXAMPLE 7: Generic Pipeline Builder
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 7: Generic Pipeline - Chaining Type-Safe Operations")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build a data processing pipeline where each stage transforms data.
Input type → Output type, maintaining type safety through the chain!

LOGIC:
- Pipeline[In, Out] transforms In to Out
- Chain multiple pipelines together
- Type checker ensures compatibility
""")

In = TypeVar('In')
Out = TypeVar('Out')

class Pipeline(Generic[In, Out]):
    """Generic pipeline stage"""

    def __init__(self, name: str, transform: Callable[[In], Out]):
        self.name = name
        self.transform = transform

    def run(self, input_data: In) -> Out:
        """Run pipeline stage"""
        print(f"  ⚙️  Running pipeline stage: {self.name}")
        result = self.transform(input_data)
        return result

    def then(self, next_stage: 'Pipeline[Out, Any]') -> 'Pipeline[In, Any]':
        """Chain another pipeline stage"""
        def combined(input_data: In):
            intermediate = self.run(input_data)
            return next_stage.run(intermediate)

        return Pipeline(
            name=f"{self.name} → {next_stage.name}",
            transform=combined
        )

print("\n▶ Building data processing pipeline:")

# Stage 1: str → List[str] (split text)
split_stage = Pipeline[str, List[str]](
    name="Split Text",
    transform=lambda text: text.split()
)

# Stage 2: List[str] → List[str] (filter short words)
filter_stage = Pipeline[List[str], List[str]](
    name="Filter Short Words",
    transform=lambda words: [w for w in words if len(w) > 3]
)

# Stage 3: List[str] → int (count words)
count_stage = Pipeline[List[str], int](
    name="Count Words",
    transform=lambda words: len(words)
)

# Stage 4: int → str (format result)
format_stage = Pipeline[int, str](
    name="Format Result",
    transform=lambda count: f"Total words: {count}"
)

# Chain stages together
print("\n  Building complete pipeline:")
complete_pipeline = (
    split_stage
    .then(filter_stage)
    .then(count_stage)
    .then(format_stage)
)

# Run pipeline
print("\n▶ Running pipeline:")
input_text = "The quick brown fox jumps over the lazy dog"
result = complete_pipeline.run(input_text)

print(f"\n  Input: '{input_text}'")
print(f"  Output: '{result}'")

# Another example with different types
print("\n▶ Building number processing pipeline:")

# int → int (square)
square = Pipeline[int, int]("Square", lambda x: x ** 2)

# int → float (divide by 10)
divide = Pipeline[int, float]("Divide by 10", lambda x: x / 10)

# float → str (format)
format_num = Pipeline[float, str]("Format", lambda x: f"{x:.2f}")

number_pipeline = square.then(divide).then(format_num)

print("\n  Running number pipeline:")
number_result = number_pipeline.run(5)
print(f"     Input: 5")
print(f"     Output: {number_result}")

print("\n💡 KEY TAKEAWAY:")
print("   Pipeline[In, Out] for type-safe transformations")
print("   Chain operations while maintaining type safety")
print("   Use for: Data pipelines, ETL, processing chains")

# ==============================================================================
# EXAMPLE 8: Protocol for Duck Typing
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 8: Protocol - Structural Subtyping")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Define interfaces based on BEHAVIOR, not inheritance. Any class that
has the required methods satisfies the protocol - no explicit inheritance!

LOGIC:
- Protocol defines required methods
- Any class with those methods satisfies the protocol
- Duck typing with type safety!
""")

class Serializable(Protocol):
    """Protocol for serializable objects"""

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        ...

    def to_json(self) -> str:
        """Convert to JSON"""
        ...

class Executable(Protocol):
    """Protocol for executable objects"""

    def execute(self, **kwargs) -> Any:
        """Execute the object"""
        ...

def serialize_and_save(obj: Serializable, filename: str) -> None:
    """Save any serializable object"""
    data = obj.to_dict()
    json_str = obj.to_json()
    print(f"  💾 Saving {filename}: {len(json_str)} bytes")

def execute_and_log(obj: Executable, **kwargs) -> Any:
    """Execute any executable object"""
    print(f"  ⚙️  Executing {obj.__class__.__name__}")
    result = obj.execute(**kwargs)
    print(f"  ✓ Result: {result}")
    return result

# Classes that satisfy protocols (no explicit inheritance!)
class Tool:
    """Tool class (satisfies both protocols!)"""

    def __init__(self, name: str):
        self.name = name

    def to_dict(self) -> dict:
        return {"name": self.name}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def execute(self, **kwargs) -> str:
        return f"Tool {self.name} executed with {kwargs}"

class Config:
    """Config class (satisfies Serializable)"""

    def __init__(self, settings: dict):
        self.settings = settings

    def to_dict(self) -> dict:
        return self.settings

    def to_json(self) -> str:
        return json.dumps(self.settings)

print("\n▶ Using protocols:")

# Tool satisfies both protocols
tool = Tool("read_file")

print("\n  As Serializable:")
serialize_and_save(tool, "tool.json")

print("\n  As Executable:")
execute_and_log(tool, path="/data/file.txt")

# Config satisfies Serializable
config = Config({"host": "localhost", "port": 8080})

print("\n  Config as Serializable:")
serialize_and_save(config, "config.json")

print("\n💡 KEY TAKEAWAY:")
print("   Protocol = structural subtyping (duck typing + types)")
print("   No inheritance needed - just implement the methods")
print("   Flexible interfaces for Python!")

# ==============================================================================
# EXAMPLE 9: Generic Async Operations
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 9: Async Generics - Type-Safe Concurrent Operations")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Combine generics with asyncio for type-safe concurrent operations.
Perfect for MCP servers executing different tool types concurrently!

LOGIC:
- Generic async functions
- Maintain type safety through async operations
- Type-safe concurrent execution
""")

T = TypeVar('T')

class AsyncResult(Generic[T]):
    """Generic async result wrapper"""

    def __init__(self, value: T):
        self._value = value

    async def get(self) -> T:
        """Get value asynchronously"""
        await asyncio.sleep(0.1)  # Simulate async operation
        return self._value

    async def map(self, func: Callable[[T], Any]) -> 'AsyncResult':
        """Transform value asynchronously"""
        value = await self.get()
        transformed = func(value)
        return AsyncResult(transformed)

async def fetch_async(key: str, value: T) -> T:
    """Generic async fetch operation"""
    print(f"    🔄 Fetching {key}...")
    await asyncio.sleep(0.5)
    print(f"    ✓ Retrieved {key}")
    return value

async def process_async(data: T, processor: Callable[[T], Any]) -> Any:
    """Generic async processor"""
    print(f"    ⚙️  Processing {type(data).__name__}...")
    await asyncio.sleep(0.3)
    result = processor(data)
    print(f"    ✓ Processed: {result}")
    return result

async def demo_async_generics():
    """Demonstrate async generic operations"""

    print("\n▶ Async generic operations:")

    # Fetch different types
    print("\n  Fetching different types concurrently:")

    str_result, int_result, list_result = await asyncio.gather(
        fetch_async("name", "Claude"),
        fetch_async("count", 42),
        fetch_async("items", ["a", "b", "c"])
    )

    print(f"     String: {str_result}")
    print(f"     Integer: {int_result}")
    print(f"     List: {list_result}")

    # Process with type-safe processors
    print("\n  Processing with type-specific logic:")

    processed_str = await process_async(str_result, lambda s: s.upper())
    processed_int = await process_async(int_result, lambda n: n * 2)
    processed_list = await process_async(list_result, lambda l: len(l))

    print(f"     Processed string: {processed_str}")
    print(f"     Processed int: {processed_int}")
    print(f"     Processed list length: {processed_list}")

    # Test AsyncResult
    print("\n  Using AsyncResult wrapper:")

    result = AsyncResult[str]("initial value")
    value = await result.get()
    print(f"     Got value: {value}")

    # Chain transformations
    transformed = await (await result.map(str.upper)).map(lambda s: f"[{s}]")
    final = await transformed.get()
    print(f"     Transformed: {final}")

asyncio.run(demo_async_generics())

print("\n💡 KEY TAKEAWAY:")
print("   Generics work with async/await!")
print("   Type-safe concurrent operations")
print("   Perfect for MCP async tool execution")

# ==============================================================================
# EXAMPLE 10: Complex Generic Types and Bounds
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Advanced Generics - Bounds and Constraints")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Sometimes you need generics with constraints:
- T must be a number (int or float)
- T must be comparable
- T must have specific methods

LOGIC:
- TypeVar with bounds restricts allowed types
- Protocol for structural constraints
- Multiple generic type variables
""")

from numbers import Number

# Bounded TypeVar (only numeric types)
NumT = TypeVar('NumT', int, float)

def calculate_average(numbers: List[NumT]) -> float:
    """Calculate average of numeric values"""
    if not numbers:
        return 0.0

    total = sum(numbers)
    return total / len(numbers)

def find_max(numbers: List[NumT]) -> NumT:
    """Find maximum (works with int or float)"""
    if not numbers:
        raise ValueError("Empty list")

    return max(numbers)

# Protocol for comparable
class Comparable(Protocol):
    """Protocol for objects that can be compared"""

    def __lt__(self, other: Any) -> bool: ...
    def __le__(self, other: Any) -> bool: ...
    def __gt__(self, other: Any) -> bool: ...
    def __ge__(self, other: Any) -> bool: ...

T_Comparable = TypeVar('T_Comparable', bound=Comparable)

def sort_items(items: List[T_Comparable]) -> List[T_Comparable]:
    """Sort any comparable items"""
    return sorted(items)

# Multiple type variables
K = TypeVar('K')
V = TypeVar('V')

class BiDirectionalMap(Generic[K, V]):
    """Bidirectional map (forward and reverse lookup)"""

    def __init__(self):
        self._forward: Dict[K, V] = {}
        self._reverse: Dict[V, K] = {}

    def set(self, key: K, value: V) -> None:
        """Set key-value pair"""
        self._forward[key] = value
        self._reverse[value] = key

    def get_by_key(self, key: K) -> Optional[V]:
        """Get value by key"""
        return self._forward.get(key)

    def get_by_value(self, value: V) -> Optional[K]:
        """Get key by value (reverse lookup)"""
        return self._reverse.get(value)

print("\n▶ Testing bounded generics:")

# Works with int
int_avg = calculate_average([1, 2, 3, 4, 5])
print(f"  Int average: {int_avg}")

# Works with float
float_avg = calculate_average([1.5, 2.5, 3.5])
print(f"  Float average: {float_avg}")

# Find max
max_int = find_max([3, 7, 2, 9, 1])
max_float = find_max([3.14, 2.71, 1.41])

print(f"  Max int: {max_int}")
print(f"  Max float: {max_float}")

# Test comparable protocol
print("\n▶ Testing comparable protocol:")

@dataclass
class Priority:
    """Comparable priority"""
    level: int

    def __lt__(self, other):
        return self.level < other.level

    def __le__(self, other):
        return self.level <= other.level

    def __gt__(self, other):
        return self.level > other.level

    def __ge__(self, other):
        return self.level >= other.level

priorities = [Priority(3), Priority(1), Priority(2)]
sorted_priorities = sort_items(priorities)

print(f"  Unsorted: {[p.level for p in priorities]}")
print(f"  Sorted: {[p.level for p in sorted_priorities]}")

# Test bidirectional map
print("\n▶ Testing bidirectional map:")

# String → Int map
id_map = BiDirectionalMap[str, int]()

id_map.set("user-1", 101)
id_map.set("user-2", 102)
id_map.set("user-3", 103)

print(f"  Forward lookup (user-1): {id_map.get_by_key('user-1')}")
print(f"  Reverse lookup (102): {id_map.get_by_value(102)}")

# Tool name → Tool ID map
tool_map = BiDirectionalMap[str, str]()

tool_map.set("read_file", "tool-001")
tool_map.set("write_file", "tool-002")

print(f"\n  Tool name → ID: {tool_map.get_by_key('read_file')}")
print(f"  Tool ID → name: {tool_map.get_by_value('tool-001')}")

print("\n💡 KEY TAKEAWAY:")
print("   Bounded TypeVar restricts allowed types")
print("   Protocol for structural constraints")
print("   Multiple type variables for complex generics")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 ALL 10 GENERICS EXAMPLES COMPLETED!")
print("=" * 80)

summary = """
What You've Mastered:

1. ✅ Generic Functions - Type-safe utilities
2. ✅ Generic Container - Box, Result types
3. ✅ MCP Response - Type-safe tool results
4. ✅ Repository Pattern - Generic database access
5. ✅ Generic Cache - Type-safe caching
6. ✅ Event System - Type-safe pub/sub
7. ✅ Pipeline Builder - Chaining transformations
8. ✅ Protocol - Duck typing with type safety
9. ✅ Async Generics - Type-safe concurrent ops
10. ✅ Advanced Generics - Bounds and constraints

Key Generic Concepts:
────────────────────────────────────────────────
• TypeVar('T') - Define generic type variable
• Generic[T] - Make class generic
• Multiple TypeVars - Generic[K, V]
• Bounded TypeVar - Restrict to specific types
• Protocol - Structural typing (duck typing + types)

Common Patterns:
────────────────────────────────────────────────
• Container[T] - Box, Optional, Result
• Repository[T] - Database access
• Cache[K, V] - Key-value caching
• Response[T] - Wrapped results
• Pipeline[In, Out] - Data transformations

Type Safety Benefits:
────────────────────────────────────────────────
✓ Type checker catches errors before runtime
✓ Better IDE autocomplete
✓ Self-documenting code
✓ Refactoring safety
✓ Clear interfaces

When to Use Generics:
────────────────────────────────────────────────
✓ Building reusable data structures
✓ Wrapper classes (Result, Response, Cache)
✓ Repository/DAO patterns
✓ Pipeline and chain operations
✓ Event systems
✓ Any code working with "any type"

Real-World Uses in MCP/AI:
────────────────────────────────────────────────
✓ MCPResponse[T] - Different tool result types
✓ Repository[Tool] - Tool storage
✓ Cache[str, ToolResult] - Result caching
✓ Pipeline[Input, Output] - Data processing
✓ EventBus[EventType] - Event handling

You've completed all Python Prerequisites! 🎉
"""

print(summary)

print("\n" + "=" * 80)
print("📝 PRACTICE SUGGESTIONS:")
print("=" * 80)
print("""
1. Build a generic data structure (Tree, Graph, Queue)
2. Implement Result type for error handling
3. Create generic cache for your application
4. Build type-safe pipeline for data processing
5. Use Protocol to define flexible interfaces

🎓 YOU'VE COMPLETED ALL 6 PYTHON TOPICS!
   Total: 60+ comprehensive examples across 6 files

Next Step: Deep dive into MCP (Model Context Protocol)!
""")
