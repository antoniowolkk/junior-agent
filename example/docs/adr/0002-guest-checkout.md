# ADR-0002: Allow guest checkout

- **Status:** Accepted
- **Date:** 2026-10-21
- **Deciders:** Sari (Product), Rio (Tech lead)

## Context

Every shopper is currently forced to create an account before paying. Funnel data shows 23% of first-time shoppers who reach the account step never come back. Support tickets describe it as "I only wanted groceries, not another password."

The original reason for the requirement was reorder history and marketing reach — both real, both valuable to us rather than to the shopper at that moment.

Deliveries need a name, phone, and address regardless. None of those require a password.

## Decision

Shoppers can complete an order without an account. We collect name, phone, address, and email. After the order is confirmed, we offer account creation — pre-filled from what they already typed — but never require it.

Guest orders are stored against the email address so support can find them and so we can offer reorder later. A guest is not a user record; it is an order with contact details.

## Alternatives considered

- **Keep the account requirement** — we know the cost: 23% of first-time shoppers lost at that step.
- **Social login only (Google/Apple)** — reduces friction but not to zero, adds an external dependency to the critical payment path, and excludes shoppers who do not want their grocery habits tied to a Google account.
- **Deferred account creation with a magic link before payment** — still a step, still an inbox round-trip on a phone mid-purchase.

## Consequences

**Good**
- Removes an entire step from the highest-drop-off part of the funnel.
- First-time shoppers can buy in one session.
- Aligns the flow with what the shopper is actually trying to do.

**Bad / accepted cost**
- Weaker marketing reach: fewer accounts created, smaller mailing list.
- Support cannot verify a guest by login; identity is checked by order number plus email.
- Two paths through checkout to build and test instead of one.
- Fraud risk rises slightly without account history. Mitigated by Midtrans-side checks (ADR-0003) and a per-phone-number rate limit.

**Follow-ups**
- Decide retention policy for guest order data — currently an open question in `docs/prd.md`.
- Add a per-phone-number rate limit on order creation.
- Post-order account creation must not lose the order context.
