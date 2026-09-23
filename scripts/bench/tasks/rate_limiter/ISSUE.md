## Bug report

Support says some accounts are placing way more orders than their configured
rate limit should allow. It doesn't happen for every account, and nobody has
been able to catch it live. All the tests pass.

`RateLimiter` in `rate_limiter.py` is what enforces the limit. Please look
into it and fix whatever is wrong.
