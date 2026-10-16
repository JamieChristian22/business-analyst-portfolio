# Functional Requirements Document (FRD)
**Status:** Draft design; no production verification

| ID | Functional requirement | Rule / expected system behavior | Error path | Linked business requirement |
|---|---|---|---|---|
| FR-01 | Employee intake | Accept required `employeeId`, `fullName`, `email`, `department`, `managerId`, `startDate`, `roleCode` | Return field-level errors | BR-01 |
| FR-02 | Email validation | Require syntactically valid email; trim whitespace and normalize domain case per policy | Reject request without provisioning | BR-02 |
| FR-03 | Duplicate detection | Compare unique employee identifier against active/pending records | Block and route for review | BR-02 |
| FR-04 | Manager approval | Record approver ID, timestamp, decision, reason | Rejected request returns to HR | BR-03 |
| FR-05 | Role mapping | Map approved role code to predefined access bundles | Unknown role requires IT review | BR-04 |
| FR-06 | Provisioning dispatch | Create idempotent request with correlation ID | Retry transient failures; escalate persistent failures | BR-04 |
| FR-07 | Status tracking | Show Draft/Pending Approval/Approved/Provisioning/Exception/Completed | Alert on overdue stage | BR-05 |
| FR-08 | Audit history | Store actor, action, timestamp, old/new status, correlation ID | Alert if logging unavailable | BR-06 |
| FR-09 | Notifications | Send manager approval, rejection, completion, exception notices | Queue failed notifications | BR-07 |
| FR-10 | KPI reporting | Aggregate throughput, cycle time, failure rate, aging | Show missing-data warnings | BR-08 |

## Business rules
- Provisioning cannot begin without a valid employee identifier, validated email, and required approvals.
- Retries must be bounded and idempotent to prevent duplicate account requests.
- Elevated access is not automatically granted through standard role mapping.
- Failed or rejected requests remain traceable; do not silently discard errors.

## Open design decisions
Email policy beyond syntax, duplicate matching criteria, role catalog, retry thresholds, SLA and retention period require owner approval.
