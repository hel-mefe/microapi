# Error Handling

MicroAPI uses exceptions as **intentional control flow** for HTTP errors.

## HTTPException

Framework-defined HTTP exceptions carry:
- Status code
- Error detail
- Optional headers

Handlers raise exceptions instead of constructing responses.

## Benefits

- Clean separation of business logic and HTTP semantics
- Centralized error handling
- Predictable behavior under failure

Unexpected exceptions are allowed to bubble up during development.
