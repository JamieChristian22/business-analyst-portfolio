# Decision brief: Advertising Efficiency and Budget Review

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Decision requested:** approve the proposed metric definitions, investigate source gaps, and prioritize a governed pilot. This is an illustrative sponsor brief, not an approved business decision.

## Business question

Which ad groups should be reviewed for a controlled budget test, and what cost/attribution gaps prevent a full ROI claim?

## Evidence

- **Advertising baseline:** Attributed revenue $1,675,567.96; spend $1,254,002.01; weighted ROAS 1.34x. Evidence: Analysis/Q01.csv.
- **Ad-group review candidate:** Affiliates has the highest observed ROAS at 2.20x on $82,332.05 spend. Evidence: Analysis/Q02.csv.
- **Ad-only contribution:** Revenue minus ad cost is $421,565.95. Evidence: Analysis/Q01.csv.
- **Response counts:** 997,083 clicks and 20,129 attributed conversions. Evidence: Analysis/Q01.csv.

## Recommended next actions

| Action | Owner | Evidence needed to close |
| --- | --- | --- |
| Confirm attribution definitions before comparing across platforms. | Marketing Operations Manager | Attribution is not incrementality and the attribution window is unknown. |
| Propose a capped test with a holdout and Finance review. | Marketing Operations Manager | High average efficiency does not prove marginal response to more spend. |
| Label this ad-only contribution; request costs before full ROI or net profit reporting. | Marketing Operations Manager | This omits COGS, agency fees, overhead, returns, and other business costs. |
| Display denominators and clarify the conversion window. | Marketing Operations Manager | Conversion events do not prove incremental sales. |

## Required controls and unresolved limits

Attributed revenue does not prove incremental revenue. Revenue minus advertising cost excludes COGS, agency fees, returns, and other costs; it is an ad-only contribution measure, not full net profit or causal ROI.

Obtain campaign IDs, attribution windows, order-level revenue, returns, COGS, agency fees, and experiment assignments before full ROI or incrementality reporting.

An analytical validation pass confirms implemented calculations and fixture behavior. Approval still requires source-owner confirmation, business UAT, configured role controls, and operational monitoring. For Finance, an unresolved reconciliation explicitly blocks close-pack approval.

## Pilot and benefit measurement

Measure four comparable refresh cycles, reconciliation time, exception backlog, user task success, and adoption of the agreed review workflow. Record the baseline before deployment. Labor savings can be modeled as (baseline minutes - pilot minutes) / 60 multiplied by approved loaded hourly cost, with a documented number of cycles. No actual labor rate or saved time is supplied, so no financial benefit is asserted here.

## Sponsor disposition

Decision: Pending. Approver: VP Growth. Required record: approve / reject / defer; rationale; date; conditions; and linked evidence. Keep this disposition separate from technical test status.
