# MicroAPI

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/926e2c12-3826-400a-9b1a-343fb94fae3d" />


**MicroAPI** is a minimal, deterministic ASGI web framework built from first principles to explore the core architectural requirements of modern Python web frameworks.

It intentionally re-implements fundamental concepts found in frameworks like FastAPI and Starlette—routing, middleware, dependency injection, lifespan events—without shortcuts or hidden abstractions.

MicroAPI is not designed for feature parity.  
It is designed for **correctness, clarity, and architectural rigor**.

---

## Motivation

Modern Python web frameworks provide an excellent developer experience, but their internal complexity is often opaque.

MicroAPI exists to answer a single question:

> **What is the minimal, correct set of abstractions required to build a modern Python web framework?**

To explore this, MicroAPI:
- avoids implicit behavior
- makes lifecycles explicit
- enforces deterministic routing semantics
- treats dependency resolution as a first-class concern
- favors architectural correctness over convenience

---

## Design Principles

- **Deterministic behavior over magic**
- **Explicit lifecycles**
- **Minimal surface area**
- **Composable abstractions**
- **No global hidden state**
- **Testability as a core requirement**

---

## Core Features

### Routing
- Trie-based router with linear-time path matching
- Deterministic route precedence
- Static segments always take precedence over dynamic segments
- Explicit distinction between `404 Not Found` and `405 Method Not Allowed`
- HTTP method–aware routing
- Route decorators (`@get`, `@post`, etc.)

### Middleware
- Fully composable middleware pipeline
- Middleware can wrap, short-circuit, or observe request handling
- Predictable execution order
- Logging middleware
- CORS middleware with credentials support

### Dependency Injection
- Signature-based dependency resolution
- Request injection
- Dependency chaining
- Per-request dependency caching
- Async and async-generator dependencies
- Deterministic setup and teardown semantics
- Dependency overrides for testing

### Background Tasks
- Request-scoped background task system
- Tasks execute after the response is sent
- Supports synchronous and asynchronous callables
- Failures do not affect the response lifecycle

### Application Lifecycle
- ASGI lifespan support
- Startup and shutdown hooks
- Registry-aware lifecycle management

### Registry
- Centralized service registry
- App-scoped and request-scoped dependencies
- Integrated with dependency injection and lifespan events

### Introspection
- Built-in endpoint introspection page
- Lists registered routes and supported HTTP methods

---

## Routing Semantics

MicroAPI routing is deterministic and intentionally minimal:

- Paths are split into segments
- Static segments always take precedence over dynamic segments
- Dynamic segments capture values into `request.path_params`
- Route matching is linear in path depth

### Example precedence

/users/me      → static route
/users/{id}    → dynamic route

### Example usage

```python3
from microapi.app import MicroAPI
from microapi.background import BackgroundTasks

app = MicroAPI()

@app.get("/users/{id}")
async def get_user(request, background_tasks: BackgroundTasks):
    background_tasks.add(log_access, request.path)
    return {"user_id": request.path_params["id"]}
```

### Middleware Examples

```pythons
async def middleware(request, call_next):
    print("before")
    response = await call_next(request)
    print("after")
    return response

app.add_middleware(middleware)
```

### Dependency Injection Example

```python3
from microapi.dependencies import Depends

async def get_db():
    return "db-connection"

async def handler(db=Depends(get_db)):
    return db
```

### Background Tasks Example

```python3

```


### What MicroAPI Is Not (By Design)

MicroAPI intentionally does not include the following:

- Automatic request validation
- OpenAPI / schema generation
- Regex or wildcard routes
- Static file serving
- WebSockets

These features are deferred until core semantics are fully stabilized.

### Planned next steps:

- Route groups and prefixes
- Typed path and query parameters
- Static file support
- Background task scheduling
- Validation layer
- OpenAPI generation (later)

Each feature will be added incrementally without compromising existing abstractions.

### Development

#### Make tests
```make
make test
```

#### Lint
```
ruff check .
```

