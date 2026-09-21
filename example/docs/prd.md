# PRD — Warung Checkout: reduce payment-step abandonment

## Problem

61% of shoppers who reach the payment step never complete the order. Session recordings and funnel data point at two places. First, the address form: it has 11 fields, all required, and it is the single biggest drop-off point on mobile. Second, payment selection: the page lists 14 payment methods in one flat list, and shoppers scroll past the one they actually use.

Support tickets say the same thing in plainer words: "too long", "I gave up".

## Who it is for

- **Primary user:** A returning grocery shopper in Jakarta or Surabaya, on an Android phone over 4G, buying a basket of 8–20 items, usually in the evening. They have ordered before and are ordering the same kind of thing again.
- **Secondary user:** A first-time shopper who has not created an account and does not want to.

## Business outcome

- **Lever:** Revenue.
- **What changes if this works:** More carts that reach payment become paid orders. No new traffic needed — this is the same shoppers, finishing.
- **How we will measure it:** Payment-step abandonment rate. Currently 61%. Target under 45% within one quarter. Guardrail metric: failed-payment rate must not rise above its current 3.2%.

## Scope

**In scope**
- Shorten the address form to the fields actually needed for delivery.
- Remember and prefill the last-used address for returning shoppers.
- Show the shopper's three most recently used payment methods first, with the rest behind a "More options" control.
- Guest checkout — buy without creating an account (see ADR-0002).
- Clear, specific error messages when payment fails.

**Explicitly out of scope**
- One-click checkout. It needs stored payment credentials, which is a separate decision with real security weight.
- Any change to the cart page itself.
- New payment methods. We are reordering the existing 14, not adding a 15th.
- Loyalty points and vouchers.

## User stories with acceptance criteria

1. As a returning shopper, I see my last delivery address already filled in, so I do not retype it.
   - Given I have completed an order before and am signed in, when I reach the address step, then the form is prefilled with my most recent delivery address and an "Edit" control is visible.
   - Given I tap "Edit" and change the street field, when I continue, then the new address is used for this order and becomes my most recent address.
   - Given I have never ordered before, when I reach the address step, then the form is empty and no error is shown.

2. As any shopper, I fill in fewer address fields, so the form is faster on a phone.
   - Given I am on the address step, when the form renders, then exactly these fields are present: recipient name, phone, street address, city, postal code, and an optional delivery note.
   - Given I leave the optional delivery note empty, when I continue, then the order proceeds with no error.
   - Given I enter a postal code that is not 5 digits, when I continue, then I stay on the form and see "Postal code must be 5 digits" next to that field, and no other field shows an error.

3. As a returning shopper, I see the payment methods I actually use at the top, so I do not scroll.
   - Given I have paid with GoPay, then a bank transfer, then GoPay again, when I reach payment selection, then GoPay and bank transfer appear first, most recent first.
   - Given I have never paid before, when I reach payment selection, then the three most popular methods store-wide appear first.
   - Given I tap "More options", then all 14 methods are shown.

4. As a first-time shopper, I complete an order without creating an account.
   - Given I am not signed in, when I reach checkout, then I can continue as a guest without being asked for a password.
   - Given I complete a guest order, when the order is confirmed, then I receive the confirmation by email and am offered — not required — to create an account.

5. As any shopper, when payment fails I understand what to do next.
   - Given my payment is declined for insufficient funds, when the failure returns, then I see "Payment declined — not enough balance. Try another method." and my cart is still intact.
   - Given payment fails for any reason, when I return to the payment step, then nothing in my cart or address has been lost.

## Constraints

- **Performance:** The checkout page must be interactive within 2 seconds on a mid-range Android phone over 4G. Payment-step p95 latency must stay under 800ms.
- **Security / privacy:** This flow touches names, phone numbers, delivery addresses, and payment authorization. Card data never reaches our servers — Midtrans handles it (ADR-0003). Addresses and phone numbers must never appear in application logs.
- **Compatibility:** Chrome on Android 10+, Safari on iOS 15+. Screens down to 375px wide.
- **Deadline:** Must ship before the Ramadan sales peak, which starts 18 February 2027. That date is fixed by the marketing calendar and cannot move.

## Open questions

- Do we keep guest orders linked to an email address for reordering, or discard them after delivery? — owner: Sari (Product) — needed by: 12 Nov 2026
- Is the "three most recent payment methods" list per device or per account? Affects guest shoppers. — owner: Sari (Product) — needed by: 12 Nov 2026
- Who approves the wording of payment failure messages — product or support? — owner: Dimas (Support lead) — needed by: 20 Nov 2026

Anything unanswered here is a reason for the agent to ask, not to guess.
