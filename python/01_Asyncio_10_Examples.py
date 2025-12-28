"""
ASYNCIO - 10 REAL-LIFE CODING EXAMPLES
========================================

Source: https://github.com/panaversity/learn-modern-ai-python/tree/main/00_python_colab
Topic: Asynchronous Programming for AI-Native Development

This file contains 10 comprehensive, real-world examples of asyncio usage
in AI and MCP development scenarios.

EXAMPLES:
1. Concurrent API Calls to Multiple Services
2. MCP Server with Multiple Client Connections
3. Real-Time Data Streaming Pipeline
4. Async File I/O for Large Dataset Processing
5. WebSocket Server for Live AI Responses
6. Task Timeout and Cancellation Management
7. Producer-Consumer Pattern for AI Workloads
8. Async Database Connection Pool
9. Parallel AI Model Inference
10. Async Rate Limiting for API Calls
"""

import asyncio
import time
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json

print("=" * 80)
print("ASYNCIO - 10 REAL-LIFE CODING EXAMPLES")
print("=" * 80)
print("Master asynchronous programming for AI-native development!")
print("=" * 80)

# ==============================================================================
# EXAMPLE 1: Concurrent API Calls to Multiple Services
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 1: Concurrent API Calls to Multiple Services")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Your AI application needs to gather data from multiple APIs simultaneously:
- OpenAI API for text generation
- Anthropic API for Claude responses
- Database API for user context
- Analytics API for logging

Instead of waiting for each API call sequentially (slow!), we call them
all at once using asyncio.
""")

@dataclass
class APIResponse:
    """Represents response from an API call"""
    service: str
    data: Any
    latency: float
    success: bool
    error: Optional[str] = None

async def call_openai_api(prompt: str) -> APIResponse:
    """Simulate calling OpenAI API"""
    start = time.time()
    print(f"  [OpenAI] Sending request: '{prompt[:30]}...'")

    await asyncio.sleep(1.2)  # Simulate network latency

    latency = time.time() - start
    return APIResponse(
        service="OpenAI",
        data={"response": "AI generated text...", "tokens": 150},
        latency=latency,
        success=True
    )

async def call_anthropic_api(prompt: str) -> APIResponse:
    """Simulate calling Anthropic Claude API"""
    start = time.time()
    print(f"  [Anthropic] Sending request: '{prompt[:30]}...'")

    await asyncio.sleep(1.5)  # Simulate network latency

    latency = time.time() - start
    return APIResponse(
        service="Anthropic",
        data={"response": "Claude's response...", "tokens": 200},
        latency=latency,
        success=True
    )

async def call_database_api(user_id: str) -> APIResponse:
    """Simulate database query for user context"""
    start = time.time()
    print(f"  [Database] Fetching context for user: {user_id}")

    await asyncio.sleep(0.8)  # Simulate DB query

    latency = time.time() - start
    return APIResponse(
        service="Database",
        data={"user": user_id, "preferences": {"theme": "dark"}},
        latency=latency,
        success=True
    )

async def call_analytics_api(event: str) -> APIResponse:
    """Simulate logging to analytics service"""
    start = time.time()
    print(f"  [Analytics] Logging event: {event}")

    await asyncio.sleep(0.5)  # Simulate logging

    latency = time.time() - start
    return APIResponse(
        service="Analytics",
        data={"event_id": "evt-123", "logged": True},
        latency=latency,
        success=True
    )

async def aggregate_ai_responses(prompt: str, user_id: str):
    """Call all APIs concurrently and aggregate responses"""
    print("\n▶ Starting concurrent API calls...")
    start_time = time.time()

    # Launch all API calls concurrently
    responses = await asyncio.gather(
        call_openai_api(prompt),
        call_anthropic_api(prompt),
        call_database_api(user_id),
        call_analytics_api("ai_query"),
        return_exceptions=True  # Don't fail if one API fails
    )

    total_time = time.time() - start_time

    print(f"\n✅ All APIs completed in {total_time:.2f}s")
    print("\n📊 Results Summary:")

    for response in responses:
        if isinstance(response, Exception):
            print(f"  ❌ Error: {response}")
        else:
            status = "✓" if response.success else "✗"
            print(f"  {status} {response.service}: {response.latency:.2f}s")

    # Calculate what sequential time would have been
    sequential_time = sum(r.latency for r in responses if isinstance(r, APIResponse))
    print(f"\n⚡ Speed improvement: {sequential_time / total_time:.1f}x faster than sequential!")

    return responses

# Run example 1
asyncio.run(aggregate_ai_responses(
    prompt="Explain quantum computing in simple terms",
    user_id="user-12345"
))

print("\n💡 KEY TAKEAWAY:")
print("   Use asyncio.gather() to run multiple async operations concurrently.")
print("   Perfect for: API calls, database queries, file I/O - anything with waiting!")

# ==============================================================================
# EXAMPLE 2: MCP Server with Multiple Client Connections
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 2: MCP Server with Multiple Client Connections")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
An MCP server needs to handle requests from multiple Claude Code clients
simultaneously. Each client sends tool execution requests that take time
to process. Server must handle all clients concurrently without blocking.
""")

