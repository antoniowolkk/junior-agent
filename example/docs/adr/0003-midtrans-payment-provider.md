# ADR-0003: Use Midtrans as the payment provider

- **Status:** Accepted
- **Date:** 2026-10-28
- **Deciders:** Rio (Tech lead), Sari (Product), Nina (Finance)

## Context

We need to accept the payment methods Indonesian grocery shoppers actually use: GoPay, OVO, DANA, ShopeePay, bank transfer / virtual account, QRIS, and cards. Card acceptance alone would miss most of our shoppers.

We do not want card data touching our servers. Handling it ourselves would put the whole application in PCI-DSS scope, which is far beyond what this team can carry.

Settlement needs to reach an Indonesian bank account, and Finance needs reconciliation reports they can work with.

## Decision

We use Midtrans as the single payment provider, integrated via its hosted Snap flow so that card details are entered on Midtrans-controlled surfaces and never reach our backend.

Our backend creates a transaction, receives an asynchronous webhook for the result, and treats the webhook as the authoritative record of payment. The frontend result is treated as a hint for what to show the shopper, never as proof of payment.

All Midtrans credentials live in environment variables and are never read, printed, or logged by application code.

## Alternatives considered

- **Xendit** — comparable local coverage and a genuinely close call. Midtrans won on documentation quality for the specific e-wallets we need and on an existing relationship through Finance.
- **Stripe** — better developer experience, but weak coverage of Indonesian e-wallets, which are the majority of our volume. Wrong tool for this market.
- **Direct integrations with each wallet** — best fees at high volume, but a separate integration, contract, and reconciliation process per provider. Not affordable at our size.
- **Building card handling ourselves** — puts us in PCI-DSS scope. Rejected outright.

## Consequences

**Good**
- One integration covers every payment method our shoppers use.
- Card data never touches our infrastructure; PCI scope stays minimal.
- Finance gets reconciliation reports without custom work.

**Bad / accepted cost**
- Vendor lock-in. Switching later means rewriting the payment layer and re-testing every method.
- Transaction fees are higher than direct wallet integrations would be at volume.
- Their outage is our outage. We have no fallback provider.
- The hosted Snap flow limits how much of the payment UI we control.

**Follow-ups**
- Webhook handling must be idempotent — Midtrans retries, and a duplicate must never create a second order.
- Verify the webhook signature on every call. An unsigned or wrongly signed webhook is rejected and logged.
- Define what the shopper sees when Midtrans is unreachable.
- Revisit this ADR if monthly volume passes 50,000 transactions, where direct integrations start to pay for themselves.
