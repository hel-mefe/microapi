# microapi

microapi is a minimal, FastAPI-inspired web framework built from scratch to understand how modern Python API frameworks work at a fundamental level.

The goal of this project is not feature parity with FastAPI, but clarity. microapi removes abstraction layers and hidden behavior so that every part of the request lifecycle can be read, understood, and modified.

This repository is both a learning tool and a reference implementation.

---

## Project Goals

microapi is designed with the following goals in mind:

- Provide a clear, minimal ASGI application implementation
- Demonstrate how routing works internally
- Expose the request and response lifecycle explicitly
- Avoid code generation, schemas, and magic decorators
- Keep the codebase small and readable end to end

Non-goals:

- Full FastAPI compatibility
- OpenAPI or Swagger generation
- Production-grade performance tuning
- Plugin ecosystems or extensive configuration systems

---

## Architecture Overview

The framework is intentionally split into small, focused modules.

microapi/
├── app.py # ASGI application and lifecycle
├── router.py # Route registration and matching
├── request.py # HTTP request abstraction
├── response.py # HTTP response abstraction
├── types.py # Core ASGI typing aliases
└── init.py



Each module represents a single responsibility in the request lifecycle.

---

## Minimal Example

```python
from microapi import MicroAPI

app = MicroAPI()

@app.get("/ping")
async def ping():
    return {"message": "pong"}

```

Run the application using any ASGI server

``` bash
uvicorn example:app
```

## ASGI Compliance

microapi is a valid ASGI application.

The main application object implements the ASGI callable interface:

```python
async def __call__(self, scope, receive, send)
```

Only HTTP scopes are handled at this stage. Other ASGI scope types such as websocket and lifespan are intentionally ignored in early iterations.


