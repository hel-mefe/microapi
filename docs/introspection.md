# Endpoint Introspection

MicroAPI includes a built-in endpoint introspection page:

```
GET /endpoints
```


## Characteristics

- Reflects real runtime routing state
- Does not execute handlers
- Does not rely on schemas or decorators
- Owned entirely by the framework

This feature is intended for development and debugging.

