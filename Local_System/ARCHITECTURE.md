# Local system architecture and acceptance evidence

The browser presents six case studies, query tables, filtered charts, source detail, requirements, UAT, gap actions, and audit history. Python serves the UI and HTTP API on loopback. SQLite stores source facts and operational workflow state. The original CSVs and project registers remain immutable seed inputs.

## Transaction boundaries

Login establishes an expiring server-side session with an HttpOnly/SameSite cookie. Writes require a CSRF header and an approved application role. Each update checks the current version, applies the state transition, and inserts its audit record in one database transaction. Validation failures roll back. The UI receives a conflict when its record version is stale.

Analyst submits a requirement; reviewer approves/rejects after checking three evidenced UAT results. Admin has refresh authority but no business approval authority. Updating linked UAT invalidates prior acceptance. Changed source hashes additionally block previously passed tests, invalidate affected approvals, and reopen closed gaps for review. An unchanged refresh preserves workflow state.

Refresh loads all sources into a staging database before touching persistent facts. It validates schema, required values, domain rules, and source hashes. Only a successful staged run replaces facts and records a successful refresh. A failed staging run leaves the prior version in place. Dashboard filters operate on an isolated in-memory snapshot of persisted facts and never mutate the production-like local source tables.

## Key tables

| Table | Purpose |
| --- | --- |
| users | Salted password hashes and fixed local roles |
| requirements | Acceptance criteria, submission/review state, reviewer evidence, version |
| uat | Expected/actual result, evidence, tester, date, status, version |
| gaps | Current/target state, impact priority, linked requirement, closure evidence, version |
| audit | Actor, action, entity, before/after state, timestamp |
| refresh_runs | Successful source versions and hashes |
| Canonical fact tables | Unchanged source values mapped to typed analytical fields with row lineage |

## HTTP contract

| Endpoint | Method | Authorized behavior |
| --- | --- | --- |
| /api/login | POST | Credentials establish session; cross-origin writes rejected |
| /api/session | GET | Return current account role and CSRF token |
| /api/projects | GET | Authenticated case-study metadata |
| /api/dashboard | GET | Filtered query tables; detail denied to viewer |
| /api/export | GET | Aggregate CSV; source detail requires analyst/reviewer/admin |
| /api/records | GET | Authenticated requirement, UAT, and gap records |
| /api/uat | POST | Analyst/reviewer execution with evidence and version check |
| /api/requirement | POST | Analyst submission; reviewer evidence-based decision |
| /api/gap | POST | Analyst closure proposal; reviewer disposition |
| /api/refresh | POST | Admin-only staged refresh |
| /api/refresh | GET | Authenticated refresh metadata |
| /api/audit | GET | Reviewer/admin history |
| /api/logout | POST | Invalidate session |

## Verification

16 HTTP/database integration tests cover all six dashboards, source reconciliation under filters, CSV export, role denials, CSRF/origin denials, injection attempts, stale edits, evidence prerequisites, independent approval, approval invalidation, gap transitions, persistence, refresh permissions, failed-refresh preservation, and changed-source revalidation. These tests operate on temporary databases; they do not fabricate shipped UAT or approvals.

Client JavaScript passes a syntax check. Native browser visual testing could not run because this environment had no available browser executable and its browser download was blocked/truncated. No browser pass or screenshot is claimed. Inspect the actual desktop/mobile UI using the walkthrough in README.md; the HTTP controls are tested independently of the UI.

## Production differences

Loopback HTTP is appropriate for a local demonstration. Internet hosting requires a production application server, HTTPS, approved identity and business-scope authorization, secure secrets/retention, monitoring, and operational ownership. Direct file access can alter the local database; the audit log is not an external tamper-proof service. Native dashboard/CRM configuration and external acceptance remain explicit gaps.
