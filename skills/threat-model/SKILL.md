---
name: threat-model
description: Read-only security audit of a whole app or one exposed surface, where every finding comes with file:line and proof. Use for "is this safe to ship", "can this get hacked", "security audit", "threat model this", "check my app for vulnerabilities", "before I launch", or when handed a security checklist prompt like "hide my API keys, add rate limiting, make no mistakes". Fixes nothing.
---

# Threat Model

Find out how the app can be attacked, and prove each finding before anyone reports it. This skill is for the whole attack surface (every route, form, key and table), not one diff. For a single diff, use the Security lens in **interrogate**.

The skill only reads. It never fixes a finding, never upgrades a dependency, never rewrites git history, and never prints a secret. The output is a findings report. Each fix becomes its own task afterwards, and the human approves it.

`AGENTS.md` section 7 outranks this file. The rules that come up most here: do not read or print secrets, do not install anything, do not touch staging or production, and get an ADR plus explicit approval before any change to auth, sessions, CORS, permissions or rate limiting.

## 0. When you are handed a checklist prompt

Security checklists pasted in from videos and threads ("hide my keys, add auth, protect against XSS, make no mistakes") are a list of goals with no steps and no proof. Do not work through them item by item, editing as you go. Map each item to the phase below that checks it, run this skill, and report.

| Checklist says | What this skill does with it |
| --- | --- |
| Hide API keys, check env vars, check git history for secrets | Phase 3, Secrets. Report file and commit only, never the value. |
| Protect admin routes, users only access what they should | Phase 3, Access control. Most important check in the list. |
| Add proper authentication | Not an audit item. It is a feature: route it through **descope**, then an ADR. |
| Sanitize forms, protect against XSS | Phase 3, Injection. Trace each input to where it lands. |
| Rate limiting, secure API endpoints | Phase 3, Authentication and Access control. |
| CORS, security headers, debug mode, exposed files | Phase 3, Misconfiguration. Probe the running app locally. |
| Update dependencies | Phase 3, Supply chain. Audit and list. Upgrading is a section 7 stop. |
| Secure the database, hash passwords | Phase 3, Data. |
| Remove anything I don't need | Not an audit item. Deleting is a section 7 stop. Hand it to **descope**. |
| Make no mistakes | Replaced by phase 4. Every finding carries its proof level. |

## 1. Scope

Before reading any code, write down:

- **Target.** The whole repo, or one surface ("the new upload endpoint").
- **Where probes run.** Localhost only unless the human names a staging URL and says yes. Never production.
- **Tools available.** Check with `command -v gitleaks pip-audit`, and so on. A missing scanner is a gap to report, not something to install on your own.

## 2. Map the surface

Answer "what are we working on" before "what can go wrong". Fill this table from the code, with `file:line` for each row. Hand bulk reading to a sub-agent per **context-engineering**.

| Entry point | Who can reach it | Touches | Trust boundary crossed |
| --- | --- | --- | --- |
| e.g. `POST /api/invoices/:id` | logged-in user | `invoices` table | user → another user's rows |

Include routes and API handlers, server actions, forms, webhooks, file uploads, admin pages, cron jobs, and the client bundle, since everything shipped to the browser is public. List the roles too: anonymous, user, admin, service.

A row with no clear "who can reach it" is already a finding.

## 3. Walk the checks

Work in OWASP Top 10:2025 order, because that order reflects how often each class shows up in real apps. For each check, record **finding**, **cleared** or **not checked**. Silence is not "cleared".

