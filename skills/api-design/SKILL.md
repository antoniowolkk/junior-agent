---
name: api-design
description: Design a public or network contract (REST, GraphQL, or RPC endpoints, request and response types, error format) before implementing it, and keep it backward compatible. Use for /api-design, "design this endpoint", "add an API", "is this a breaking change", "version this API", "pagination", "idempotency", "OpenAPI", or any change other programs will call over the wire.
---

# API Design

Write the contract first, review it as a contract, then implement against it. Once a client depends on a field, a status code, or an error shape, changing it costs every caller. The design is the part that is hard to undo.

Subordinate to `AGENTS.md` section 7. Where this says proceed and the guardrails say ask, ask.

**Scope.** This skill covers what crosses the network. Internal types and module boundaries belong to **architect**. Changing a live database schema belongs to **migrate**. Auditing an existing API for holes belongs to **threat-model**. Route there instead of repeating them here.

## 1. Ground

- Find the existing API conventions in this repo: URL style, casing, error body, pagination, auth middleware. Cite file:line. A new endpoint that matches the house style beats a better one that does not.
- List the callers: browser, mobile app, third party, internal service. Mobile and third-party clients cannot be redeployed with you, so their old versions live for months.
- If a spec exists (OpenAPI, GraphQL SDL, `.proto`), it is the source of truth. Edit it before code.

## 2. Model the resources

Write the caller's requests first, as literal examples, then derive the shape.

| Decide | Default |
| --- | --- |
| Nouns | Resources are nouns, plural collections: `/orders`, `/orders/{id}`. Actions that are not CRUD become a sub-resource or a custom method (`POST /orders/{id}:cancel`), not a verb in a query string. |
| Identifiers | Opaque strings. Never expose auto-increment ids if enumeration matters. |
| Casing | One style for fields across the whole API. Match what exists. |
| Timestamps | RFC 3339 strings in UTC. Money as integer minor units plus a currency code. |
| Nullable vs absent | Decide per field and write it in the spec. Clients treat them differently. |
| Data model | Only fields a caller needs. Every field you expose is one you must keep. |

## 3. Fix the cross-cutting rules

1. **Errors.** One body shape for every failure, e.g. RFC 9457 problem details (`type`, `title`, `status`, `detail`). A stable machine-readable code, never a parsed message. 4xx means the caller can fix it; 5xx means you must.
2. **Pagination.** Every list endpoint paginates from day one, cursor-based by default (`page_size`, `page_token`, `next_page_token`). Adding pagination later is a breaking change.
3. **Idempotency.** `GET`, `PUT`, `DELETE` must be safe to retry. A `POST` that creates or charges accepts an `Idempotency-Key` header and returns the first result on replay.
4. **Validation at the trust boundary.** Validate type, length, range, and enum membership on the server for every input, including path and query params. Reject unknown fields or ignore them, and say which in the spec.
5. **Auth on every endpoint.** Each operation names its required scope or role, and checks the specific object belongs to the caller. "Public" is an explicit annotation, not a missing one.
6. **Limits.** Max page size, max body size, rate limit, and what status the caller gets when hit.

## 4. Breaking or not

Classify every change to an existing contract before writing it. Label the classification measured (a contract test or schema diff tool says so), inferred, or guess.

| Change | Breaking? |
| --- | --- |
| Add an optional request field, a response field, a new endpoint | No, if clients ignore unknown fields. Check that they do. |
| Add a required request field | Yes |
| Remove or rename a field, endpoint, or enum value | Yes |
| Change a field's type, format, or meaning | Yes, even when the type name stays the same |
| Add an enum value to a response | Often. Strict clients crash on unknown values. |
| Tighten validation, change a status code or error code | Yes |
| Change default sort order or page size | Yes, in practice |

A breaking change ships as a new version (`/v2`, a new GraphQL field, a new proto message) alongside the old one, with a deprecation date. Removing the old version is irreversible and needs a yes from the human per section 7.

## 5. Contract-first, then tests

1. Write or update the spec. Run its linter if the repo has one.
2. Sketch handlers that return `not implemented`, wired to the spec's routes.
3. Write contract tests: each example request from phase 2 against the running server, asserting status, body shape against the schema, and the error body for at least one bad input and one unauthorized call.
4. Implement until they pass. Report them as measured; a spec you only read is inferred.

## Output

The spec diff, the example requests and responses, the breaking-change table filled in for this change, and the contract test command with its result. Add an ADR (per `AGENTS.md` section 8) for a new version, a new auth scheme, or a new error format.

## Failure modes

| Smell | What it means |
| --- | --- |
| Handler written before the spec | The code is now the contract by accident. |
| Error bodies differ between endpoints | Clients write one parser per endpoint. Pick one shape. |
| List endpoint with no limit | It works until the table grows. |
| "Nobody uses that field" | Guess. Check access logs or clients before calling it unused. |
| Auth checked in the UI only | No server check means no check. Run **threat-model**. |

## Sources

- IBM Bob Modes catalog, modes api-builder/schema-builder — https://bob-modes.2azhe5jwptg4.au-syd.codeengine.appdomain.cloud (used as inspiration; no text reused)
- [Google API Improvement Proposals](https://google.aip.dev): resource naming (AIP-122), custom methods (AIP-136), pagination (AIP-158), compatibility (AIP-180).
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457): the error body shape.
- [Zalando RESTful API Guidelines](https://opensource.zalando.com/restful-api-guidelines/): compatibility rules and extensible enums.
- [IETF draft: The Idempotency-Key HTTP Header Field](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/): retry-safe POST.
