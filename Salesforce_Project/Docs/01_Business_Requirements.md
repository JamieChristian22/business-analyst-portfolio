# CRM Pipeline Definitions and Forecast Readiness: business requirements

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Case status:** Independent portfolio simulation using supplied repository data. Jamie Christian is the portfolio author. Stakeholder roles, proposed meetings, estimates, and approvals below are illustrative. This is not a claim of employment, client engagement, or production deployment.

## Business context and decision

A sales operations team needs a transparent pipeline view that separates open opportunities, closed outcomes, and probability-weighted amounts before using the CRM extract in a forecast discussion.

The decision to support is: **What is the current open pipeline and weighted open pipeline, and what additional CRM fields are needed before forecasting timing or conversion?** The report is a decision aid. It does not automatically change business policy or execute a commercial action.

## Baseline and measurable objectives

The supplied source contains **10 records** in one undated snapshot. The extract is the analytical baseline. There is no verified historical baseline for reporting labor, adoption, financial uplift, or forecasting accuracy.

1. Every source record remains traceable through source_row and the input SHA-256 hash.
2. Additive control totals reconcile within $0.01 and integer counts reconcile exactly.
3. Every documented requirement has acceptance criteria, a user story, and a UAT case.
4. Rates use the ratio of matched aggregate amounts/counts. Zero denominators display as undefined.
5. Unresolved source differences and design gaps remain visible before any business release decision.

These are prototype quality objectives. Benefits such as saved reporting time require a measured production pilot; no realized benefit is asserted.

## Scope boundary

**In scope:** data profiling; canonical field mapping; five runnable SQL analyses; business KPI definitions; process/control redesign; role-based access design; evidence-linked recommendations; backlog, traceability, RAID, change control, and UAT planning.

**Out of scope:** upstream system replacement; live connectors; credential setup; configured CRM rules; production row-level security; scheduler deployment; real stakeholder approval; and financial or causal conclusions beyond the extract.

## Source and grain

- Authoritative source: `Data/pipeline.csv` from repository commit `7e619b132a3d63304aec64a3e726829ae5c97863`.
- Grain: One current opportunity snapshot identified by Opportunity. There are ten records; no snapshot date or stage history is supplied.
- Original input bytes are retained. Canonical types and names are mapped at ingestion; source-derived percentages are not used as aggregate rates.
- Limitations: There are no close dates, owners, customer identifiers, stage history, snapshot dates, or activities. This is a small current-state snapshot and cannot establish conversion rates, sales velocity, forecast accuracy, or a historical win rate.

## Stakeholders and approval responsibilities

| Role | Position | Decision rights |
| --- | --- | --- |
| Sponsor | VP Sales | Approve scope, funding assumptions, and business release |
| Business owner | Sales Operations Manager | Approve metric semantics and UAT disposition |
| Primary user | Revenue Operations Analyst | Validate report interpretation and review workflow |
| Data owner | Source System Administrator | Confirm keys, source semantics, completeness, and export authorization |
| Engineering | Data / BI Engineer | Implement transformations, access controls, logging, and refresh |
| Control reviewer | Finance / Security Reviewer | Approve reconciliation, sensitive-data handling, and access model |

The sponsor approves scope and release; the business owner approves metric semantics and UAT; the source owner validates contracts; engineering implements controls. These duties must be confirmed in a real engagement.

## Prioritized requirement inventory

| ID | Requirement | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| CRM-REQ-01 | Validate opportunity records | Must | Duplicate IDs and probability outside 0-1 are detected; supplied records are profiled. |
| CRM-REQ-02 | Separate open and closed values | Must | Open + won + lost equals all-record amount within $0.01. |
| CRM-REQ-03 | Calculate weighted open pipeline | Must | Fixed unequal-amount fixture matches sum of products; closed values are excluded. |
| CRM-REQ-04 | Review stage concentration | Should | Stage amounts reconcile; counts total the source record count. |
| CRM-REQ-05 | Create opportunity review queue | Should | Only open stages appear and each value is traceable to one source record. |
| CRM-REQ-06 | Expose forecast limitations | Must | No sales velocity, historical win rate, or time-bounded forecast is claimed. |
| CRM-REQ-07 | Specify stage controls | Must | Closed Won with probability below 1 and Closed Lost above 0 are blocked in fixture/design tests. |
| CRM-REQ-08 | Define CRM role controls | Must | Future role tests prevent unauthorized forecast edits; local CSV prototype does not enforce CRM roles. |

Must requirements protect correct interpretation, lineage, or access. Should requirements add useful drilldowns or workflow enhancements. Priorities are proposed for review, not approved stakeholder commitments.

## Success and release criteria

The analytical prototype is acceptable when source control totals reconcile, all delivered SQL runs, and tests confirm weighted arithmetic and domain boundaries. A production release additionally requires confirmed provenance, approved KPI semantics, implemented access tests, successful business UAT, refresh monitoring, and a signed decision from the appropriate approvers. A passing analytical test alone does not constitute business acceptance.

## Open discovery items

Add snapshot_date, owner_id, created_date, expected_close_date, stage_history, loss_reason, account_id, and approved probability policy before time-bounded forecasting.

For unresolved questions, record the owner, required evidence, and deadline in the RAID log. Do not convert assumptions into facts to close a requirement.
