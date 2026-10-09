# Process and gap analysis

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


![Process controls](../Diagrams/process_controls.svg)

## Current and future state

The current-state issues below are scenario assumptions informed by repository inconsistencies and source gaps. The future state is a proposed design. No reporting-time reduction or operational adoption has been measured.

| Owner | Step | Current issue | Proposed control |
| --- | --- | --- | --- |
| Operations | Collect marketplace export | Manual source comparison | Versioned file receipt |
| BA / Finance | Resolve KPI disagreements | Mix GMV and revenue | Approved KPI dictionary |
| Data Engineer | Validate and normalize rows | Untracked spreadsheet edits | Schema and reconciliation gate |
| Analyst | Analyze seller and product mix | Average percentage rows | Weighted KPIs and drilldowns |
| Sponsor | Assign seller reviews | Act on unsupported margin claims | Evidence-led review queue |

## Gap disposition

| Gap | Evidence | Proposed response | Verification |
| --- | --- | --- | --- |
| Metric definitions differ across narrative and source | Historical assets compared with supplied CSV fields | Use current BRD, canonical dictionary, and explicit metric formulas | Recompute Q01 and review labels |
| Refresh has no source lineage | Source files have no approved production run metadata | Hash input, retain source_row, record execution log | Same input hash produces matching control totals |
| Exceptions have no accountable owner | No actual external approval record exists | Assign an owner and retain disposition in RAID / UAT | Release review checks every open Must issue |
| Controls described but not implemented | Local CSV/SQL prototype has no identity layer | Implement role controls in a future BI/CRM deployment | Positive and negative authorization tests |

## Handoff and exception path

The source owner hands an immutable extract and source contract to engineering. Engineering returns schema, row, and control-total exceptions to the BA and data owner. The BA explains business impact and updates the requirement when source semantics change. The business owner approves the disposition; unresolved control failures keep the prior approved report available. Analysts then create review actions with a reason and evidence. The sponsor receives the decision brief after the controls and business UAT are complete.

## Proposed performance measurement

Measure reporting preparation time over four comparable refresh cycles before and after deployment, including exception handling and review time. Measure reconciliation exception count, failed refreshes, task completion during user review, and outstanding Must requirements. Preserve denominators and sample sizes. Treat the results as a pilot with uncertainty; do not extrapolate financial uplift from a process diagram.
