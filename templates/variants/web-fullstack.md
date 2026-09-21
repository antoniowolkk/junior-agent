# Variant: Full-stack web (React + API backend)

Paste these into the matching sections of `AGENTS.md`. Everything else in the base file stays as-is.

## 3. Stack and layout

- **Frontend:** React + TypeScript, Vite, Vitest + Testing Library
- **Backend:** <FastAPI (Python) | Express/Nest (Node) | ...>, tests with <pytest | vitest>
- **Database:** <PostgreSQL> via <ORM>
- **Package manager:** <pnpm | npm> (web), <uv | poetry | pip> (backend)

```
/web       React app — UI only, no business rules
  src/features/<name>/   one folder per feature: component, hooks, tests
  src/lib/               shared helpers
/backend   API — all business rules and validation live here
  <app>/routes/          HTTP layer, thin
  <app>/services/        business logic
  <app>/models/          data models / schema
  tests/
/docs      prd.md, adr/
```

## 4. Commands

| Purpose | Command |
| --- | --- |
| Install (web) | `pnpm install` |
| Install (backend) | `<...>` |
| Dev (web) | `pnpm dev` |
| Dev (backend) | `<...>` |
| Test (web) | `pnpm test` |
| Test (backend) | `<...>` |
| Lint | `pnpm lint` |
| Type check | `pnpm typecheck` |
| Build | `pnpm build` |

Both suites must pass before a change is done.

## 5. Conventions — additions

- The API contract is the boundary. Change it in the backend first, with a test, then update the frontend.
- Validate every input server-side. Client-side validation is UX only and is never the security boundary.
- Never trust data from the client. Never put a secret in frontend code — anything in `/web` is public.
- Loading, empty, and error states are required for every screen that fetches data.
- No business rules duplicated in the frontend.

## 7. Guardrails — additions

- Never run a database migration. Write it, then stop and ask.
- Never change auth, session, CORS, or permission logic without an ADR and explicit approval.
- Never add a third-party script or analytics tag to the frontend.
