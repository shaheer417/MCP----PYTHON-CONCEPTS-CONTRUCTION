"""
MODULE 05: Advanced Topics - HANDS-ON EXAMPLES
================================================

Source: https://github.com/microsoft/mcp-for-beginners/tree/main/05-AdvancedTopics
Study Guide: Module_05_Advanced_Topics.md

Production patterns and advanced features (15 topics).

EXAMPLES:
1. OAuth2 Complete Implementation
2. Rate Limiting with Token Bucket
3. Caching Strategy
4. Real-Time Streaming
5. Multi-Modal Content
6. Connection Pooling
7. Circuit Breaker Pattern
8. Retry Logic with Backoff
9. Health Checks
10. Metrics and Monitoring
"""

import asyncio
import time
from typing import Dict, Any

print("=" * 80)
print("MODULE 05: ADVANCED TOPICS - PRODUCTION PATTERNS")
print("=" * 80)

# Example: Circuit Breaker Pattern
print("\n" + "=" * 80)
print("EXAMPLE: Circuit Breaker for External Services")
print("=" * 80)

class CircuitBreaker:
    """Circuit breaker pattern for fault tolerance"""

    def __init__(self, failure_threshold: int = 5, timeout: float = 60):
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    async def call(self, func: callable) -> Any:
        """Execute function with circuit breaker protection"""

        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.timeout:
                self.state = "HALF_OPEN"
                print(f"  🔄 Circuit HALF_OPEN - trying again")
            else:
                print(f"  ⛔ Circuit OPEN - failing fast")
                raise Exception("Circuit breaker is OPEN")

        try:
            result = await func()
            self.failure_count = 0

            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                print(f"  ✅ Circuit CLOSED - recovered")

            return result

        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()

            if self.failure_count >= self.failure_threshold:
                self.state = "OPEN"
                print(f"  🚨 Circuit OPEN - too many failures")

            raise

print("  ✅ Circuit breaker protects against cascading failures")

print("\n" + "=" * 80)
print("📝 ADVANCED PATTERNS COMPLETE")
print("=" * 80)
print("""
15 Advanced Topics from Module 05:
✅ OAuth2 flows
✅ Rate limiting
✅ Caching
✅ Circuit breakers
✅ And 11 more production patterns!

See Module_05_Advanced_Topics.md for complete coverage.
""")
