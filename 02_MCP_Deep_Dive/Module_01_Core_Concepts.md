# Module 01: Core Concepts - How MCP Actually Works

## Deep Dive into MCP Architecture and Protocol Fundamentals

**Sources:**
- [Microsoft MCP for Beginners - Module 01](https://github.com/microsoft/mcp-for-beginners/blob/main/01-CoreConcepts/README.md)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Integration - Panaversity](https://ai-native.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows/mcp-integration)

---

## 🎯 Learning Objectives

By the end of this module, you will:

1. ✅ Understand the complete MCP architecture in depth
2. ✅ Know the three server primitives (Tools, Resources, Prompts)
3. ✅ Understand the three client primitives (Sampling, Elicitation, Logging)
4. ✅ Master the communication flow and message patterns
5. ✅ Understand transport layers (stdio, HTTP)
6. ✅ Know security principles and implementation
7. ✅ Be able to design your own MCP server

---

## 🏗️ MCP Architecture - Complete Picture

### **The Full System**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        MCP COMPLETE ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                          ┌──────────────┐                               │
│                          │   USER       │                               │
│                          │  (Human)     │                               │
│                          └──────┬───────┘                               │
│                                 │                                       │
│                                 ↓                                       │
│  ┌─────────────────────────────────────────────────────────┐           │
│  │                    MCP HOST                             │           │
│  │  (Claude Desktop, VS Code, Custom AI App)               │           │
│  ├─────────────────────────────────────────────────────────┤           │
│  │  Responsibilities:                                      │           │
│  │  • User interface and interaction                       │           │
│  │  • Manages MCP clients                                  │           │
│  │  • Orchestrates multiple servers                        │           │
│  │  • Handles permissions and security                     │           │
│  │  • Coordinates AI model (LLM)                           │           │
│  └─────────────┬───────────────────────────┬───────────────┘           │
│                │                           │                           │
│                ↓                           ↓                           │
│  ┌──────────────────────┐    ┌──────────────────────┐                 │
│  │   MCP CLIENT #1      │    │   MCP CLIENT #2      │                 │
│  │  (Protocol Handler)  │    │  (Protocol Handler)  │                 │
│  ├──────────────────────┤    ├──────────────────────┤                 │
│  │  • 1:1 with server   │    │  • 1:1 with server   │                 │
│  │  • Send requests     │    │  • Send requests     │                 │
│  │  • Receive responses │    │  • Receive responses │                 │
│  │  • Handle protocol   │    │  • Handle protocol   │                 │
│  └─────────┬────────────┘    └─────────┬────────────┘                 │
│            │                           │                               │
│            ↓                           ↓                               │
│  ┌──────────────────────┐    ┌──────────────────────┐                 │
│  │   MCP SERVER #1      │    │   MCP SERVER #2      │                 │
│  │  (File Operations)   │    │  (Database Ops)      │                 │
│  ├──────────────────────┤    ├──────────────────────┤                 │
│  │  Provides:           │    │  Provides:           │                 │
│  │  • Tools             │    │  • Tools             │                 │
│  │  • Resources         │    │  • Resources         │                 │
│  │  • Prompts           │    │  • Prompts           │                 │
│  └─────────┬────────────┘    └─────────┬────────────┘                 │
│            │                           │                               │
│            ↓                           ↓                               │
│      ┌──────────┐              ┌────────────┐                         │
│      │  FILES   │              │  DATABASE  │                         │
│      └──────────┘              └────────────┘                         │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

KEY RELATIONSHIPS:
• One Host can have multiple Clients
• One Client connects to exactly ONE Server
• One Server can be connected to by multiple Clients
• Each component has specific responsibilities
```

### **Component Responsibilities - Deep Dive**

#### **1. MCP HOST (The Orchestrator)**

```
┌─────────────────────────────────────────────────────────────┐
│                       MCP HOST                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RESPONSIBILITIES:                                          │
│  ├─ User Interface                                          │
│  │  • Display AI responses to user                          │
│  │  • Accept user input                                     │
│  │  • Show permission dialogs                               │
│  │                                                          │
│  ├─ Client Management                                       │
│  │  • Create and manage MCP clients                         │
│  │  • Route requests to correct client/server               │
│  │  • Aggregate responses from multiple servers             │
│  │                                                          │
│  ├─ AI Model Coordination                                   │
│  │  • Send context to AI model (LLM)                        │
│  │  • Receive AI's tool/resource requests                   │
│  │  • Provide tool results back to AI                       │
│  │                                                          │
│  └─ Security & Permissions                                  │
│     • Ask user for consent                                  │
│     • Enforce access controls                               │
│     • Audit log operations                                  │
│                                                             │
│  EXAMPLES:                                                  │
│  • Claude Desktop (official Anthropic app)                  │
│  • Claude Code (command-line interface)                     │
│  • VS Code with MCP extension                               │
│  • Custom AI applications you build                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### **2. MCP CLIENT (The Protocol Handler)**

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP CLIENT                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RESPONSIBILITIES:                                          │
│  ├─ Protocol Communication                                  │
│  │  • Speak JSON-RPC 2.0                                    │
│  │  • Format messages correctly                             │
│  │  • Handle message IDs                                    │
│  │                                                          │
│  ├─ Server Connection                                       │
│  │  • Establish connection to ONE server                    │
│  │  • Maintain persistent connection                        │
│  │  • Handle reconnection if needed                         │
│  │                                                          │
│  ├─ Request Management                                      │
│  │  • Send requests to server                               │
│  │  • Wait for responses                                    │
│  │  • Match responses to requests (by ID)                   │
│  │  • Handle timeouts                                       │
│  │                                                          │
│  └─ Capability Negotiation                                  │
│     • Discover what server offers                           │
│     • List available tools/resources/prompts                │
│     • Handle protocol version negotiation                   │
│                                                             │
│  RELATIONSHIP:                                              │
│  • 1:1 with Server (each client connects to ONE server)     │
│  • Many:1 with Host (host manages multiple clients)         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### **3. MCP SERVER (The Capability Provider)**

```
┌─────────────────────────────────────────────────────────────┐
│                      MCP SERVER                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  RESPONSIBILITIES:                                          │
│  ├─ Expose Capabilities                                     │
│  │  • Define available tools                                │
│  │  • Provide resources                                     │
│  │  • Offer prompt templates                                │
│  │                                                          │
│  ├─ Execute Operations                                      │
│  │  • Run tool functions                                    │
│  │  • Read resource data                                    │
│  │  • Fill prompt templates                                 │
│  │                                                          │
│  ├─ Validate & Respond                                      │
│  │  • Validate incoming requests                            │
│  │  • Execute safely                                        │
│  │  • Return structured responses                           │
│  │  • Handle errors gracefully                              │
│  │                                                          │
│  └─ Access Control                                          │
│     • Implement security boundaries                         │
│     • Validate permissions                                  │
│     • Log access for audit                                  │
│                                                             │
│  EXAMPLES:                                                  │
│  • File server (read/write files)                           │
│  • Database server (query database)                         │
│  • Web server (search, scrape)                              │
│  • Playwright (browser automation)                          │
│  • Context7 (documentation)                                 │
│  • Your custom servers!                                     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Three Server Primitives - In-Depth

### **Primitive 1: TOOLS (Actions)**

Tools are **executable functions** that AI can invoke to perform actions.

```
┌─────────────────────────────────────────────────────────────┐
│                         TOOLS                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT THEY ARE:                                             │
│  Functions the AI can execute to DO things                  │
│                                                             │
│  CHARACTERISTICS:                                           │
│  • Have side effects (modify state)                         │
│  • Execute actions (not just read)                          │
│  • Can change external systems                              │
│  • Require careful security                                 │
│                                                             │
│  STRUCTURE:                                                 │
│  ┌───────────────────────────────────────────────┐         │
│  │ Tool Definition                               │         │
│  ├───────────────────────────────────────────────┤         │
│  │ • name: "read_file"                           │         │
│  │ • description: "Read file contents..."        │         │
│  │ • inputSchema: {                              │         │
│  │     type: "object",                           │         │
│  │     properties: {                             │         │
│  │       path: {type: "string"}                  │         │
│  │     },                                        │         │
│  │     required: ["path"]                        │         │
│  │   }                                           │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  DISCOVERY & EXECUTION:                                     │
│  ┌───────────────────────────────────────────────┐         │
│  │ Step 1: AI lists tools                        │         │
│  │         Client → Server: tools/list           │         │
│  │         Server → Client: [tool1, tool2, ...]  │         │
│  │                                               │         │
│  │ Step 2: AI calls a tool                       │         │
│  │         Client → Server: tools/call           │         │
│  │         {                                     │         │
│  │           name: "read_file",                  │         │
│  │           arguments: {path: "/data/file.txt"} │         │
│  │         }                                     │         │
│  │                                               │         │
│  │ Step 3: Server executes & responds            │         │
│  │         Server → Client: {                    │         │
│  │           result: "file contents..."          │         │
│  │         }                                     │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  EXAMPLES:                                                  │
│  • read_file(path) → reads file                             │
│  • write_file(path, content) → writes file                  │
│  • execute_bash(command) → runs command                     │
│  • db_query(sql) → queries database                         │
│  • web_search(query) → searches web                         │
│  • send_email(to, subject, body) → sends email              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Primitive 2: RESOURCES (Data)**

Resources are **read-only data sources** that AI can access.

```
┌─────────────────────────────────────────────────────────────┐
│                       RESOURCES                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT THEY ARE:                                             │
│  Data that AI can READ (but not modify)                     │
│                                                             │
│  CHARACTERISTICS:                                           │
│  • Read-only (no side effects)                              │
│  • Provide context to AI                                    │
│  • URI-based identification                                 │
│  • Support different MIME types                             │
│                                                             │
│  URI SCHEME:                                                │
│  ┌───────────────────────────────────────────────┐         │
│  │ file:///path/to/file.txt                      │         │
│  │ db://database/table/record                    │         │
│  │ api://service/endpoint                        │         │
│  │ doc://documentation/page                      │         │
│  │ custom://your-scheme/resource                 │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  DISCOVERY & ACCESS:                                        │
│  ┌───────────────────────────────────────────────┐         │
│  │ Step 1: AI lists resources                    │         │
│  │         Client → Server: resources/list       │         │
│  │         Server → Client: [                    │         │
│  │           {uri: "file:///...", name: "..."},  │         │
│  │           {uri: "db://...", name: "..."}      │         │
│  │         ]                                     │         │
│  │                                               │         │
│  │ Step 2: AI reads a resource                   │         │
│  │         Client → Server: resources/read       │         │
│  │         {uri: "file:///data/config.json"}     │         │
│  │                                               │         │
│  │ Step 3: Server returns content                │         │
│  │         Server → Client: {                    │         │
│  │           contents: [{                        │         │
│  │             uri: "file:///data/config.json",  │         │
│  │             mimeType: "application/json",     │         │
│  │             text: "{...config data...}"       │         │
│  │           }]                                  │         │
│  │         }                                     │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  EXAMPLES:                                                  │
│  • File contents (configuration files, docs)                │
│  • Database records (user data, logs)                       │
│  • API responses (external data)                            │
│  • Documentation (help pages, manuals)                      │
│  • Live data feeds (metrics, status)                        │
│                                                             │
│  USE CASES:                                                 │
│  ✓ Provide context to AI (project docs, configs)           │
│  ✓ Give AI access to knowledge bases                        │
│  ✓ Share read-only data safely                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Primitive 3: PROMPTS (Templates)**

Prompts are **reusable conversation templates** that structure AI interactions.

```
┌─────────────────────────────────────────────────────────────┐
│                        PROMPTS                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT THEY ARE:                                             │
│  Pre-built templates for common AI tasks                    │
│                                                             │
│  CHARACTERISTICS:                                           │
│  • Reusable across conversations                            │
│  • Can have parameters (placeholders)                       │
│  • Provide consistent interactions                          │
│  • Encode best practices                                    │
│                                                             │
│  STRUCTURE:                                                 │
│  ┌───────────────────────────────────────────────┐         │
│  │ Prompt Template                               │         │
│  ├───────────────────────────────────────────────┤         │
│  │ name: "analyze_code"                          │         │
│  │ description: "Analyze code quality"           │         │
│  │ arguments: [                                  │         │
│  │   {name: "code", description: "..."},         │         │
│  │   {name: "language", description: "..."}      │         │
│  │ ]                                             │         │
│  │ template: "Analyze this {language} code..."   │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  DISCOVERY & USAGE:                                         │
│  ┌───────────────────────────────────────────────┐         │
│  │ Step 1: List available prompts                │         │
│  │         Client → Server: prompts/list         │         │
│  │         Server → Client: [prompt1, prompt2]   │         │
│  │                                               │         │
│  │ Step 2: Get a prompt with arguments           │         │
│  │         Client → Server: prompts/get          │         │
│  │         {                                     │         │
│  │           name: "analyze_code",               │         │
│  │           arguments: {                        │         │
│  │             code: "def foo()...",             │         │
│  │             language: "python"                │         │
│  │           }                                   │         │
│  │         }                                     │         │
│  │                                               │         │
│  │ Step 3: Server returns filled template        │         │
│  │         Server → Client: {                    │         │
│  │           description: "...",                 │         │
│  │           messages: [                         │         │
│  │             {role: "user", content: "..."}    │         │
│  │           ]                                   │         │
│  │         }                                     │         │
│  └───────────────────────────────────────────────┘         │
│                                                             │
│  EXAMPLES:                                                  │
│  • "Analyze this code for bugs"                             │
│  • "Write unit tests for this function"                     │
│  • "Explain this error message"                             │
│  • "Generate documentation for this API"                    │
│  • "Refactor this code"                                     │
│                                                             │
│  BENEFITS:                                                  │
│  ✓ Consistent quality (encode expertise)                    │
│  ✓ Fast workflows (pre-built templates)                     │
│  ✓ Best practices (domain experts create prompts)           │
│  ✓ Discoverability (users find helpful prompts)             │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Information Flow - Complete Request/Response Cycle

### **The Complete Journey of a Request**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                   COMPLETE MCP REQUEST FLOW                             │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: USER INPUT                                                    │
│  ───────────────────────────────────────────────────────────           │
│  👤 User types: "Read /data/sales.csv and analyze trends"              │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 2: HOST PROCESSING                                               │
│  ───────────────────────────────────────────────────────────           │
│  🖥️  Claude Desktop (Host):                                            │
│     1. Receives user input                                              │
│     2. Sends to AI model (Claude LLM)                                   │
│     3. AI determines: "I need to read a file"                           │
│     4. AI requests: use tool "read_file"                                │
│     5. Host asks user: "Allow read access to /data/sales.csv?"          │
│     6. User approves: "Yes"                                             │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 3: CLIENT SENDS REQUEST                                          │
│  ───────────────────────────────────────────────────────────           │
│  📤 MCP Client:                                                         │
│     Creates JSON-RPC request:                                           │
│     {                                                                   │
│       "jsonrpc": "2.0",                                                 │
│       "method": "tools/call",                                           │
│       "params": {                                                       │
│         "name": "read_file",                                            │
│         "arguments": {"path": "/data/sales.csv"}                        │
│       },                                                                │
│       "id": 1                                                           │
│     }                                                                   │
│                                                                         │
│     Sends via transport layer (stdio or HTTP) →                         │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 4: SERVER PROCESSES                                              │
│  ───────────────────────────────────────────────────────────           │
│  🖥️  File Server:                                                      │
│     1. Receives JSON-RPC message                                        │
│     2. Parses request                                                   │
│     3. Validates parameters                                             │
│     4. Checks permissions                                               │
│     5. Executes: reads /data/sales.csv                                  │
│     6. Reads file from filesystem                                       │
│     7. Formats response                                                 │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 5: SERVER RESPONDS                                               │
│  ───────────────────────────────────────────────────────────           │
│  📥 File Server:                                                        │
│     Creates JSON-RPC response:                                          │
│     {                                                                   │
│       "jsonrpc": "2.0",                                                 │
│       "result": {                                                       │
│         "content": "Date,Sales\n2024-01-01,1000\n...",                  │
│         "size": 2048,                                                   │
│         "mime_type": "text/csv"                                         │
│       },                                                                │
│       "id": 1                                                           │
│     }                                                                   │
│                                                                         │
│     Sends back via transport layer ←                                    │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 6: CLIENT RECEIVES                                               │
│  ───────────────────────────────────────────────────────────           │
│  📥 MCP Client:                                                         │
│     1. Receives response                                                │
│     2. Matches ID (request #1 → response #1)                            │
│     3. Validates response format                                        │
│     4. Extracts result data                                             │
│     5. Returns to Host                                                  │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 7: AI PROCESSES                                                  │
│  ───────────────────────────────────────────────────────────           │
│  🤖 Claude (LLM):                                                       │
│     1. Receives file contents                                           │
│     2. Parses CSV data                                                  │
│     3. Analyzes trends                                                  │
│     4. Generates response                                               │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 8: USER SEES RESULT                                              │
│  ───────────────────────────────────────────────────────────           │
│  👤 User sees:                                                          │
│     "I've analyzed your sales data. Here are the trends:                │
│      • January sales: $50,000 (20% increase)                            │
│      • Peak day: January 15th                                           │
│      • Trend: Upward growth of 15% month-over-month"                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

TOTAL TIME: ~500ms
COMPONENTS INVOLVED: 7 (User, Host, AI, Client, Server, Filesystem, User)
PROTOCOL MESSAGES: 2 (request + response)
USER EXPERIENCE: Seamless!
```

---

## 📡 Transport Layers - How Messages Travel

### **Transport 1: stdio (Standard Input/Output)**

```
┌─────────────────────────────────────────────────────────────┐
│                    STDIO TRANSPORT                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IT IS:                                                │
│  Communication via standard input/output streams            │
│                                                             │
│  HOW IT WORKS:                                              │
│                                                             │
│  ┌──────────────┐                    ┌──────────────┐      │
│  │   CLIENT     │                    │   SERVER     │      │
│  │   PROCESS    │                    │   PROCESS    │      │
│  ├──────────────┤                    ├──────────────┤      │
│  │              │  stdout (pipe)     │              │      │
│  │    writes    │ ────────────────→  │    reads     │      │
│  │    to pipe   │                    │  from stdin  │      │
│  │              │                    │              │      │
│  │              │  stdin (pipe)      │              │      │
│  │    reads     │ ←────────────────  │    writes    │      │
│  │  from pipe   │                    │  to stdout   │      │
│  └──────────────┘                    └──────────────┘      │
│                                                             │
│  CHARACTERISTICS:                                           │
│  ✅ Local communication (same machine)                      │
│  ✅ Secure (process isolation)                              │
│  ✅ Simple to implement                                     │
│  ✅ No network setup needed                                 │
│  ✅ RECOMMENDED for most use cases                          │
│                                                             │
│  MESSAGE FORMAT:                                            │
│  Each message is a single line of JSON:                     │
│  {"jsonrpc":"2.0","method":"tools/call","params":...}\n     │
│                                                             │
│  EXAMPLE SETUP:                                             │
│  ```python                                                  │
│  # Server runs as subprocess                                │
│  server_process = subprocess.Popen(                         │
│      ["python", "mcp_server.py"],                           │
│      stdin=subprocess.PIPE,                                 │
│      stdout=subprocess.PIPE                                 │
│  )                                                          │
│  ```                                                        │
│                                                             │
│  USE WHEN:                                                  │
│  • Local integrations (Claude Desktop, VS Code)             │
│  • Single machine setups                                    │
│  • Maximum security needed                                  │
│  • Simple deployment                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Transport 2: HTTP with Server-Sent Events (SSE)**

```
┌─────────────────────────────────────────────────────────────┐
│                  HTTP + SSE TRANSPORT                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IT IS:                                                │
│  Communication over HTTP with streaming support             │
│                                                             │
│  HOW IT WORKS:                                              │
│                                                             │
│  ┌──────────────┐                    ┌──────────────┐      │
│  │   CLIENT     │                    │   SERVER     │      │
│  │   (Web App)  │                    │  (HTTP API)  │      │
│  ├──────────────┤                    ├──────────────┤      │
│  │              │  HTTP POST         │              │      │
│  │  Sends       │ ────────────────→  │  Receives    │      │
│  │  request     │  /mcp/messages     │  processes   │      │
│  │              │                    │              │      │
│  │              │  SSE Stream        │              │      │
│  │  Receives    │ ←────────────────  │  Streams     │      │
│  │  responses   │  (continuous)      │  responses   │      │
│  └──────────────┘                    └──────────────┘      │
│                                                             │
│  CLIENT → SERVER (HTTP POST):                               │
│  POST /mcp/messages HTTP/1.1                                │
│  Content-Type: application/json                             │
│  Authorization: Bearer token...                             │
│                                                             │
│  {"jsonrpc":"2.0","method":"tools/call",...}                │
│                                                             │
│  SERVER → CLIENT (SSE):                                     │
│  HTTP/1.1 200 OK                                            │
│  Content-Type: text/event-stream                            │
│                                                             │
│  data: {"jsonrpc":"2.0","result":{...},"id":1}              │
│                                                             │
│  CHARACTERISTICS:                                           │
│  ✅ Remote communication (different machines)               │
│  ✅ Works over network/internet                             │
│  ✅ Supports authentication (OAuth, Bearer tokens)           │
│  ✅ Can stream long responses                               │
│  ✅ Firewall-friendly (uses standard HTTP)                  │
│                                                             │
│  AUTHENTICATION:                                            │
│  • OAuth 2.0 flow                                           │
│  • Bearer tokens                                            │
│  • API keys                                                 │
│                                                             │
│  USE WHEN:                                                  │
│  • Cloud-hosted servers                                     │
│  • Remote access needed                                     │
│  • Multiple clients from different locations                │
│  • Web-based applications                                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Transport Comparison**

| Feature | stdio | HTTP + SSE |
|---------|-------|-----------|
| **Location** | Local (same machine) | Local or Remote |
| **Security** | Process isolation | Needs auth (OAuth, tokens) |
| **Setup** | Very simple | More complex |
| **Performance** | Fast (no network) | Network latency |
| **Use Case** | Desktop apps, IDEs | Cloud services, web apps |
| **Recommended For** | Most use cases ⭐ | Remote scenarios |

---

## 🔐 Security Architecture

### **The Security Model**

```
┌─────────────────────────────────────────────────────────────┐
│                  MCP SECURITY LAYERS                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LAYER 1: USER CONSENT (Primary Security)                   │
│  ═══════════════════════════════════════════════            │
│                                                             │
│  Before ANY operation:                                      │
│  ┌─────────────────────────────────────────────┐           │
│  │ 1. AI requests action                       │           │
│  │    "I want to read /data/passwords.txt"     │           │
│  │                                             │           │
│  │ 2. Host shows dialog to user                │           │
│  │    ┌──────────────────────────────────┐    │           │
│  │    │  ⚠️  Permission Required         │    │           │
│  │    │                                  │    │           │
│  │    │  Claude wants to:                │    │           │
│  │    │  READ /data/passwords.txt        │    │           │
│  │    │                                  │    │           │
│  │    │  [Deny]          [Allow]         │    │           │
│  │    └──────────────────────────────────┘    │           │
│  │                                             │           │
│  │ 3. User must explicitly approve             │           │
│  │                                             │           │
│  │ 4. Only if approved, request proceeds       │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  LAYER 2: ACCESS CONTROL                                    │
│  ═══════════════════════════════════════════════            │
│                                                             │
│  Server enforces what it allows:                            │
│  ┌─────────────────────────────────────────────┐           │
│  │ Allowed Operations:                         │           │
│  │ ✅ Read files in /data directory            │           │
│  │ ✅ Write files in /output directory         │           │
│  │ ❌ Read files in /system directory          │           │
│  │ ❌ Execute system commands                  │           │
│  │ ❌ Delete any files                         │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  LAYER 3: TRANSPORT SECURITY                                │
│  ═══════════════════════════════════════════════            │
│                                                             │
│  stdio:                                                     │
│  • Process isolation                                        │
│  • Local-only (can't access remotely)                       │
│  • OS-level security                                        │
│                                                             │
│  HTTP:                                                      │
│  • TLS encryption (HTTPS)                                   │
│  • OAuth 2.0 authentication                                 │
│  • Bearer tokens                                            │
│  • API key validation                                       │
│                                                             │
│  LAYER 4: AUDIT LOGGING                                     │
│  ═══════════════════════════════════════════════            │
│                                                             │
│  Every operation logged:                                    │
│  • Who (user ID)                                            │
│  • What (tool/resource accessed)                            │
│  • When (timestamp)                                         │
│  • Result (success/failure)                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Security Principles**

```
┌────────────────────────────────────────────────────────────┐
│              MCP SECURITY PRINCIPLES                       │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  1. EXPLICIT CONSENT                                       │
│     Every operation requires user approval                 │
│     User understands what will happen                      │
│     No hidden actions                                      │
│                                                            │
│  2. LEAST PRIVILEGE                                        │
│     Servers get minimum permissions needed                 │
│     Fine-grained access control                            │
│     Deny by default                                        │
│                                                            │
│  3. DATA PRIVACY                                           │
│     User data stays under user control                     │
│     No unauthorized sharing                                │
│     Clear data handling policies                           │
│                                                            │
│  4. TRANSPARENCY                                           │
│     User sees what AI is doing                             │
│     Operations are auditable                               │
│     Clear error messages                                   │
│                                                            │
│  5. SAFE DEFAULTS                                          │
│     Secure by default configuration                        │
│     Opt-in for risky operations                            │
│     Sandboxed execution                                    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Protocol Lifecycle - Connection to Completion

### **Complete Session Lifecycle**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MCP SESSION LIFECYCLE                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  PHASE 1: INITIALIZATION                                                │
│  ═════════════════════════                                              │
│                                                                         │
│  1. Host starts                                                         │
│     └─ User launches Claude Desktop                                     │
│                                                                         │
│  2. Client creation                                                     │
│     └─ Host creates MCP client for each server                          │
│                                                                         │
│  3. Connection establishment                                            │
│     ┌─────────────────────────────────────────────┐                    │
│     │ Client → Server: "initialize" request       │                    │
│     │ {                                           │                    │
│     │   "method": "initialize",                   │                    │
│     │   "params": {                               │                    │
│     │     "protocolVersion": "2025-11-25",        │                    │
│     │     "capabilities": {                       │                    │
│     │       "tools": {},                          │                    │
│     │       "resources": {}                       │                    │
│     │     },                                      │                    │
│     │     "clientInfo": {                         │                    │
│     │       "name": "claude-desktop",             │                    │
│     │       "version": "1.0.0"                    │                    │
│     │     }                                       │                    │
│     │   }                                         │                    │
│     │ }                                           │                    │
│     └─────────────────────────────────────────────┘                    │
│                                                                         │
│  4. Server response                                                     │
│     ┌─────────────────────────────────────────────┐                    │
│     │ Server → Client: "initialize" response      │                    │
│     │ {                                           │                    │
│     │   "result": {                               │                    │
│     │     "protocolVersion": "2025-11-25",        │                    │
│     │     "capabilities": {                       │                    │
│     │       "tools": {},                          │                    │
│     │       "resources": {},                      │                    │
│     │       "prompts": {}                         │                    │
│     │     },                                      │                    │
│     │     "serverInfo": {                         │                    │
│     │       "name": "file-server",                │                    │
│     │       "version": "1.0.0"                    │                    │
│     │     }                                       │                    │
│     │   }                                         │                    │
│     │ }                                           │                    │
│     └─────────────────────────────────────────────┘                    │
│                                                                         │
│  5. Capability negotiation complete                                     │
│     └─ Both sides know what's supported                                │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 2: ACTIVE SESSION                                                │
│  ═══════════════════════                                                │
│                                                                         │
│  6. Discover capabilities                                               │
│     Client → Server: "tools/list"                                       │
│     Client → Server: "resources/list"                                   │
│     Client → Server: "prompts/list"                                     │
│                                                                         │
│  7. Use capabilities                                                    │
│     └─ Multiple request/response cycles                                │
│     └─ User asks, AI uses tools/resources                              │
│                                                                         │
│  ↓                                                                      │
│                                                                         │
│  PHASE 3: TERMINATION                                                   │
│  ════════════════════                                                   │
│                                                                         │
│  8. Cleanup                                                             │
│     └─ Client closes connection                                         │
│     └─ Server cleanup resources                                         │
│                                                                         │
│  9. Session end                                                         │
│     └─ User closes application                                          │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🎭 Client Primitives - Server Requesting From Client

While servers provide Tools/Resources/Prompts to AI, they can also REQUEST things from the client:

### **Client Primitive 1: SAMPLING**

```
┌─────────────────────────────────────────────────────────────┐
│                    SAMPLING                                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IT IS:                                                │
│  Server asks CLIENT to get an LLM response                  │
│                                                             │
│  WHY IT EXISTS:                                             │
│  Servers can use AI to generate content autonomously        │
│                                                             │
│  FLOW:                                                      │
│  ┌─────────────────────────────────────────────┐           │
│  │ 1. Server needs AI-generated content        │           │
│  │    (e.g., generate code, summarize text)    │           │
│  │                                             │           │
│  │ 2. Server → Client: "sampling/request"      │           │
│  │    {                                        │           │
│  │      "prompt": "Generate unit tests for...",│           │
│  │      "maxTokens": 1000                      │           │
│  │    }                                        │           │
│  │                                             │           │
│  │ 3. Client → AI Model (LLM)                  │           │
│  │    Sends prompt, gets response              │           │
│  │                                             │           │
│  │ 4. Client → Server: Response                │           │
│  │    {                                        │           │
│  │      "content": "Generated content..."      │           │
│  │    }                                        │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  EXAMPLE USE CASE:                                          │
│  Server: "Code Review Tool"                                 │
│  1. Receives code to review                                 │
│  2. Uses sampling to ask AI: "What are issues in this code?"│
│  3. Gets AI analysis                                        │
│  4. Returns formatted review                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Client Primitive 2: ELICITATION**

```
┌─────────────────────────────────────────────────────────────┐
│                    ELICITATION                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IT IS:                                                │
│  Server asks CLIENT to get user input                       │
│                                                             │
│  WHY IT EXISTS:                                             │
│  Servers can interact with user for confirmations/input     │
│                                                             │
│  FLOW:                                                      │
│  ┌─────────────────────────────────────────────┐           │
│  │ 1. Server needs user input                  │           │
│  │    (e.g., confirm deletion, choose option)  │           │
│  │                                             │           │
│  │ 2. Server → Client: "elicitation/request"   │           │
│  │    {                                        │           │
│  │      "message": "Confirm delete file.txt?", │           │
│  │      "options": ["Yes", "No"]               │           │
│  │    }                                        │           │
│  │                                             │           │
│  │ 3. Client → User                            │           │
│  │    Shows dialog: "Confirm delete file.txt?" │           │
│  │    [Yes] [No]                               │           │
│  │                                             │           │
│  │ 4. User responds: "Yes"                     │           │
│  │                                             │           │
│  │ 5. Client → Server: Response                │           │
│  │    {"choice": "Yes"}                        │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  EXAMPLE USE CASE:                                          │
│  Server: "File Management Tool"                             │
│  1. User asks to "clean up old files"                       │
│  2. Server finds 50 old files                               │
│  3. Uses elicitation: "Delete these 50 files?"              │
│  4. User confirms                                           │
│  5. Server proceeds with deletion                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Client Primitive 3: LOGGING**

```
┌─────────────────────────────────────────────────────────────┐
│                      LOGGING                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IT IS:                                                │
│  Server sends log messages to CLIENT for debugging          │
│                                                             │
│  WHY IT EXISTS:                                             │
│  Debug and monitor server operations                        │
│                                                             │
│  LOG LEVELS:                                                │
│  • DEBUG - Detailed diagnostic info                         │
│  • INFO - General informational messages                    │
│  • WARN - Warning messages                                  │
│  • ERROR - Error messages                                   │
│                                                             │
│  FLOW:                                                      │
│  ┌─────────────────────────────────────────────┐           │
│  │ Server → Client: "logging/message"          │           │
│  │ {                                           │           │
│  │   "level": "info",                          │           │
│  │   "data": "Processing file.txt...",         │           │
│  │   "timestamp": "2024-01-15T10:30:00Z"       │           │
│  │ }                                           │           │
│  │                                             │           │
│  │ Client displays in console/UI               │           │
│  └─────────────────────────────────────────────┘           │
│                                                             │
│  BENEFIT:                                                   │
│  Users/developers see what server is doing                  │
│  Helps debug issues                                         │
│  Transparency in operations                                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📨 Message Format - JSON-RPC 2.0

### **Why JSON-RPC 2.0?**

```
BENEFITS OF JSON-RPC 2.0:
──────────────────────────────────────────────────────
✅ Standardized (widely adopted)
✅ Simple (JSON is easy to parse)
✅ Language-agnostic (works with any language)
✅ Request-response matching (via ID)
✅ Error handling built-in
✅ Supports notifications (no response needed)
```

### **Message Types**

#### **Request Message**

```json
{
  "jsonrpc": "2.0",           // Protocol version (required)
  "method": "tools/call",     // Method to invoke (required)
  "params": {                 // Parameters (optional)
    "name": "read_file",
    "arguments": {
      "path": "/data/file.txt"
    }
  },
  "id": 1                     // Request ID (required for requests)
}
```

**Visual Breakdown:**

```
┌──────────────────────────────────────────────────────────┐
│                  REQUEST MESSAGE                         │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  jsonrpc: "2.0"                                          │
│  ↳ Tells receiver: "I'm speaking JSON-RPC 2.0"           │
│                                                          │
│  method: "tools/call"                                    │
│  ↳ What to do: call a tool                               │
│  ↳ Other methods: resources/read, prompts/get            │
│                                                          │
│  params: {...}                                           │
│  ↳ Method-specific parameters                            │
│  ↳ For tools/call: name + arguments                      │
│                                                          │
│  id: 1                                                   │
│  ↳ Unique identifier for THIS request                    │
│  ↳ Response will have same ID                            │
│  ↳ Allows async request/response matching                │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

#### **Success Response Message**

```json
{
  "jsonrpc": "2.0",           // Protocol version
  "result": {                 // The result (if successful)
    "content": "File contents here...",
    "size": 1024
  },
  "id": 1                     // Matches request ID
}
```

#### **Error Response Message**

```json
{
  "jsonrpc": "2.0",           // Protocol version
  "error": {                  // Error (if failed)
    "code": -32600,           // Error code
    "message": "Invalid request",  // Human-readable message
    "data": {                 // Additional error details
      "details": "Missing required parameter 'path'"
    }
  },
  "id": 1                     // Matches request ID
}
```

#### **Notification (No Response Expected)**

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/progress",
  "params": {
    "progress": 75,
    "message": "Processing..."
  }
  // No 'id' field - notification doesn't need response
}
```

---

## 🔀 Complete Workflow Diagrams

### **Workflow 1: Tool Execution (End-to-End)**

```
USER ASKS QUESTION
        ↓
┌───────────────────────────────────────────────────────────────┐
│                                                               │
│  👤 User: "Read sales.csv and calculate total revenue"       │
│        ↓                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ HOST (Claude Desktop)                               │    │
│  │ 1. Receives user input                               │    │
│  │ 2. Sends to AI model: "User wants to analyze sales"  │    │
│  └─────────────────────────────────────────────────────┘    │
│        ↓                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ AI MODEL (Claude LLM)                                │    │
│  │ 3. Thinks: "I need to read sales.csv file"           │    │
│  │ 4. Decides: Use tool "read_file"                     │    │
│  │ 5. Returns to Host: "Call read_file with path=/..."  │    │
│  └─────────────────────────────────────────────────────┘    │
│        ↓                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ HOST                                                 │    │
│  │ 6. Shows permission dialog:                          │    │
│  │    "Allow read access to sales.csv? [Yes] [No]"      │    │
│  └─────────────────────────────────────────────────────┘    │
│        ↓                                                      │
│  👤 User clicks: [Yes]                                       │
│        ↓                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ CLIENT                                               │    │
│  │ 7. Creates JSON-RPC request:                         │    │
│  │    {                                                 │    │
│  │      "method": "tools/call",                         │    │
│  │      "params": {                                     │    │
│  │        "name": "read_file",                          │    │
│  │        "arguments": {"path": "sales.csv"}            │    │
│  │      },                                              │    │
│  │      "id": 1                                         │    │
│  │    }                                                 │    │
│  │ 8. Sends via stdio/HTTP to server                    │    │
│  └─────────────────────────────────────────────────────┘    │
│        ↓                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ SERVER (File Operations)                             │    │
│  │ 9. Receives request                                  │    │
│  │ 10. Validates: tool exists? params valid?            │    │
│  │ 11. Checks permissions: can read sales.csv?          │    │
│  │ 12. Executes: reads file from filesystem             │    │
│  │     Content: "Date,Revenue\n2024-01-01,5000\n..."    │    │
│  │ 13. Creates response:                                │    │
│  │     {                                                │    │
│  │       "result": {                                    │    │
│  │         "content": "Date,Revenue\n...",              │    │
│  │         "size": 2048                                 │    │
│  │       },                                             │    │
│  │       "id": 1                                        │    │
│  │     }                                                │    │
│  │ 14. Sends response back                              │    │
│  └─────────────────────────────────────────────────────┘    │
│        ↓                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ CLIENT                                               │    │
│  │ 15. Receives response                                │    │
│  │ 16. Matches ID (request #1 → response #1)            │    │
│  │ 17. Returns result to Host                           │    │
│  └─────────────────────────────────────────────────────┘    │
│        ↓                                                      │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ AI MODEL                                             │    │
│  │ 18. Receives file contents                           │    │
│  │ 19. Analyzes CSV data                                │    │
│  │ 20. Calculates: Total revenue = $125,000             │    │
│  │ 21. Generates response                               │    │
│  └─────────────────────────────────────────────────────┘    │
│        ↓                                                      │
│  👤 User sees: "Total revenue from sales.csv is $125,000"    │
│                                                               │
└───────────────────────────────────────────────────────────────┘

STEPS: 21
TIME: ~500ms
COMPONENTS: 6 (User, Host, AI, Client, Server, Filesystem)
MESSAGES: 2 (request + response)
```

### **Workflow 2: Resource Access (Read-Only Data)**

```
┌───────────────────────────────────────────────────────────────┐
│          RESOURCE ACCESS WORKFLOW                             │
├───────────────────────────────────────────────────────────────┤
│                                                               │
│  1. Discovery Phase                                           │
│  ─────────────────────────────────────────────────────        │
│                                                               │
│     Client → Server: "resources/list"                         │
│                                                               │
│     Server → Client: [                                        │
│       {                                                       │
│         "uri": "file:///docs/api.md",                         │
│         "name": "API Documentation",                          │
│         "description": "API endpoint docs",                   │
│         "mimeType": "text/markdown"                           │
│       },                                                      │
│       {                                                       │
│         "uri": "db://products/table",                         │
│         "name": "Product Database",                           │
│         "description": "All products",                        │
│         "mimeType": "application/json"                        │
│       }                                                       │
│     ]                                                         │
│                                                               │
│     AI now knows: 2 resources available                      │
│                                                               │
│  ↓                                                            │
│                                                               │
│  2. Access Phase                                              │
│  ─────────────────────────────────────────────────────        │
│                                                               │
│     AI decides: "I need the API docs"                         │
│                                                               │
│     Client → Server: "resources/read"                         │
│     {                                                         │
│       "uri": "file:///docs/api.md"                            │
│     }                                                         │
│                                                               │
│     Server → Client: {                                        │
│       "contents": [{                                          │
│         "uri": "file:///docs/api.md",                         │
│         "mimeType": "text/markdown",                          │
│         "text": "# API Docs\n\n## Endpoints..."              │
│       }]                                                      │
│     }                                                         │
│                                                               │
│     AI receives: Full documentation text                     │
│                                                               │
│  ↓                                                            │
│                                                               │
│  3. AI Uses Resource                                          │
│  ─────────────────────────────────────────────────────        │
│                                                               │
│     AI reads docs, understands API                            │
│     AI answers user's question using this knowledge           │
│                                                               │
│     User sees: Accurate answer based on actual docs!          │
│                                                               │
└───────────────────────────────────────────────────────────────┘

KEY DIFFERENCE FROM TOOLS:
• Resources = READ-ONLY (no modifications)
• Tools = ACTIONS (can change things)
```

---

## 🔗 Protocol Methods - Complete Reference

### **Server → Client Methods**

```
┌─────────────────────────────────────────────────────────────┐
│              SERVER PROVIDES TO CLIENT                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  INITIALIZATION:                                            │
│  • initialize - Capability negotiation                      │
│  • ping - Health check                                      │
│                                                             │
│  TOOLS:                                                     │
│  • tools/list - List all available tools                    │
│  • tools/call - Execute a specific tool                     │
│                                                             │
│  RESOURCES:                                                 │
│  • resources/list - List all available resources            │
│  • resources/read - Read specific resource(s)               │
│  • resources/subscribe - Watch for changes (optional)       │
│  • resources/unsubscribe - Stop watching (optional)         │
│                                                             │
│  PROMPTS:                                                   │
│  • prompts/list - List all available prompts                │
│  • prompts/get - Get filled prompt template                 │
│                                                             │
│  NOTIFICATIONS (Server → Client, no response):              │
│  • notifications/resources/list_changed - Resources updated │
│  • notifications/tools/list_changed - Tools updated         │
│  • notifications/prompts/list_changed - Prompts updated     │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### **Client → Server Methods (Client Primitives)**

```
┌─────────────────────────────────────────────────────────────┐
│              CLIENT PROVIDES TO SERVER                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  SAMPLING:                                                  │
│  • sampling/createMessage - Request AI completion           │
│                                                             │
│  ELICITATION:                                               │
│  • elicitation/request - Ask user for input                 │
│                                                             │
│  LOGGING:                                                   │
│  • logging/setLevel - Set log level                         │
│  • (Server sends via notifications/message)                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Takeaways - Module 01

```
┌────────────────────────────────────────────────────────────┐
│                  REMEMBER THIS!                            │
├────────────────────────────────────────────────────────────┤
│                                                            │
│  ARCHITECTURE:                                             │
│  • Host (UI) → Client (protocol) → Server (capabilities)   │
│  • One Host, multiple Clients, multiple Servers            │
│  • Each Client connects to exactly ONE Server              │
│                                                            │
│  SERVER PRIMITIVES (Server provides to AI):                │
│  • Tools - Actions (read_file, web_search)                 │
│  • Resources - Data (docs, configs, DB records)            │
│  • Prompts - Templates (reusable conversations)            │
│                                                            │
│  CLIENT PRIMITIVES (Server requests from Client):          │
│  • Sampling - Get AI completions                           │
│  • Elicitation - Get user input                            │
│  • Logging - Send debug messages                           │
│                                                            │
│  TRANSPORT:                                                │
│  • stdio - Local (recommended for most cases)              │
│  • HTTP + SSE - Remote (for cloud/web scenarios)           │
│                                                            │
│  MESSAGE FORMAT:                                           │
│  • JSON-RPC 2.0                                            │
│  • Request: method + params + id                           │
│  • Response: result/error + id                             │
│                                                            │
│  SECURITY:                                                 │
│  • User consent required                                   │
│  • Access control in servers                               │
│  • Transport encryption                                    │
│  • Audit logging                                           │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## 🔗 Sources

- [Microsoft MCP for Beginners - Module 01](https://github.com/microsoft/mcp-for-beginners/blob/main/01-CoreConcepts/README.md)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Integration - Panaversity](https://ai-native.panaversity.org/docs/AI-Tool-Landscape/claude-code-features-and-workflows/mcp-integration)

---

## ✅ Self-Check Questions

Test your understanding:

1. **What are the three server primitives?**
   <details><summary>Answer</summary>Tools (actions), Resources (data), Prompts (templates)</details>

2. **What's the difference between Tools and Resources?**
   <details><summary>Answer</summary>Tools can modify/execute (side effects); Resources are read-only data</details>

3. **What transport layer is recommended for local use?**
   <details><summary>Answer</summary>stdio (standard input/output)</details>

4. **What protocol does MCP use for messages?**
   <details><summary>Answer</summary>JSON-RPC 2.0</details>

5. **What are the three client primitives?**
   <details><summary>Answer</summary>Sampling (get AI completion), Elicitation (get user input), Logging (debug messages)</details>

6. **Why does every message have an 'id' field?**
   <details><summary>Answer</summary>To match requests with their responses (async request/response pairing)</details>

---

## 🚀 Next Steps

**You Now Understand:**
- ✅ Complete MCP architecture (Host, Client, Server)
- ✅ All six primitives (3 server + 3 client)
- ✅ Message format (JSON-RPC 2.0)
- ✅ Transport layers (stdio, HTTP)
- ✅ Complete request/response flow
- ✅ Security model

**Ready For:**
→ **Module 02: Security** - Deep dive into security implementation
→ **Module 03: Building Your First Server** - Hands-on coding!

**Practice File:**
→ **Module_01_Core_Concepts.py** - Code examples for all concepts

---

**Congratulations!** You've mastered MCP core concepts! 🎉
