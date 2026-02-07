# Routing

MicroAPI uses a custom **Trie-based router** for HTTP path matching.

## Why a Trie?

- Linear-time route matching (O(path depth))
- Deterministic behavior
- Clear precedence rules
- Efficient memory layout

## Supported Route Types

- Static paths: `/users`, `/health`
- Parameterized paths: `/users/{id}`

## Precedence Rules

Static segments always take precedence over dynamic segments.

/users/me -> static
/users/{id} -> dynamic


This ensures predictable routing behavior.

## What Is Intentionally Excluded

- Regex routes
- Wildcard (`/*`) routes

These are deferred to middleware or future extensions.