class MCPServer:
    """Simulates an MCP server handling multiple clients"""

    def __init__(self, max_clients: int = 10):
        self.max_clients = max_clients
        self.active_clients: Dict[str, asyncio.Task] = {}
        self.request_count = 0

    async def handle_client(self, client_id: str, num_requests: int):
        """Handle a single client's requests"""
        print(f"  🔌 Client {client_id} connected")

        try:
            for i in range(num_requests):
                self.request_count += 1
                request_id = f"req-{self.request_count}"

                # Simulate processing tool request
                tool_name = random.choice(["read_file", "write_file", "execute_bash"])
                print(f"    [{client_id}] Processing {tool_name} ({request_id})")

                await asyncio.sleep(random.uniform(0.5, 1.5))  # Simulate work

                print(f"    [{client_id}] ✓ Completed {request_id}")

        except asyncio.CancelledError:
            print(f"  ⚠️ Client {client_id} disconnected")
            raise
        finally:
            print(f"  🔌 Client {client_id} session ended")

    async def start(self, num_clients: int = 5):
        """Start server and accept client connections"""
        print(f"\n🚀 MCP Server started (max clients: {self.max_clients})")

        # Simulate multiple clients connecting
        client_tasks = []
        for i in range(num_clients):
            client_id = f"client-{i+1:02d}"
            num_requests = random.randint(2, 4)

            # Each client handled concurrently
            task = asyncio.create_task(self.handle_client(client_id, num_requests))
            client_tasks.append(task)

        # Wait for all clients to finish
        await asyncio.gather(*client_tasks)

        print(f"\n✅ Server processed {self.request_count} total requests")

# Run example 2
print("\n▶ Simulating MCP server with 5 concurrent clients:")
server = MCPServer(max_clients=10)
asyncio.run(server.start(num_clients=5))

print("\n💡 KEY TAKEAWAY:")
print("   asyncio.create_task() spawns independent coroutines.")
print("   MCP servers use this to handle multiple clients simultaneously!")

