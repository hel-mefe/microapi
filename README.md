# MicroAPI

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/1c21e035-5a76-4754-9b40-7fadc8627ffe" />

# MicroAPI

**MicroAPI** is a minimal, FastAPI-inspired **ASGI web framework built from scratch**, designed to explore and demonstrate the core mechanics of modern Python web frameworks with an emphasis on **explicit architecture, deterministic routing, and extensibility**.

Rather than focusing on ergonomics first, MicroAPI prioritizes **semantic correctness**, clean separation of concerns, and a foundation that can scale to advanced features such as middleware, dependency injection, CORS, and lifecycle events.

---

## Goals & Philosophy

MicroAPI is built around a few core principles:

- **Explicit over implicit**
  No hidden magic or reflection-heavy behavior. Control flow is visible and intentional.

- **Semantics before ergonomics**
  Core behavior (routing, request flow, errors) is locked down before adding decorators or syntactic sugar.

- **Deterministic behavior**
  Routing, error handling, and request mutation follow strict, predictable rules.

- **Framework-owned HTTP semantics**
  Business logic is isolated from transport and protocol concerns.

This project is both an educational deep dive and a serious foundation for a minimal framework.

---

## Key Features

- **ASGI-compliant core**
  Built directly on the ASGI specification, with a clean application boundary.

- **Trie-based HTTP router**
  Custom router implementation using a Trie data structure, enabling:
  - Linear-time route matching (O(path length))
  - Static and parameterized paths (`/users/{id}`)
  - Deterministic precedence rules (static > dynamic)

- **Request & Response Abstractions**
  - Clean request object decoupled from ASGI internals
  - Framework-owned response types (`TextResponse`, `JSONResponse`)
  - Explicit body handling and header management

- **HTTP Error Control Flow**
  - Dedicated `HTTPException` model
  - Clear separation between business errors and HTTP responses
  - Centralized error handling in the framework layer

- **Endpoint Introspection**
  - Built-in endpoint discovery at `GET /__endpoints__`
  - Reflects real runtime routing state
  - No schemas, decorators, or reflection hacks

- **Extensible Architecture**
  Designed from the ground up to support:
  - Middleware
  - Dependency Injection
  - CORS handling
  - Application lifespan events (startup / shutdown)

---

## Project Structure



---

## Example Usage

```python
from microapi.router.trie import TrieRouter
from microapi.app import MicroAPI

router = TrieRouter()

async def hello(request):
    return {"message": "Hello, world!"}

async def get_user(request):
    return {"user_id": request.path_params["id"]}

router.add("GET", "/", hello)
router.add("GET", "/users/{id}", get_user)

app = MicroAPI(router)
```

Run with

```
make run
```

## Routing Semantics

MicroAPI routing is deterministic and intentionally minimal:

- Paths are split into segments
- Static segments always take precedence over dynamic segments
- Dynamic segments capture values into `request.path_params`
- Route matching is linear in path depth

### Example precedence

`/users/me`: static route
`users/{id}`: dynamic route
`/users/me` will always match before `/users/{id}`.

---

## What MicroAPI Is Not (Yet)

MicroAPI intentionally does **not** include the following (by design):

- Decorators like `@get`, `@post`
- Dependency Injection
- Automatic request validation
- OpenAPI / schema generation
- Regex or wildcard (`/*`) routes

These features are planned **after core semantics are fully stabilized**.

---

## Roadmap

Planned next steps:

- HTTP method semantics (405 vs 404)
- Middleware system (enables CORS, logging, authentication)
- Application lifespan events
- Route decorators (`@get`, `@post`, etc.)
- Dependency Injection
- Typed path and query parameters
- Static file support

Each feature will be added **without compromising existing abstractions**.

---

## Why This Project Exists

MicroAPI exists to answer a simple question:

> What does it actually take to build a modern Python web framework correctly?

This project explores that question by re-implementing core ideas from FastAPI and Starlette—**without shortcuts**, and with a strong focus on **architecture, correctness, and long-term maintainability**.

---

## License

MIT License
