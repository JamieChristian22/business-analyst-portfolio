# BI and system design

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Implemented versus proposed

Implemented: immutable CSVs, profiling, five SQL exports, fixtures, saved static previews, and the shared persistent SQLite workbench with local user identity, interactive query filters, refresh, workflow actions, local approvals, and audit records. Proposed for production: native platform integration, enterprise identity/RLS, external business acceptance, scheduler/monitoring integration, and hosted deployment. Historical PBIX/TWB files remain in Legacy and are not certified against the new canonical schema.

## Data architecture

Source export -> immutable landing/version -> schema and control validation -> canonical fact table -> query results / BI semantic model -> user review -> approved actions. Store exceptions beside the run, with file hash, source_row, rule, owner, and disposition. Publish only an approved version in production; keep the prior approved version available for rollback.

Canonical fact table: `pipeline`. Grain: One current opportunity snapshot identified by Opportunity. There are ten records; no snapshot date or stage history is supplied.

The local prototype uses source_row for lineage and loads original fields with documented types. A future dimensional model should use distinct dimension keys for opportunity_id, stage. Validate dimension uniqueness before joins. A one-to-many relationship must not multiply fact rows. Reconcile monetary totals before and after any join.

## Reporting experience specification

| View | Intended user task | Measures / evidence | Acceptance requirement |
| --- | --- | --- | --- |
| Overview | Understand scope, period, source freshness, and portfolio baseline | Q01 control totals; dataset count/hash | Values reconcile and interpretation limits are visible |
| Business comparison | Compare the relevant business categories | Q02 and Q03 | Numerator/denominator use the same population |
| Review detail | Trace an observation, contribution, or exception | Q04 and Q05 | Stable sorting, full denominators, and source lineage |
| Exceptions | Assign and resolve source/control gaps | Data profile, RAID, UAT | Unresolved exceptions do not disappear after refresh |

The HTML preview is a self-contained static snapshot of executed query outputs. It is useful for reviewers without BI software. It has no login, filter engine, refresh scheduler, or writeback. The shared local workbench provides reporting-period filters and source drilldown. In a future native BI build, add reporting-period filters only after snapshot/close dates exist, clear-filter action, no-record states, and drillthrough constrained to the same reporting population.

## Proposed semantic measures

The [DAX file](../Dashboard/proposed_measures.dax) contains core formulas for a future canonical model. These formulas are **not executed or validated in Power BI**. Import the canonical field schema, establish a valid model, add the required remaining measures from the KPI dictionary, and reconcile them against Q01-Q05 before certifying a dashboard. DIVIDE returns blank for zero denominators; display that as undefined rather than zero.

## Role and export design

| Role | Read | Change | Export | Audit requirement |
| --- | --- | --- | --- | --- |
| Viewer | Approved aggregate views | None | Aggregate export only if approved | Log sensitive export attempts |
| Analyst | Approved detail needed for analysis | Draft recommendations | Approved detail scope | Record input version and export population |
| Manager | Assigned business scope | Review disposition | Assigned scope only | Log approve/reject and reason |
| Administrator | Configuration and operational metadata | Mappings, refresh, permissions | Restricted operational need | Separate administrative activity from business approval |

For zone/department/seller segmentation, create a governed user-to-scope mapping with unique, effective-dated assignments. Deny missing assignments by default. Test a permitted user, a user outside scope, a missing mapping, an export attempt, and revoked access. No local CSV or static HTML output enforces this policy.

## Nonfunctional requirements

- Correctness: monetary controls within $0.01; exact counts; no silent row multiplication; undefined ratio treatment.
- Freshness: show source/reporting period and last successful refresh separately. A failed refresh retains a stale-data notice and does not pretend the report is current.
- Accessibility: future BI views require keyboard access, readable labels, text alternatives, and color-independent status meaning. Verify in the chosen platform with representative users.
- Performance: measure page and refresh time on expected production volume; set targets only after volume/concurrency is agreed. Local runs are not production load tests.
- Recoverability: retain previous approved input, mapping, and output versions. Rebuild and reconcile before republishing after an incident.
- Audit: retain who changed definitions, permissions, and approval state, when, and with what evidence. Confirm retention with the organization.

## Integration gaps

Add snapshot_date, owner_id, created_date, expected_close_date, stage_history, loss_reason, account_id, and approved probability policy before time-bounded forecasting. Live connectors and scheduler configuration require the organization's approved platform and credentials. The portfolio does not embed secrets or make changes to an external service.
