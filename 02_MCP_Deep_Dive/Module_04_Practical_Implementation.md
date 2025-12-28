# Module 04: Practical Implementation - Real-World Techniques

## SDK Usage, Debugging, Testing, and Advanced Patterns

**Sources:**
- [Microsoft MCP for Beginners - Module 04](https://github.com/microsoft/mcp-for-beginners/tree/main/04-PracticalImplementation)
- [MCP SDK Documentation](https://modelcontextprotocol.io/sdks)

---

## 🎯 Learning Objectives

1. ✅ Master MCP SDKs across multiple languages
2. ✅ Debug MCP servers and clients effectively
3. ✅ Implement comprehensive testing strategies
4. ✅ Use reusable prompt templates
5. ✅ Build production-quality code

---

## 📚 MCP SDK Ecosystem

### **Official SDKs**

```
┌─────────────────────────────────────────────────────────────┐
│              OFFICIAL MCP SDKs                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TypeScript/JavaScript                                      │
│  ├─ Package: @modelcontextprotocol/sdk                      │
│  ├─ Best for: Node.js servers, web apps                     │
│  └─ Maturity: ⭐⭐⭐⭐⭐ Most mature                        │
│                                                             │
│  Python                                                     │
│  ├─ Package: mcp                                            │
│  ├─ Best for: Data science, ML integration                  │
│  └─ Maturity: ⭐⭐⭐⭐ Very stable                          │
│                                                             │
│  .NET/C#                                                    │
│  ├─ Package: ModelContextProtocol                           │
│  ├─ Best for: Enterprise apps, Azure                        │
│  └─ Maturity: ⭐⭐⭐⭐ Production-ready                     │
│                                                             │
│  Java                                                       │
│  ├─ Package: org.modelcontextprotocol                       │
│  ├─ Best for: Spring Boot, enterprise                       │
│  └─ Maturity: ⭐⭐⭐ Stable                                 │
│                                                             │
│  Rust                                                       │
│  ├─ Package: mcp-sdk                                        │
│  ├─ Best for: High-performance servers                      │
│  └─ Maturity: ⭐⭐⭐ Growing                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🐛 Debugging MCP Systems

### **Common Issues & Solutions**

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    DEBUGGING GUIDE                                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ISSUE 1: Connection Fails                                              │
│  ═══════════════════════════════════════                                │
│  Symptoms: Client can't connect to server                               │
│                                                                         │
│  Debug Steps:                                                           │
│  ✓ Check server is running (ps aux | grep server)                       │
│  ✓ Verify transport type matches (stdio vs HTTP)                        │
│  ✓ Check file paths/ports are correct                                   │
│  ✓ Look at stderr for server errors                                     │
│  ✓ Enable debug logging on both sides                                   │
│                                                                         │
│  ISSUE 2: Tool Execution Fails                                          │
│  ═══════════════════════════════════════                                │
│  Symptoms: tools/call returns error                                     │
│                                                                         │
│  Debug Steps:                                                           │
│  ✓ Validate parameters match schema                                     │
│  ✓ Check tool handler for exceptions                                    │
│  ✓ Verify tool is registered (tools/list)                               │
│  ✓ Add console.log/print in handler                                     │
│  ✓ Use Inspector to test tool directly                                  │
│                                                                         │
│  ISSUE 3: Messages Not Being Received                                   │
│  ═══════════════════════════════════════                                │
│  Symptoms: Request sent but no response                                 │
│                                                                         │
│  Debug Steps:                                                           │
│  ✓ Check message format (valid JSON-RPC 2.0?)                           │
│  ✓ Verify newline after each message (stdio)                            │
│  ✓ Confirm ID matching (request ID == response ID)                      │
│  ✓ Check for infinite loops in handlers                                 │
│  ✓ Enable protocol-level logging                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### **Debugging Workflow**

```
Problem Occurs
       ↓
┌──────────────────────────────────────────┐
│ 1. Enable Debug Logging                  │
│    Set LOG_LEVEL=debug                   │
└──────────┬───────────────────────────────┘
           ↓
┌──────────────────────────────────────────┐
│ 2. Use MCP Inspector                     │
│    Test server in isolation              │
└──────────┬───────────────────────────────┘
           ↓
┌──────────────────────────────────────────┐
│ 3. Check Message Format                  │
│    Validate JSON-RPC compliance          │
└──────────┬───────────────────────────────┘
           ↓
┌──────────────────────────────────────────┐
│ 4. Add Logging to Handlers               │
│    console.log() / print() liberally     │
└──────────┬───────────────────────────────┘
           ↓
┌──────────────────────────────────────────┐
│ 5. Test Edge Cases                       │
│    Null values, missing params, etc.     │
└──────────┬───────────────────────────────┘
           ↓
    Problem Solved!
```

---

## 🔗 Sources

- [Microsoft MCP for Beginners - Module 04](https://github.com/microsoft/mcp-for-beginners/tree/main/04-PracticalImplementation)

---

## ✅ Key Takeaways

```
PRACTICAL SKILLS:
• Use official SDKs for your language
• Debug with Inspector tool
• Comprehensive testing (unit, integration, E2E)
• Production-ready error handling
• Reusable prompt templates
```

---

**Next: Module 05 - Advanced Topics!** 🚀