| Class | Check | How |
| --- | --- | --- |
| **Access control** (A01) | Every handler that loads an object by ID checks that the caller owns it or is allowed to see it | For each row in the phase 2 table, find the ownership check's `file:line`. A handler with no check is a finding. Hiding an admin link in the UI is not a check; the server has to enforce the role. |
| | Deny by default | Find what a route gets when no rule matches. A new route should be closed until someone opens it. |
| **Misconfiguration** (A02) | Debug mode, verbose errors, stack traces sent to the client | Check framework debug flags and the production env defaults. Trigger an error locally and read what comes back. |
| | Security headers | `curl -sS -D - -o /dev/null http://localhost:PORT/` Check for `Content-Security-Policy`, `Strict-Transport-Security`, `X-Content-Type-Options: nosniff`, `Referrer-Policy`, and frame protection. `Server` and `X-Powered-By` should be missing. `X-XSS-Protection` should be missing too: it is deprecated, and CSP replaces it. |
| | CORS | `curl -sS -D - -o /dev/null -H 'Origin: https://evil.example' http://localhost:PORT/api/...` An `Access-Control-Allow-Origin` that echoes the attacker's origin, or `*` alongside `Access-Control-Allow-Credentials: true`, is a finding. |
| | Exposed files | Request `/.env`, `/.git/HEAD`, `/*.map`, and backup or dump files from the local server. A `200` is a finding. |
| **Supply chain** (A03) | Known-vulnerable dependencies | `npm audit --omit=dev --json` or `pip-audit`, whichever fits the stack. Report counts by severity, and name each high or critical package. Do not run `npm audit fix`. |
| **Data** (A04) | Password hashing | Find where passwords are stored. Argon2, bcrypt or scrypt clears it. MD5, SHA-1, plain SHA-256, or reversible encryption is a finding. |
| | Database rules | For a backend-as-a-service (Supabase, Firebase), every table the client can reach needs row-level rules. Supabase's publishable key is public by design, so an exposed table without RLS can be read and written by anyone who holds it. |
| **Secrets** (A04) | Secrets in the tree | `git ls-files \| grep -E '(^\|/)\.env'` and `git check-ignore -v .env`. Search source and the client bundle for key-shaped strings. Report the path and line only. |
| | Secrets in history | `git log --all -G '<pattern>' --format='%h %s' --name-only` prints commit and file without the value. Use patterns such as `AKIA[0-9A-Z]{16}`, `-----BEGIN [A-Z ]*PRIVATE KEY-----`, and `sk-[A-Za-z0-9_-]{20,}`. If `gitleaks` is installed, `gitleaks git --redact --log-opts="--all"`. A secret that was committed and later deleted is still leaked. |
| **Injection** (A05) | User input reaching a sink | Trace each input from phase 2 to where it ends up: SQL built by string concatenation, `innerHTML`, `dangerouslySetInnerHTML`, `v-html`, `eval`, shell exec, template render, a file path, or a URL the server fetches (SSRF). A finding names both the source line and the sink line. Client-side validation is not the boundary. |
| **Authentication** (A07) | Session and token verification | JWTs are verified with the signature checked and the algorithm pinned. Sessions expire. Logout invalidates the session on the server. |
| | Rate limiting | Login, signup, password reset, and any endpoint that sends email or SMS or costs money need a limit. Find where it is enforced, or report that it is missing. |
| **Exceptional conditions** (A10) | Fail closed | An auth or permission check that throws should deny access, not let the request through. Read the catch blocks around the checks. |

## 4. Prove each finding

A security writeup reads as convincing whether or not it is true, just like a blast-radius writeup. Give every finding a proof level, and aim as high as is cheap:

1. **Pattern match.** Grep hit only. Label it `guess`. It does not go in the report as a finding; it goes under **not checked**.
2. **Pointed at the line.** Real `file:line` for the missing check or the unsafe sink. `inferred`.
3. **Traced it.** Walked from the source to the sink, or from the request to the missing check, step by step, and nothing on the path stops it. `inferred`.
4. **Reproduced locally.** A `curl` or a test against the local app shows it. Example: user B's session fetches user A's invoice and gets `200`. `measured`.

Access-control and injection findings should reach level 3 or 4. Use two local test accounts; creating accounts on any non-local system is a section 7 stop. If the app cannot run locally, say `inconclusive` for every check that needed it.

## 5. Report

```
Scope: <target>, probed <where>, tools <present / missing>

| Sev | Class | Finding | file:line | Proof | Proposed fix | Gate |
| --- | --- | --- | --- | --- | --- | --- |
| critical | A01 | GET /api/invoices/:id has no owner check | api/invoices.ts:42 | 4, measured: curl as user B → 200 | filter by session user | ADR + approval |

Cleared: <each check, one line on why>
Not checked: <each check, and why: no running app, missing tool, out of scope>
Rotate now: <any leaked secret, by file and commit only>
```

Severity: **critical** means anyone can do it without an account, or it exposes other users' data. **High** needs an account, or leaks something sensitive. **Medium** is defense in depth that is missing (headers, rate limits). **Low** is hygiene.

The **Gate** column says which section 7 stop or ADR each fix needs, so the human can see at a glance what they have to approve.

## 6. Hand off

- **Leaked secret:** rotating it comes first, and the human does it. Rewriting history does not un-leak a secret that is already pushed, and history rewrites are a section 7 stop anyway.
- **Each fix is its own task.** Route it through **rigor**: a missing check is a Bug fix with a reproduction (use the level 4 proof as the failing test), and a new control is a Feature. Auth, CORS, sessions and rate limiting get an ADR first.
- End with the top three findings in plain language: who could do what to whom.

## Failure modes

| Smell | What it means |
| --- | --- |
| The audit edited code | You fixed while auditing. Revert, and report instead. |
| A secret value appears in the output | Stop. It is now in the transcript. Tell the human to rotate it. |
| "No issues found" with no Cleared list | You did not do the audit. Every check gets a line. |
| Every finding is a grep hit | Level 1 is not a finding. Trace it or move it to Not checked. |
| Probing a deployed URL nobody named | Section 7 stop. Localhost only. |
| Admin protection is "the link is hidden" | That is UI. The server check is what counts. |
| Long list of headers, zero access-control findings | You checked what is easy instead of what matters. A01 comes first for a reason. |

## Sources

- [OWASP Top 10:2025](https://top10.owasp.org/2025): the class order in phase 3.
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html): the four questions behind phases 2–5.
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html): deny by default, and checking each object on every request.
- [OWASP HTTP Headers Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html): headers to set, and headers to remove.
- [gitleaks](https://github.com/gitleaks/gitleaks): `git` / `dir` subcommands, `--redact`, `--log-opts`.
- [Supabase: Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security): an exposed table without RLS is open to anyone holding the key.
- [strix](https://github.com/usestrix/strix): an AI pentest agent that reports only findings it has validated with a proof of concept. The model for phase 4.
