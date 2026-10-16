# Exception and retry runbook (proposed)
1. **Detect:** request exceeds SLA or downstream API returns error; capture correlation ID.
2. **Classify:** 4xx validation/auth (non-retry by default), 409 duplicate (reconcile), 429 (respect retry-after), 5xx/timeouts (bounded retries).
3. **Contain:** never provision access on rejected/unauthorized input; avoid duplicate dispatch with idempotency key.
4. **Retry:** suggested exponential delays 1, 2, 4 minutes plus jitter; actual policy subject to platform limits and owner approval.
5. **Escalate:** after max attempts, open IT exception with request ID, sanitized error, owner, business impact and due time.
6. **Resolve:** fix mapping/credentials or data at source; replay only after approval; confirm audit history.
7. **Close:** update HR and manager; record root cause and prevention action.

## Operational acceptance
No silent failures; error owner visible; trace ID preserved; replay is safe; secrets and PII redacted.
