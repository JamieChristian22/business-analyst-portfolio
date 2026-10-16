# KPI dictionary (targets, not observed outcomes)
| KPI | Formula | Proposed target | Source / cadence |
|---|---|---|---|
| First-pass completeness | Requests accepted without correction / submitted requests | ≥98% | Intake logs; weekly |
| On-time provisioning | Completed within SLA / approved requests due | ≥95% | Workflow timestamps; weekly |
| Average onboarding cycle time | Avg(completed timestamp - approved timestamp) | Baseline then improve | Event log; weekly |
| Integration error rate | Failed integration attempts / total attempts | Agree threshold | Integration monitoring; daily |
| Duplicate account incidents | Confirmed duplicate accounts per period | 0 | IAM audit; monthly |
| Approval compliance | Provisioned requests with required approval / all provisioned requests | 100% | Audit trail; monthly |

**Data quality rules:** exclude test data from operational reporting, track missing timestamps, define timezone, segment by department and onboarding type, and document denominator exclusions.
