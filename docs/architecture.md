# Architecture Overview

MicroAPI is designed around explicit, layered abstractions.

The framework is structured to separate:
- Protocol handling (ASGI)
- Routing semantics
- Request and response lifecycles
- Error control flow
- Developer-facing ergonomics

## Core Layers

1. **ASGI Boundary**
   - Receives raw ASGI `scope`, `receive`, and `send`
   - Converts them into framework-owned abstractions

2. **Routing Layer**
   - Determines which handler should execute
   - Extracts path parameters
   - Does not mutate requests

3. **Application Layer**
   - Owns request mutation
   - Handles errors and response dispatch

4. **Handler Layer**
   - Pure business logic
   - Free from HTTP and ASGI concerns

This separation ensures correctness, testability, and extensibility.
