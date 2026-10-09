# Decision brief: CRM Pipeline Definitions and Forecast Readiness

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Decision requested:** approve the proposed metric definitions, investigate source gaps, and prioritize a governed pilot. This is an illustrative sponsor brief, not an approved business decision.

## Business question

What is the current open pipeline and weighted open pipeline, and what additional CRM fields are needed before forecasting timing or conversion?

## Evidence

- **Open pipeline:** Open opportunity amount is $119,000.00; weighted open amount is $53,550.00. Evidence: Analysis/Q02.csv.
- **Closed outcomes:** Closed won $30,000.00; closed lost $15,000.00. Evidence: Analysis/Q02.csv.
- **Snapshot size:** 10 opportunity records; all-record amount $164,000.00. Evidence: Analysis/Q01.csv.
- **Opportunity review:** Opportunity D (Negotiate) has the highest weighted open amount: $13,500.00. Evidence: Analysis/Q04.csv.

## Recommended next actions

| Action | Owner | Evidence needed to close |
| --- | --- | --- |
| Use open-only amounts in forecast-readiness discussions. | Sales Operations Manager | Weighted amounts are probability-based scenario values, not booked or dated forecast revenue. |
| Reconcile open plus closed to all-record amount. | Sales Operations Manager | Closed outcomes belong outside open pipeline; this snapshot does not support historical win rate. |
| Request timing and history fields before velocity or forecast accuracy reporting. | Sales Operations Manager | No snapshot date, close date, cohort, or stage history is supplied. |
| Ask the owner to validate stage and probability with account context. | Sales Operations Manager | No activity history explains probability or deal quality. |

## Required controls and unresolved limits

There are no close dates, owners, customer identifiers, stage history, snapshot dates, or activities. This is a small current-state snapshot and cannot establish conversion rates, sales velocity, forecast accuracy, or a historical win rate.

Add snapshot_date, owner_id, created_date, expected_close_date, stage_history, loss_reason, account_id, and approved probability policy before time-bounded forecasting.

An analytical validation pass confirms implemented calculations and fixture behavior. Approval still requires source-owner confirmation, business UAT, configured role controls, and operational monitoring. For Finance, an unresolved reconciliation explicitly blocks close-pack approval.

## Pilot and benefit measurement

Measure four comparable refresh cycles, reconciliation time, exception backlog, user task success, and adoption of the agreed review workflow. Record the baseline before deployment. Labor savings can be modeled as (baseline minutes - pilot minutes) / 60 multiplied by approved loaded hourly cost, with a documented number of cycles. No actual labor rate or saved time is supplied, so no financial benefit is asserted here.

## Sponsor disposition

Decision: Pending. Approver: VP Sales. Required record: approve / reject / defer; rationale; date; conditions; and linked evidence. Keep this disposition separate from technical test status.