# ==============================================================================
# EXAMPLE 3: Real-Time Data Streaming Pipeline
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 3: Real-Time Data Streaming Pipeline")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Process a continuous stream of data (logs, sensor data, user events).
Data arrives at different rates and needs processing without blocking
the pipeline. Classic use case for async streams.
""")

class DataStream:
    """Simulates a real-time data stream"""

    async def generate_events(self, num_events: int = 20):
        """Generate streaming events"""
        for i in range(num_events):
            await asyncio.sleep(random.uniform(0.1, 0.3))  # Irregular arrival

            event = {
                "id": f"evt-{i+1:03d}",
                "timestamp": datetime.now().isoformat(),
                "type": random.choice(["click", "purchase", "view", "error"]),
                "value": random.randint(1, 100)
            }

            yield event

class StreamProcessor:
    """Process streaming data with async pipeline"""

    def __init__(self):
        self.processed = 0
        self.total_value = 0

    async def process_event(self, event: Dict):
        """Process a single event"""
        print(f"  📊 Processing {event['id']}: {event['type']}")

        # Simulate processing time
        await asyncio.sleep(0.2)

        self.processed += 1
        self.total_value += event['value']

        # Simulate different processing based on type
        if event['type'] == 'error':
            print(f"     ⚠️ Error event detected! Value: {event['value']}")

    async def run_pipeline(self, stream: DataStream, num_events: int):
        """Run the streaming pipeline"""
        print("\n▶ Starting real-time data pipeline...")
        start = time.time()

        # Process stream with limited concurrency (buffer)
        tasks = []
        async for event in stream.generate_events(num_events):
            # Launch processing task
            task = asyncio.create_task(self.process_event(event))
            tasks.append(task)

            # Limit concurrent processing (buffer size)
            if len(tasks) >= 5:
                # Wait for oldest task to complete
                await tasks[0]
                tasks.pop(0)

        # Wait for remaining tasks
        if tasks:
            await asyncio.gather(*tasks)

        duration = time.time() - start

        print(f"\n✅ Pipeline complete!")
        print(f"   Processed: {self.processed} events")
        print(f"   Total value: {self.total_value}")
        print(f"   Time: {duration:.2f}s")
        print(f"   Throughput: {self.processed / duration:.1f} events/sec")

# Run example 3
stream = DataStream()
processor = StreamProcessor()
asyncio.run(processor.run_pipeline(stream, num_events=20))

print("\n💡 KEY TAKEAWAY:")
print("   Async generators (async for) handle streaming data efficiently.")
print("   Used in: Log processing, sensor data, real-time AI monitoring.")

# ==============================================================================
# EXAMPLE 4: Async File I/O for Large Dataset Processing
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 4: Async File I/O for Large Dataset Processing")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You need to process multiple large files for AI training data preparation.
Reading files one by one is slow. With async file I/O, read multiple files
concurrently to speed up data loading pipeline.
""")

async def read_file_async(file_path: str, file_size_mb: float) -> Dict:
    """Simulate reading a large file asynchronously"""
    print(f"  📂 Reading: {file_path} ({file_size_mb}MB)")
    start = time.time()

    # Simulate file read time (proportional to size)
    await asyncio.sleep(file_size_mb * 0.1)

    duration = time.time() - start

    # Simulate processing file content
    data = {
        "path": file_path,
        "size_mb": file_size_mb,
        "records": int(file_size_mb * 1000),  # Simulate records
        "read_time": duration
    }

    print(f"  ✓ Completed: {file_path} ({duration:.2f}s)")
    return data

async def process_dataset_parallel(file_paths: List[tuple]):
    """Process multiple dataset files in parallel"""
    print("\n▶ Processing dataset files in parallel...")
    start_time = time.time()

    # Read all files concurrently
    tasks = [read_file_async(path, size) for path, size in file_paths]
    results = await asyncio.gather(*tasks)

    total_time = time.time() - start_time

    # Calculate statistics
    total_records = sum(r['records'] for r in results)
    total_size = sum(r['size_mb'] for r in results)

    print(f"\n✅ Dataset loading complete!")
    print(f"   Files: {len(results)}")
    print(f"   Total size: {total_size:.1f}MB")
    print(f"   Total records: {total_records:,}")
    print(f"   Time: {total_time:.2f}s")
    print(f"   Speed: {total_size / total_time:.1f} MB/sec")

    # What would sequential time be?
    sequential_time = sum(r['read_time'] for r in results)
    print(f"\n⚡ {sequential_time / total_time:.1f}x faster than sequential!")

# Run example 4
dataset_files = [
    ("training_data_part1.csv", 5.2),
    ("training_data_part2.csv", 4.8),
    ("training_data_part3.csv", 6.1),
    ("validation_data.csv", 2.3),
    ("test_data.csv", 1.9),
]

