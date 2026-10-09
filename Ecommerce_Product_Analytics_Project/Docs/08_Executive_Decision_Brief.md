# Decision brief: Ecommerce Funnel Measurement and Experiment Discovery

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Decision requested:** approve the proposed metric definitions, investigate source gaps, and prioritize a governed pilot. This is an illustrative sponsor brief, not an approved business decision.

## Business question

Which funnel transition and device should be investigated first, and what new instrumentation is needed to test a proposed checkout change?

## Evidence

- **Funnel baseline:** 14,000 view observations, 2,406 cart observations, 1,608 checkout observations, and 1,200 purchase observations. Evidence: Analysis/Q01.csv.
- **Largest proportional transition loss:** View to cart loses 82.81% of prior-stage observations (11,594 observations). Evidence: Analysis/Q01.csv.
- **Device comparison:** desktop has the highest observed purchase/view rate at 10.58% across 4,425 view observations. Evidence: Analysis/Q02.csv.
- **Revenue and source profit:** Revenue is $94,277.20; supplied profit is $23,418.34. Evidence: Analysis/Q01.csv.

## Recommended next actions

| Action | Owner | Evidence needed to close |
| --- | --- | --- |
| Use observation labels until an event/customer contract is approved. | Checkout Product Manager | No customer/session key proves unique people. |
| Inspect errors, device context, and shipping/payment events before selecting a change. | Checkout Product Manager | Loss identifies where to investigate, not why abandonment occurs. |
| Use this comparison to prioritize investigation, not claim device causality. | Checkout Product Manager | Device mix and channel differences are uncontrolled. |
| Confirm the profit definition and obtain cost/return records before extending the economics. | Checkout Product Manager | Source profit is not independently reconciled to costs. |

## Required controls and unresolved limits

Repeated complete rows may be valid anonymous observations. Retain them until event keys establish duplication. There are no shipping fees, error events, experiment arms, or customer IDs; causal checkout explanations and unique-customer claims are unsupported.

Add event_id, session_id, exposure_id, experiment_variant, timestamps, shipping quote events, payment outcomes, and consent flags before causal experimentation.

An analytical validation pass confirms implemented calculations and fixture behavior. Approval still requires source-owner confirmation, business UAT, configured role controls, and operational monitoring. For Finance, an unresolved reconciliation explicitly blocks close-pack approval.

## Pilot and benefit measurement

Measure four comparable refresh cycles, reconciliation time, exception backlog, user task success, and adoption of the agreed review workflow. Record the baseline before deployment. Labor savings can be modeled as (baseline minutes - pilot minutes) / 60 multiplied by approved loaded hourly cost, with a documented number of cycles. No actual labor rate or saved time is supplied, so no financial benefit is asserted here.

## Sponsor disposition

Decision: Pending. Approver: Head of Ecommerce. Required record: approve / reject / defer; rationale; date; conditions; and linked evidence. Keep this disposition separate from technical test status.
