# Request and Response Model

MicroAPI defines framework-owned request and response abstractions.

## Request

The request object:
- Is created once per incoming request
- Wraps ASGI data
- Exposes method, path, headers, query params, and path params
- Lazily reads the request body

## Response

Responses are explicit objects:
- `TextResponse`
- `JSONResponse`

Handlers may return:
- A response object
- A dictionary (converted to JSON)
- A string (converted to text)

This ensures consistent HTTP semantics.
