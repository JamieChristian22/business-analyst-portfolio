# Decision brief: Restaurant Sales Reporting by City and Zone

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Decision requested:** approve the proposed metric definitions, investigate source gaps, and prioritize a governed pilot. This is an illustrative sponsor brief, not an approved business decision.

## Business question

Which restaurants and zones require a manager review, and are observed monthly changes supported by comparable records?

## Evidence

- **Restaurant sales baseline:** 220 restaurants across 6 months generate $74,146,771.54 sales. Evidence: Analysis/Q01.csv.
- **Restaurant review:** R-0187 in Greensboro has the highest six-month sales: $615,248.51. Evidence: Analysis/Q04.csv.
- **Latest monthly movement:** 2025-12 sales are $13,385,195.37; adjacent-month change is 4.01%. Evidence: Analysis/Q03.csv.
- **Coverage control:** All 220 restaurants report all six supplied months. Evidence: Analysis/Q04.csv.

## Recommended next actions

| Action | Owner | Evidence needed to close |
| --- | --- | --- |
| Use restaurant/city/zone reporting labels. | Sales Operations Manager | The extract contains restaurants, not sales reps or product margins. |
| Ask the manager for operating calendar, size, and local context. | Sales Operations Manager | Sales rank is not profitability or target attainment. |
| Discuss a comparable-month review and request prior-year records. | Sales Operations Manager | Six months cannot establish YoY changes or stable seasonality. |
| Obtain closures and comparable-store flags before performance judgments. | Sales Operations Manager | Complete source coverage does not prove comparable operating days. |

## Required controls and unresolved limits

There are no revenue targets, sales reps, product categories, operating costs, or prior-year records. This case cannot establish target attainment, profitability, rep performance, or year-over-year change.

Obtain monthly targets, store operating calendar, closures, currency, comparable-store flags, costs, and prior-year sales before extending performance conclusions.

An analytical validation pass confirms implemented calculations and fixture behavior. Approval still requires source-owner confirmation, business UAT, configured role controls, and operational monitoring. For Finance, an unresolved reconciliation explicitly blocks close-pack approval.

## Pilot and benefit measurement

Measure four comparable refresh cycles, reconciliation time, exception backlog, user task success, and adoption of the agreed review workflow. Record the baseline before deployment. Labor savings can be modeled as (baseline minutes - pilot minutes) / 60 multiplied by approved loaded hourly cost, with a documented number of cycles. No actual labor rate or saved time is supplied, so no financial benefit is asserted here.

## Sponsor disposition

Decision: Pending. Approver: Regional Operations Director. Required record: approve / reject / defer; rationale; date; conditions; and linked evidence. Keep this disposition separate from technical test status.