asyncio.run(process_dataset_parallel(dataset_files))

print("\n💡 KEY TAKEAWAY:")
print("   Async file I/O speeds up data loading for ML/AI pipelines.")
print("   Use aiofiles library for real async file operations!")

# ==============================================================================
# EXAMPLE 5: WebSocket Server for Live AI Responses
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 5: WebSocket Server for Live AI Responses")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Build a WebSocket server that streams AI responses in real-time as they're
generated (like ChatGPT's streaming interface). Multiple users connect and
receive live token-by-token responses.
""")

class AIStreamingServer:
    """Simulates WebSocket server streaming AI responses"""

    def __init__(self):
        self.active_connections: Dict[str, bool] = {}

    async def generate_ai_response(self, prompt: str):
        """Simulate AI model generating response token by token"""
        response = f"AI response to: '{prompt}' - This is a simulated streaming response with multiple tokens being generated over time."

        # Stream tokens one by one
        tokens = response.split()
        for i, token in enumerate(tokens):
            await asyncio.sleep(0.1)  # Simulate generation time
            yield token

    async def handle_client_stream(self, client_id: str, prompt: str):
        """Handle a single client's streaming request"""
        print(f"\n  🌐 [{client_id}] Connected for prompt: '{prompt[:40]}...'")
        self.active_connections[client_id] = True

        try:
            full_response = []

            # Stream AI response to client
            async for token in self.generate_ai_response(prompt):
                if not self.active_connections.get(client_id):
                    print(f"  ⚠️ [{client_id}] Connection closed by client")
                    break

                # Send token to client
                full_response.append(token)
                print(f"     [{client_id}] → {token}")

            print(f"  ✓ [{client_id}] Stream complete ({len(full_response)} tokens)")

        except asyncio.CancelledError:
            print(f"  ⚠️ [{client_id}] Stream cancelled")
        finally:
            self.active_connections.pop(client_id, None)
            print(f"  🌐 [{client_id}] Disconnected")

    async def run_server(self, num_clients: int = 3):
        """Simulate multiple concurrent streaming sessions"""
        print("\n🚀 AI Streaming Server started")

        # Simulate multiple clients connecting
        prompts = [
            "Explain neural networks",
            "What is quantum computing",
            "How does async programming work"
        ]

        client_tasks = []
        for i in range(num_clients):
            client_id = f"ws-client-{i+1}"
            prompt = prompts[i % len(prompts)]

            task = asyncio.create_task(
                self.handle_client_stream(client_id, prompt)
            )
            client_tasks.append(task)

            # Stagger client connections
            await asyncio.sleep(0.3)

        # Wait for all streams to complete
        await asyncio.gather(*client_tasks)

        print("\n✅ All streaming sessions completed")

# Run example 5
streaming_server = AIStreamingServer()
asyncio.run(streaming_server.run_server(num_clients=3))

print("\n💡 KEY TAKEAWAY:")
print("   Async generators perfect for streaming AI responses.")
print("   Real-world use: ChatGPT, Claude, token-by-token streaming!")

# ==============================================================================
# EXAMPLE 6: Task Timeout and Cancellation Management
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 6: Task Timeout and Cancellation Management")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
API calls or AI model inference might hang or take too long. You need to
set timeouts and cancel tasks that exceed limits. Critical for production
systems to prevent resource exhaustion.
""")

async def slow_api_call(api_name: str, delay: float) -> str:
    """Simulate an API call that might be slow"""
    print(f"  🌐 Calling {api_name} (will take {delay:.1f}s)...")

    try:
        await asyncio.sleep(delay)
        return f"Response from {api_name}"
    except asyncio.CancelledError:
        print(f"  ⚠️ {api_name} was cancelled!")
        raise

async def call_with_timeout(api_name: str, delay: float, timeout: float):
    """Call API with timeout protection"""
    try:
        # wait_for will cancel the task if it exceeds timeout
        result = await asyncio.wait_for(
            slow_api_call(api_name, delay),
            timeout=timeout
        )
        print(f"  ✓ {api_name} succeeded: {result}")
        return result

    except asyncio.TimeoutError:
        print(f"  ❌ {api_name} timed out after {timeout}s!")
        return None

async def demo_timeout_management():
    """Demonstrate timeout handling for multiple APIs"""
    print("\n▶ Testing API calls with 2s timeout:")

    # These calls have different delays
    api_calls = [
        ("FastAPI", 0.5, 2.0),      # Will succeed
        ("MediumAPI", 1.5, 2.0),    # Will succeed
        ("SlowAPI", 3.0, 2.0),      # Will timeout!
        ("VerySlow", 5.0, 2.0),     # Will timeout!
    ]

    tasks = [
        call_with_timeout(name, delay, timeout)
        for name, delay, timeout in api_calls
    ]

    results = await asyncio.gather(*tasks)

    successful = sum(1 for r in results if r is not None)
    failed = len(results) - successful

    print(f"\n📊 Results: {successful} succeeded, {failed} timed out")

asyncio.run(demo_timeout_management())

print("\n💡 KEY TAKEAWAY:")
print("   asyncio.wait_for() enforces timeouts on any async operation.")
print("   Essential for: API calls, database queries, model inference!")

# ==============================================================================
# EXAMPLE 7: Producer-Consumer Pattern for AI Workloads
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 7: Producer-Consumer Pattern for AI Workloads")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You have a queue of AI tasks (image classification, text analysis, etc.).
Producers add tasks to queue, consumers (workers) process them. This pattern
efficiently distributes workload across multiple async workers.
""")

