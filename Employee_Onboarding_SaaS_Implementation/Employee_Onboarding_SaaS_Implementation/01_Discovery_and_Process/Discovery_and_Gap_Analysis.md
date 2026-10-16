# Discovery, stakeholders and gaps
## Business objective
Reduce handoff ambiguity and incomplete employee data while improving traceability of access provisioning.

## Stakeholder map
| Stakeholder | Concern | Discovery question | Output |
|---|---|---|---|
| HR coordinator | Accurate intake | Which fields are mandatory? | Data dictionary |
| Hiring manager | Timely approval | What triggers rejection or escalation? | Approval rules |
| IT support | Provisioning queue | Which applications depend on role? | Access matrix |
| Security/IAM | Least privilege | Who approves privileged access? | Control matrix |
| Employee | Day-one readiness | How is completion communicated? | SLA and notifications |
| Compliance | Auditability | What evidence is retained and for how long? | Audit requirements |

## AS-IS pain points (scenario hypotheses)
- Handoff via email/spreadsheets; no consistent status visibility.
- Approval request loops when fields are incomplete.
- Re-keying of employee data creates inconsistency.
- Unclear owner when account creation stalls.
- Delayed audit trail for access decisions.

## TO-BE design changes
| Gap | Proposed control | Validation |
|---|---|---|
| Missing email | Required-field + format validation | Negative UAT cases |
| Approval bottleneck | SLA timers and escalation | Workflow UAT |
| Duplicate identities | Unique HR identifier + duplicate check | Integration test |
| Provisioning failure | Retry queue, correlation ID, IT ticket | Failure-path test |
| Weak traceability | Immutable approval and event log | Audit sample review |

## Assumptions and open questions
- An HR SaaS system and IAM connector are available (not confirmed).
- Approval policy, retention period, licensing, and SLA require stakeholder signoff.
- No real employee data or live directory access is used in this exercise.
