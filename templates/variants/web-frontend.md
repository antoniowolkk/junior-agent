# Variant: Frontend-only web app

Paste these into the matching sections of `AGENTS.md`.

## 3. Stack and layout

- **Framework:** React + TypeScript (Vite) <or Next.js — say which>
- **Styling:** <Tailwind | CSS modules>
- **Tests:** Vitest + Testing Library
- **Data source:** <external API | static content | CMS>

```
src/
  features/<name>/   one folder per feature: component, hooks, tests
  components/        shared, presentational only
  lib/               helpers, API client
  styles/
docs/                prd.md, adr/
```

## 4. Commands

| Purpose | Command |
| --- | --- |
| Install | `pnpm install` |
| Dev server | `pnpm dev` |
| Test | `pnpm test` |
| Lint | `pnpm lint` |
| Type check | `pnpm typecheck` |
| Build | `pnpm build` |

## 5. Conventions — additions

- Components are presentational; data fetching lives in hooks.
- Every fetching screen handles loading, empty, and error states.
- Accessibility is not optional: semantic elements, labeled inputs, keyboard reachable, visible focus, sufficient contrast.
- Responsive down to 375px width.
- Use existing design tokens/variables. Do not introduce new one-off colors or spacing values.

## 7. Guardrails — additions

- **Everything in this repo is public once shipped.** Never place an API key, token, or secret in the code, even in an env var that is bundled at build time.
- Never add a third-party script, tracker, analytics tag, or font CDN without approval.
- Never change the build/deploy config.