class AITaskQueue:
    """Queue for managing AI processing tasks"""

    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self.results = []

    async def producer(self, task_type: str, num_tasks: int):
        """Producer: Generate AI tasks"""
        print(f"\n🔄 Producer: Generating {num_tasks} {task_type} tasks...")

        for i in range(num_tasks):
            task = {
                "id": f"task-{i+1:03d}",
                "type": task_type,
                "data": f"input_data_{i+1}",
                "priority": random.randint(1, 5)
            }

            await self.queue.put(task)
            print(f"  ➕ Added: {task['id']} (priority: {task['priority']})")
            await asyncio.sleep(random.uniform(0.1, 0.3))

        print(f"  ✓ Producer finished ({num_tasks} tasks queued)")

    async def consumer(self, worker_id: int):
        """Consumer: Process AI tasks from queue"""
        print(f"  👷 Worker-{worker_id} started")

        while True:
            try:
                # Get task from queue (wait if empty)
                task = await asyncio.wait_for(self.queue.get(), timeout=3.0)

                print(f"    [Worker-{worker_id}] Processing {task['id']}...")

                # Simulate AI processing (higher priority = more time)
                processing_time = task['priority'] * 0.2
                await asyncio.sleep(processing_time)

                result = {
                    "task_id": task['id'],
                    "worker": worker_id,
                    "processing_time": processing_time,
                    "result": f"processed_{task['data']}"
                }

                self.results.append(result)
                print(f"    [Worker-{worker_id}] ✓ Completed {task['id']}")

                self.queue.task_done()

            except asyncio.TimeoutError:
                # No more tasks for 3 seconds, worker can stop
                print(f"  👷 Worker-{worker_id} stopping (no more tasks)")
                break

    async def run_pipeline(self, num_tasks: int, num_workers: int):
        """Run producer-consumer pipeline"""
        print(f"\n🏭 Starting AI workload pipeline")
        print(f"   Tasks: {num_tasks}")
        print(f"   Workers: {num_workers}")

        start_time = time.time()

        # Start producer
        producer_task = asyncio.create_task(
            self.producer("image_classification", num_tasks)
        )

        # Start multiple consumer workers
        consumer_tasks = [
            asyncio.create_task(self.consumer(i+1))
            for i in range(num_workers)
        ]

        # Wait for producer to finish
        await producer_task

        # Wait for all tasks to be processed
        await self.queue.join()

        # Wait for consumers to finish
        await asyncio.gather(*consumer_tasks)

        duration = time.time() - start_time

        print(f"\n✅ Pipeline complete!")
        print(f"   Total tasks: {len(self.results)}")
        print(f"   Total time: {duration:.2f}s")
        print(f"   Throughput: {len(self.results) / duration:.1f} tasks/sec")

