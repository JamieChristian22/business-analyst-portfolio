# Decision brief: Marketplace Revenue and Seller Reporting

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Decision requested:** approve the proposed metric definitions, investigate source gaps, and prioritize a governed pilot. This is an illustrative sponsor brief, not an approved business decision.

## Business question

Which seller/category combinations deserve an operational review, and which KPI definitions must be standardized before the next monthly business review?

## Evidence

- **Portfolio volume:** GMV $239,161.36; platform revenue $33,393.15; orders 5,500. Evidence: Analysis/Q01.csv.
- **Seller contribution:** Apex Outdoor contributes 25.30% of GMV. Evidence: Analysis/Q03.csv.
- **Product concentration:** Top 16 of 80 products contribute 24.44% of GMV. Evidence: Analysis/Q04.csv.
- **Weighted monetization:** Portfolio take rate is 13.96%; AOV is $43.48. Evidence: Analysis/Q01.csv.

## Recommended next actions

| Action | Owner | Evidence needed to close |
| --- | --- | --- |
| Use separate measures in monthly reporting. | Marketplace Operations Manager | GMV and platform revenue have different business meanings. |
| Ask operations to review seller context before any commercial action. | Marketplace Operations Manager | Concentration is observed; seller quality or margin is not measured. |
| Use the computed contribution rather than assume an 80/20 relationship. | Marketplace Operations Manager | This directly tests the historical generic Pareto claim. |
| Ask Finance to approve definitions and reconcile platform revenue to its ledger. | Marketplace Operations Manager | The rates use the ratio of sums, not an average of row percentages. |

## Required controls and unresolved limits

The dataset has no item cost, returns, seller fees beyond platform revenue, inventory, or experiment assignment. It cannot establish profit margins, pricing causality, or actual Amazon business performance.

Request order_id, fee schedule, returns, item costs, seller SLAs, and ledger control totals before extending this case into commercial profitability.

An analytical validation pass confirms implemented calculations and fixture behavior. Approval still requires source-owner confirmation, business UAT, configured role controls, and operational monitoring. For Finance, an unresolved reconciliation explicitly blocks close-pack approval.

## Pilot and benefit measurement

Measure four comparable refresh cycles, reconciliation time, exception backlog, user task success, and adoption of the agreed review workflow. Record the baseline before deployment. Labor savings can be modeled as (baseline minutes - pilot minutes) / 60 multiplied by approved loaded hourly cost, with a documented number of cycles. No actual labor rate or saved time is supplied, so no financial benefit is asserted here.

## Sponsor disposition

Decision: Pending. Approver: Marketplace General Manager. Required record: approve / reject / defer; rationale; date; conditions; and linked evidence. Keep this disposition separate from technical test status.
