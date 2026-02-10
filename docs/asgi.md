# ASGI Integration

MicroAPI is fully compliant with the ASGI specification.

## Responsibilities

- Accept incoming HTTP connections via ASGI
- Translate ASGI primitives into framework abstractions
- Maintain a strict boundary between ASGI and application logic

## Design Principles

- ASGI details are confined to the request implementation
- Handlers never interact with `scope`, `receive`, or `send`
- ASGI lifecycle events are handled at the framework level

This approach prevents protocol leakage into business logic.