# Run example 7
task_queue = AITaskQueue()
asyncio.run(task_queue.run_pipeline(num_tasks=15, num_workers=3))

print("\n💡 KEY TAKEAWAY:")
print("   asyncio.Queue() is perfect for producer-consumer patterns.")
print("   Use for: Task queues, job processing, AI batch inference!")

# ==============================================================================
# EXAMPLE 8: Async Database Connection Pool
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 8: Async Database Connection Pool")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
Your AI app queries a database frequently. Creating new connections is slow.
Use a connection pool: reuse connections across requests. Async pools handle
concurrent queries efficiently without blocking.
""")

class AsyncDatabasePool:
    """Simulates an async database connection pool"""

    def __init__(self, pool_size: int = 5):
        self.pool_size = pool_size
        self.connections: asyncio.Queue = None
        self.query_count = 0

    async def create_connection(self, conn_id: int):
        """Simulate creating a database connection"""
        print(f"    🔧 Creating connection-{conn_id}...")
        await asyncio.sleep(0.5)  # Connection startup time
        return f"connection-{conn_id}"

    async def initialize_pool(self):
        """Initialize connection pool"""
        print(f"\n🔧 Initializing connection pool (size: {self.pool_size})...")
        self.connections = asyncio.Queue(maxsize=self.pool_size)

        for i in range(self.pool_size):
            conn = await self.create_connection(i+1)
            await self.connections.put(conn)

        print(f"  ✓ Pool ready with {self.pool_size} connections")

    async def execute_query(self, query: str, query_id: int):
        """Execute a query using a connection from pool"""
        # Get connection from pool (wait if all busy)
        connection = await self.connections.get()

        try:
            print(f"  [{connection}] Executing query-{query_id}: {query}")

            # Simulate query execution
            await asyncio.sleep(random.uniform(0.3, 0.8))

            self.query_count += 1
            result = f"result_{query_id}"

            print(f"  [{connection}] ✓ Query-{query_id} complete")
            return result

        finally:
            # Return connection to pool
            await self.connections.put(connection)

    async def run_concurrent_queries(self, num_queries: int):
        """Run multiple queries concurrently using pool"""
        print(f"\n▶ Running {num_queries} concurrent queries...")
        start_time = time.time()

        queries = [
            f"SELECT * FROM users WHERE id = {i}"
            for i in range(num_queries)
        ]

        # All queries run concurrently, but limited by pool size
        tasks = [
            self.execute_query(query, i+1)
            for i, query in enumerate(queries)
        ]

        results = await asyncio.gather(*tasks)

        duration = time.time() - start_time

        print(f"\n✅ Queries complete!")
        print(f"   Total queries: {self.query_count}")
        print(f"   Time: {duration:.2f}s")
        print(f"   Throughput: {self.query_count / duration:.1f} queries/sec")
        print(f"   Pool efficiently reused {self.pool_size} connections!")

# Run example 8
db_pool = AsyncDatabasePool(pool_size=3)

async def demo_connection_pool():
    await db_pool.initialize_pool()
    await db_pool.run_concurrent_queries(num_queries=10)

asyncio.run(demo_connection_pool())

print("\n💡 KEY TAKEAWAY:")
print("   Connection pools reuse expensive resources (DB connections).")
print("   asyncio.Queue() manages the pool. Libraries: aiopg, aiomysql!")

# ==============================================================================
# EXAMPLE 9: Parallel AI Model Inference
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 9: Parallel AI Model Inference")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You need to run AI model inference on a batch of inputs. Each inference
takes time. Instead of processing sequentially, run multiple inferences
in parallel (up to GPU/CPU limits) to maximize throughput.
""")

