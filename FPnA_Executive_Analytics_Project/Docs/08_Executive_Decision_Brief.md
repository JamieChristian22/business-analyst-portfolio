# Decision brief: Finance Reporting Reconciliation and Variance Control

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Decision requested:** approve the proposed metric definitions, investigate source gaps, and prioritize a governed pilot. This is an illustrative sponsor brief, not an approved business decision.

## Business question

Can the account fact table support a reliable variance pack, and can its totals be reconciled to the separate dashboard extract?

## Evidence

- **Account-fact baseline:** Actual revenue $13,328,601.00 versus budget $13,330,369.00; variance $-1,768.00 (-0.01%). Evidence: Analysis/Q02.csv.
- **Operating income:** Fact-derived actual operating income is $1,447,948.00. Evidence: Analysis/Q02.csv.
- **Revenue source reconciliation:** 30 of 30 month/department revenue comparisons match within $0.01; 0 remain unresolved. Evidence: Analysis/Q04.csv.
- **Variance ownership:** Customer Success has the lowest signed revenue variance: $-19,990.00. Evidence: Analysis/Q03.csv.

## Recommended next actions

| Action | Owner | Evidence needed to close |
| --- | --- | --- |
| Review the signed variance by department and keep the dashboard source separate. | FP&A Manager | These totals come from the fact table only. |
| Confirm sign and account mapping with Accounting. | FP&A Manager | Positive COGS and OpEx are subtracted; no balance sheet or cash flow is present. |
| Retain the reconciliation at every refresh; any future difference blocks a production close pack until the reviewer approves its resolution. | FP&A Manager | Revenue matching does not validate every summary field, an approved ledger, or business acceptance. |
| Request a department narrative supported by operational drivers. | FP&A Manager | Variance magnitude does not establish cause or personal performance. |

## Required controls and unresolved limits

The two supplied extracts are not assumed to share totals or definitions. The account fact table is the analysis basis; reconciliation differences remain visible and block production close approval. There are no balance sheet or cash-flow records.

Obtain ledger control totals, chart-of-accounts mapping, approved budget version, FX policy, fiscal calendar, and controller signoff before production finance use.

An analytical validation pass confirms implemented calculations and fixture behavior. Approval still requires source-owner confirmation, business UAT, configured role controls, and operational monitoring. For Finance, an unresolved reconciliation explicitly blocks close-pack approval.

## Pilot and benefit measurement

Measure four comparable refresh cycles, reconciliation time, exception backlog, user task success, and adoption of the agreed review workflow. Record the baseline before deployment. Labor savings can be modeled as (baseline minutes - pilot minutes) / 60 multiplied by approved loaded hourly cost, with a documented number of cycles. No actual labor rate or saved time is supplied, so no financial benefit is asserted here.

## Sponsor disposition

Decision: Pending. Approver: Chief Financial Officer. Required record: approve / reject / defer; rationale; date; conditions; and linked evidence. Keep this disposition separate from technical test status.
