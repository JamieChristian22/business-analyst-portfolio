# Employee onboarding SaaS implementation: delivery review

## Project scope
This is a **simulated** employee onboarding implementation case study. Its AS-IS and TO-BE diagrams, mock API tests, and Jira artifacts demonstrate business analysis techniques; they do not establish a deployed HR production system.

## Acceptance criteria to validate

| ID | Requirement | Acceptance evidence |
|---|---|---|
| ONB-AC-01 | Required intake fields are validated before submission | Positive and negative API cases with payloads and observed status codes |
| ONB-AC-02 | Manager approval is recorded before downstream provisioning | Workflow trace or test record demonstrating approval gating |
| ONB-AC-03 | Duplicate submissions are handled consistently | Repeated-request test with documented idempotency behavior |
| ONB-AC-04 | Unauthorized roles cannot approve or provision | Role-based negative test and response |
| ONB-AC-05 | Failure in downstream provisioning is visible and recoverable | Error scenario, retry/rollback decision, and operator-facing alert |
| ONB-AC-06 | UAT defects are traceable to requirements | Jira issue, acceptance criterion, test evidence, and retest outcome |

**Status:** These are *proposed verification criteria*, not claims that tests passed. Existing documented mock API assertions remain separate from this expanded checklist.

## Delivery decision log

| Decision | Options | Trade-off to document |
|---|---|---|
| Approval routing | Single approver / multi-step approval | Speed vs segregation of duties |
| Integration | Synchronous / queued | Immediate feedback vs resilience |
| Provisioning failure | Retry / manual review / compensation | Recovery vs duplicate actions |
| Access control | Broad admin / least-privilege roles | Convenience vs risk |

## Interview walkthrough
Explain the manual onboarding pain point; show the AS-IS map; identify stakeholder requirements; walk through the TO-BE design; demonstrate a mock API request and response; show how Jira UAT and defect records trace back to acceptance criteria; close with the limitations and next verification steps.

## Definition of done for a future production implementation
- Signed-off stakeholder requirements and security/privacy review
- Approved API contract, authentication and audit logging
- Tested failure handling, role boundaries and duplicate prevention
- Completed UAT with defect resolution and sign-off
- Operational runbook, monitoring, rollback plan and accountable owners

Do not mark any item complete without linked evidence.