class AIModel:
    """Simulates an AI model for inference"""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.inference_count = 0

    async def predict(self, input_data: str, batch_id: int) -> Dict:
        """Run model inference on input"""
        self.inference_count += 1
        inference_id = self.inference_count

        print(f"  🧠 [{self.model_name}] Inference-{inference_id} started (batch {batch_id})")

        # Simulate model forward pass (GPU computation)
        await asyncio.sleep(random.uniform(0.5, 1.0))

        result = {
            "inference_id": inference_id,
            "batch_id": batch_id,
            "input": input_data,
            "prediction": f"class_{random.randint(0, 9)}",
            "confidence": round(random.uniform(0.7, 0.99), 3),
            "model": self.model_name
        }

        print(f"  🧠 [{self.model_name}] Inference-{inference_id} ✓ " +
              f"({result['prediction']}, conf: {result['confidence']})")

        return result

async def batch_inference(model: AIModel, inputs: List[str], batch_size: int = 4):
    """Process inputs in concurrent batches"""
    print(f"\n▶ Running batch inference (batch_size: {batch_size})...")
    start_time = time.time()

    all_results = []

    # Process in batches (simulate GPU memory limits)
    for batch_num, i in enumerate(range(0, len(inputs), batch_size), 1):
        batch = inputs[i:i + batch_size]

        print(f"\n  📦 Processing batch {batch_num} ({len(batch)} items)...")

        # Run all items in batch concurrently
        batch_tasks = [
            model.predict(input_data, batch_num)
            for input_data in batch
        ]

        batch_results = await asyncio.gather(*batch_tasks)
        all_results.extend(batch_results)

        print(f"  ✓ Batch {batch_num} complete")

    duration = time.time() - start_time

    print(f"\n✅ All inference complete!")
    print(f"   Total inferences: {len(all_results)}")
    print(f"   Time: {duration:.2f}s")
    print(f"   Throughput: {len(all_results) / duration:.1f} inferences/sec")

    return all_results

# Run example 9
model = AIModel("ResNet-50")
test_inputs = [f"image_{i:03d}.jpg" for i in range(12)]

asyncio.run(batch_inference(model, test_inputs, batch_size=4))

print("\n💡 KEY TAKEAWAY:")
print("   Batch processing with controlled concurrency maximizes GPU/CPU usage.")
print("   Used in: Image classification, NLP, batch AI predictions!")

# ==============================================================================
# EXAMPLE 10: Async Rate Limiting for API Calls
# ==============================================================================

print("\n" + "=" * 80)
print("EXAMPLE 10: Async Rate Limiting for API Calls")
print("=" * 80)
print("""
REAL-WORLD SCENARIO:
You're calling an external API (OpenAI, Anthropic, etc.) that has rate limits:
- Max 10 requests per second
- Max 100 requests per minute

Need to enforce limits to avoid getting blocked, while still maintaining
high throughput within limits.
""")

class RateLimiter:
    """Async rate limiter using token bucket algorithm"""

    def __init__(self, rate: int, per: float):
        """
        rate: Number of tokens
        per: Time period in seconds
        """
        self.rate = rate
        self.per = per
        self.allowance = rate
        self.last_check = time.time()
        self._lock = asyncio.Lock()

    async def acquire(self):
        """Wait until rate limit allows next request"""
        async with self._lock:
            current = time.time()
            time_passed = current - self.last_check
            self.last_check = current

            # Replenish tokens based on time passed
            self.allowance += time_passed * (self.rate / self.per)

            if self.allowance > self.rate:
                self.allowance = self.rate

            # If no tokens available, wait
            if self.allowance < 1.0:
                sleep_time = (1.0 - self.allowance) * (self.per / self.rate)
                await asyncio.sleep(sleep_time)
                self.allowance = 0.0
            else:
                self.allowance -= 1.0

