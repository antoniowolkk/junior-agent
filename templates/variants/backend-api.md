# Variant: Backend / API service

Paste these into the matching sections of `AGENTS.md`.

## 3. Stack and layout

- **Language / framework:** <FastAPI (Python) | Express/Nest (Node) | Go | ...>
- **Tests:** <pytest | vitest | go test>
- **Database:** <PostgreSQL> via <ORM>
- **Auth:** <JWT | session | provider>

```
<app>/
  routes/     HTTP layer — parse, authorize, delegate. Thin.
  services/   business logic. Testable without HTTP.
  models/     schema / data access
  migrations/
tests/        unit + integration
docs/         prd.md, adr/
```

## 4. Commands

| Purpose | Command |
| --- | --- |
| Install | `<...>` |
| Run dev | `<...>` |
| Test all | `<...>` |
| Test one file | `<...>` |
| Lint | `<...>` |
| Type check | `<...>` |
| New migration | `<...>` |

## 5. Conventions — additions

- Validate and sanitize every input at the boundary. Reject unknown fields.
- Parameterized queries only — never string-build SQL.
- Every endpoint states its auth requirement explicitly. Default is authenticated.
- Errors: return a safe message to the client, log the detail server-side. Never leak stack traces, SQL, or internal paths in a response.
- Never log secrets, tokens, passwords, or personal data.
- Every endpoint gets a test for the success path, the invalid-input path, and the unauthorized path.

## 7. Guardrails — additions

- Never run a migration against any database. Write it and stop.
- Never modify auth, permissions, rate limiting, or CORS without an ADR and explicit approval.
- Never point the app at a non-local database.
- Never widen a permission, disable a check, or add a bypass to make a test pass.
