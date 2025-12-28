# Module 11: MCP Server Hands-On Labs - Production-Ready Implementation

## 13 Progressive Labs: From Setup to Production Deployment

**Sources:**
- [Microsoft MCP for Beginners - Module 11](https://github.com/microsoft/mcp-for-beginners/tree/main/11-MCPServerHandsOnLabs)

---

## 🎯 Module Overview

This is the **CULMINATING MODULE** - a complete 13-lab hands-on learning path that teaches you to build **production-ready MCP servers** with PostgreSQL integration using a **retail analytics use case**.

### **What You'll Build**

```
┌─────────────────────────────────────────────────────────────────────────┐
│              RETAIL ANALYTICS MCP SERVER                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  DOMAIN: Retail Store Analytics                                         │
│                                                                         │
│  DATABASE: PostgreSQL                                                   │
│  ├─ Tables: products, sales, customers, inventory                       │
│  ├─ Row-Level Security (multi-tenancy)                                  │
│  └─ Vector embeddings for semantic search                               │
│                                                                         │
│  MCP CAPABILITIES:                                                      │
│  ├─ Tools:                                                              │
│  │   • Query sales data                                                 │
│  │   • Search products (semantic)                                       │
│  │   • Generate analytics reports                                       │
│  │   • Manage inventory                                                 │
│  │                                                                      │
│  ├─ Resources:                                                          │
│  │   • Product catalog                                                  │
│  │   • Sales history                                                    │
│  │   • Customer segments                                                │
│  │                                                                      │
│  └─ Prompts:                                                            │
│      • "Analyze sales trends"                                           │
│      • "Generate monthly report"                                        │
│      • "Forecast inventory needs"                                       │
│                                                                         │
│  DEPLOYMENT:                                                            │
│  ├─ Docker containerization                                             │
│  ├─ Azure Container Apps                                                │
│  ├─ Application Insights monitoring                                     │
│  └─ Production-grade security                                           │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 📚 The 13 Labs - Complete Learning Path

```
┌─────────────────────────────────────────────────────────────────────────┐
│                  13 HANDS-ON LABS PROGRESSION                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  FOUNDATION (Labs 00-03)                                                │
│  ═══════════════════════════════════════                                │
│                                                                         │
│  Lab 00: Introduction & Retail Analytics Context                        │
│  ├─ Understand the business problem                                     │
│  ├─ Learn domain model                                                  │
│  └─ Set expectations                                                    │
│                                                                         │
│  Lab 01: Core Architecture & Patterns                                   │
│  ├─ MCP server architecture                                             │
│  ├─ FastMCP framework introduction                                      │
│  └─ Project structure                                                   │
│                                                                         │
│  Lab 02: Security & Multi-Tenancy                                       │
│  ├─ Row-Level Security (RLS) in PostgreSQL                              │
│  ├─ Multi-tenant data isolation                                         │
│  └─ Security policies                                                   │
│                                                                         │
│  Lab 03: Development Environment Setup                                  │
│  ├─ Install PostgreSQL                                                  │
│  ├─ Set up Python environment                                           │
│  ├─ Configure FastMCP                                                   │
│  └─ Verify installation                                                 │
│                                                                         │
│  ────────────────────────────────────────────────────────────           │
│                                                                         │
│  IMPLEMENTATION (Labs 04-07)                                            │
│  ═══════════════════════════════════                                    │
│                                                                         │
│  Lab 04: PostgreSQL Database Design                                     │
│  ├─ Create retail database schema                                       │
│  ├─ Products, sales, customers, inventory tables                        │
│  ├─ Relationships and constraints                                       │
│  ├─ Indexes for performance                                             │
│  └─ Sample data population                                              │
│                                                                         │
│  Lab 05: FastMCP Server Implementation                                  │
│  ├─ Initialize FastMCP server                                           │
│  ├─ Configure database connection                                       │
│  ├─ Implement connection pooling                                        │
│  └─ Error handling patterns                                             │
│                                                                         │
│  Lab 06: Tool Development                                               │
│  ├─ query_sales tool                                                    │
│  ├─ search_products tool                                                │
│  ├─ get_inventory tool                                                  │
│  ├─ generate_report tool                                                │
│  └─ Schema introspection                                                │
│                                                                         │
│  Lab 07: Vector Embeddings with Azure OpenAI                            │
│  ├─ Product description embeddings                                      │
│  ├─ Semantic search implementation                                      │
│  ├─ Vector similarity queries                                           │
│  └─ Integration with pgvector extension                                 │
│                                                                         │
│  ────────────────────────────────────────────────────────────           │
│                                                                         │
│  QUALITY & DEPLOYMENT (Labs 08-10)                                      │
│  ═══════════════════════════════════════                                │
│                                                                         │
│  Lab 08: Testing & Debugging                                            │
│  ├─ Unit tests for tools                                                │
│  ├─ Integration tests with database                                     │
│  ├─ Debugging strategies                                                │
│  └─ Performance testing                                                 │
│                                                                         │
│  Lab 09: VS Code Integration                                            │
│  ├─ Configure MCP server in VS Code                                     │
│  ├─ Use with GitHub Copilot                                             │
│  └─ Development workflow                                                │
│                                                                         │
│  Lab 10: Deployment Strategies                                          │
│  ├─ Docker containerization                                             │
│  │   • Dockerfile creation                                              │
│  │   • Multi-stage builds                                               │
│  │   • Container optimization                                           │
│  │                                                                      │
│  ├─ Azure Container Apps deployment                                     │
│  │   • Resource creation                                                │
│  │   • Environment configuration                                        │
│  │   • Scaling policies                                                 │
│  │                                                                      │
│  └─ CI/CD pipeline                                                      │
│      • GitHub Actions                                                   │
│      • Automated testing                                                │
│      • Automated deployment                                             │
│                                                                         │
│  ────────────────────────────────────────────────────────────           │
│                                                                         │
│  PRODUCTION OPERATIONS (Labs 11-12)                                     │
│  ═══════════════════════════════════════                                │
│                                                                         │
│  Lab 11: Application Insights & Monitoring                              │
│  ├─ Telemetry integration                                               │
│  ├─ Custom metrics                                                      │
│  ├─ Distributed tracing                                                 │
│  ├─ Alert configuration                                                 │
│  └─ Dashboard creation                                                  │
│                                                                         │
│  Lab 12: Performance Optimization & Hardening                           │
│  ├─ Query optimization                                                  │
│  ├─ Connection pooling tuning                                           │
│  ├─ Caching strategies                                                  │
│  ├─ Rate limiting implementation                                        │
│  ├─ Security hardening                                                  │
│  └─ Load testing                                                        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🗄️ Database Architecture - PostgreSQL with RLS

### **Retail Analytics Schema**

```
┌─────────────────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE ARCHITECTURE                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  TABLES:                                                                │
│  ┌────────────────────────────────────────────────────────┐            │
│  │ products                                               │            │
│  │ ├─ id (PRIMARY KEY)                                    │            │
│  │ ├─ name                                                │            │
│  │ ├─ description                                         │            │
│  │ ├─ price                                               │            │
│  │ ├─ category                                            │            │
│  │ ├─ tenant_id (for multi-tenancy)                       │            │
│  │ └─ embedding (vector for semantic search)              │            │
│  └────────────────────────────────────────────────────────┘            │
│                                                                         │
│  ┌────────────────────────────────────────────────────────┐            │
│  │ sales                                                  │            │
│  │ ├─ id (PRIMARY KEY)                                    │            │
│  │ ├─ product_id (FOREIGN KEY → products)                 │            │
│  │ ├─ customer_id (FOREIGN KEY → customers)               │            │
│  │ ├─ quantity                                            │            │
│  │ ├─ total_amount                                        │            │
│  │ ├─ sale_date                                           │            │
│  │ └─ tenant_id                                           │            │
│  └────────────────────────────────────────────────────────┘            │
│                                                                         │
│  ┌────────────────────────────────────────────────────────┐            │
│  │ customers                                              │            │
│  │ ├─ id (PRIMARY KEY)                                    │            │
│  │ ├─ name                                                │            │
│  │ ├─ email                                               │            │
│  │ ├─ segment (VIP, Regular, New)                         │            │
│  │ └─ tenant_id                                           │            │
│  └────────────────────────────────────────────────────────┘            │
│                                                                         │
│  ROW-LEVEL SECURITY (RLS):                                              │
│  ┌────────────────────────────────────────────────────────┐            │
│  │ CREATE POLICY tenant_isolation ON products            │            │
│  │ FOR ALL                                               │            │
│  │ USING (tenant_id = current_setting('app.tenant_id')) │            │
│  │                                                       │            │
│  │ Result: Users only see their tenant's data!           │            │
│  └────────────────────────────────────────────────────────┘            │
│                                                                         │
│  VECTOR SEARCH (pgvector):                                              │
│  ┌────────────────────────────────────────────────────────┐            │
│  │ -- Semantic product search                             │            │
│  │ SELECT name, description                               │            │
│  │ FROM products                                          │            │
│  │ ORDER BY embedding <-> query_embedding                 │            │
│  │ LIMIT 10;                                              │            │
│  │                                                       │            │
│  │ Finds similar products by meaning, not keywords!       │            │
│  └────────────────────────────────────────────────────────┘            │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ FastMCP Framework

### **What is FastMCP?**

```
┌─────────────────────────────────────────────────────────────┐
│              FASTMCP FRAMEWORK                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  WHAT IT IS:                                                │
│  Python framework for building MCP servers quickly          │
│  Like FastAPI but for MCP!                                  │
│                                                             │
│  KEY FEATURES:                                              │
│  ├─ Decorator-based tool registration                       │
│  ├─ Automatic schema generation                             │
│  ├─ Built-in validation                                     │
│  ├─ Database integration helpers                            │
│  └─ Development server with hot reload                      │
│                                                             │
│  BENEFITS:                                                  │
│  ✅ Rapid development                                        │
│  ✅ Less boilerplate                                         │
│  ✅ Type-safe decorators                                     │
│  ✅ Excellent for prototypes → production                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Complete Lab Progression

### **The 13-Lab Journey**

```
LAB 00: Introduction ✅
└─ Understand retail analytics use case

LAB 01: Architecture ✅
└─ Learn MCP + FastMCP architecture

LAB 02: Security & Multi-Tenancy ✅
└─ Implement Row-Level Security

LAB 03: Environment Setup ✅
└─ Install all dependencies

LAB 04: Database Design ✅
└─ Create PostgreSQL schema

LAB 05: FastMCP Server ✅
└─ Build basic server structure

LAB 06: Tool Development ✅
└─ Implement query and analytics tools

LAB 07: Vector Embeddings ✅
└─ Add semantic search with Azure OpenAI

LAB 08: Testing & Debugging ✅
└─ Comprehensive test suite

LAB 09: VS Code Integration ✅
└─ Use server in development

LAB 10: Deployment ✅
└─ Docker + Azure Container Apps

LAB 11: Monitoring ✅
└─ Application Insights integration

LAB 12: Optimization ✅
└─ Performance tuning and hardening
```

---

## 🔗 Sources

- [Module 11: Hands-On Labs](https://github.com/microsoft/mcp-for-beginners/tree/main/11-MCPServerHandsOnLabs)

---

## ✅ Key Takeaways

```
WHAT YOU BUILD:
• Production-ready MCP server
• PostgreSQL integration
• Multi-tenant security
• Semantic search
• Cloud deployment
• Full monitoring

SKILLS GAINED:
• End-to-end MCP development
• Database integration patterns
• Vector embeddings
• Docker & Azure
• Production operations
```

---

**🎉 MODULE 11 COMPLETES THE MCP CURRICULUM!** 🎓