class RateLimitedAPIClient:
    """API client with rate limiting"""

    def __init__(self, requests_per_second: int = 5):
        self.limiter = RateLimiter(rate=requests_per_second, per=1.0)
        self.request_count = 0
        self.request_times = []

    async def call_api(self, endpoint: str, request_id: int):
        """Make rate-limited API call"""
        # Wait for rate limiter
        await self.limiter.acquire()

        self.request_count += 1
        current_time = time.time()
        self.request_times.append(current_time)

        print(f"  🌐 Request {request_id:02d} → {endpoint} (total: {self.request_count})")

        # Simulate API call
        await asyncio.sleep(0.1)

        return f"response_{request_id}"

    async def make_burst_requests(self, num_requests: int):
        """Attempt burst of requests (will be rate limited)"""
        print(f"\n▶ Attempting {num_requests} requests (rate limit: 5/sec)...")
        start_time = time.time()

        # Try to send all at once (limiter will control rate)
        tasks = [
            self.call_api(f"/endpoint/{i}", i+1)
            for i in range(num_requests)
        ]

        results = await asyncio.gather(*tasks)

        duration = time.time() - start_time

        # Calculate actual rate
        actual_rate = self.request_count / duration

        print(f"\n✅ Requests complete!")
        print(f"   Total: {self.request_count}")
        print(f"   Time: {duration:.2f}s")
        print(f"   Actual rate: {actual_rate:.1f} requests/sec")
        print(f"   ✓ Rate limiting enforced successfully!")

        # Show timing distribution
        if len(self.request_times) > 1:
            intervals = [
                self.request_times[i+1] - self.request_times[i]
                for i in range(len(self.request_times)-1)
            ]
            avg_interval = sum(intervals) / len(intervals)
            print(f"   Average interval: {avg_interval:.3f}s between requests")

# Run example 10
client = RateLimitedAPIClient(requests_per_second=5)
asyncio.run(client.make_burst_requests(num_requests=20))

print("\n💡 KEY TAKEAWAY:")
print("   Rate limiters prevent API abuse and ensure fair usage.")
print("   Essential for: OpenAI API, Anthropic API, any rate-limited service!")

# ==============================================================================
# FINAL SUMMARY
# ==============================================================================

print("\n" + "=" * 80)
print("🎉 ALL 10 ASYNCIO EXAMPLES COMPLETED!")
print("=" * 80)

summary = """
What You've Mastered:

1. ✅ Concurrent API Calls - Aggregate multiple service responses
2. ✅ MCP Server - Handle multiple client connections
3. ✅ Data Streaming - Process real-time event streams
4. ✅ Async File I/O - Parallel dataset loading
5. ✅ WebSocket Streaming - Live AI response streaming
6. ✅ Timeout Management - Cancel slow operations
7. ✅ Producer-Consumer - Distribute AI workloads
8. ✅ Connection Pool - Reuse database connections
9. ✅ Batch Inference - Parallel AI model predictions
10. ✅ Rate Limiting - Control API request rates

Key Patterns:
────────────────────────────────────────────────
• asyncio.gather()      → Run multiple tasks concurrently
• asyncio.create_task() → Spawn independent coroutines
• asyncio.Queue()       → Thread-safe task queues
• asyncio.wait_for()    → Enforce timeouts
• async for/yield       → Async generators for streaming
• async with           → Resource management

Real-World Applications:
────────────────────────────────────────────────
✓ MCP servers handling multiple clients
✓ AI model serving with batching
✓ Real-time data processing pipelines
✓ API aggregation for AI applications
✓ Database connection pooling
✓ Rate-limited API calls

Next: Move to CPython GIL examples! 🚀
"""

print(summary)

print("\n" + "=" * 80)
print("📝 PRACTICE SUGGESTIONS:")
print("=" * 80)
print("""
1. Modify the batch sizes and see performance changes
2. Add error handling to make examples more robust
3. Combine patterns (e.g., rate limiting + connection pool)
4. Build your own: Async web scraper, MCP client, or AI pipeline
5. Experiment with different concurrency limits

Ready for GIL? Run: 02_CPython_GIL_10_Examples.py
""")
