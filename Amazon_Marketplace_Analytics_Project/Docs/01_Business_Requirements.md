# Marketplace Revenue and Seller Reporting: business requirements

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Case status:** Independent portfolio simulation using supplied repository data. Jamie Christian is the portfolio author. Stakeholder roles, proposed meetings, estimates, and approvals below are illustrative. This is not a claim of employment, client engagement, or production deployment.

## Business context and decision

A marketplace operations team needs one agreed view of gross merchandise value, platform revenue, seller concentration, and take rate before it reviews seller performance.

The decision to support is: **Which seller/category combinations deserve an operational review, and which KPI definitions must be standardized before the next monthly business review?** The report is a decision aid. It does not automatically change business policy or execute a commercial action.

## Baseline and measurable objectives

The supplied source contains **5,500 records** over 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12. The extract is the analytical baseline. There is no verified historical baseline for reporting labor, adoption, financial uplift, or forecasting accuracy.

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

- Authoritative source: `Data/amazon_marketplace_aligned.csv` from repository commit `7e619b132a3d63304aec64a3e726829ae5c97863`.
- Grain: Source row describing an order-level marketplace record. No order identifier is supplied; source row number is an ingestion key, not proof of business uniqueness.
- Original input bytes are retained. Canonical types and names are mapped at ingestion; source-derived percentages are not used as aggregate rates.
- Limitations: The dataset has no item cost, returns, seller fees beyond platform revenue, inventory, or experiment assignment. It cannot establish profit margins, pricing causality, or actual Amazon business performance.

## Stakeholders and approval responsibilities

| Role | Position | Decision rights |
| --- | --- | --- |
| Sponsor | Marketplace General Manager | Approve scope, funding assumptions, and business release |
| Business owner | Marketplace Operations Manager | Approve metric semantics and UAT disposition |
| Primary user | Seller Performance Analyst | Validate report interpretation and review workflow |
| Data owner | Source System Administrator | Confirm keys, source semantics, completeness, and export authorization |
| Engineering | Data / BI Engineer | Implement transformations, access controls, logging, and refresh |
| Control reviewer | Finance / Security Reviewer | Approve reconciliation, sensitive-data handling, and access model |

The sponsor approves scope and release; the business owner approves metric semantics and UAT; the source owner validates contracts; engineering implements controls. These duties must be confirmed in a real engagement.

## Prioritized requirement inventory

| ID | Requirement | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| MKT-REQ-01 | Ingest marketplace records | Must | Every source record has one source_row and the aggregate GMV reconciles within $0.01. |
| MKT-REQ-02 | Separate GMV from platform revenue | Must | Portfolio totals match Q01 and neither measure is described as profit. |
| MKT-REQ-03 | Calculate weighted take rate | Must | A two-row fixture with unequal GMV produces the ratio of sums; zero GMV returns null. |
| MKT-REQ-04 | Review seller concentration | Must | Seller GMV sums to the portfolio GMV; all shares sum to 1 within tolerance. |
| MKT-REQ-05 | Identify product contribution | Should | Cumulative share is nondecreasing and the final row reaches 1. |
| MKT-REQ-06 | Show monthly changes | Should | First month has no prior comparison; months sort chronologically. |
| MKT-REQ-07 | Govern extracts and access | Must | A future role test denies viewer export and records an audit event; current CSV prototype is local only. |
| MKT-REQ-08 | Explain review actions | Should | Every recommendation identifies an owner, supporting result, uncertainty, and next validation step. |

Must requirements protect correct interpretation, lineage, or access. Should requirements add useful drilldowns or workflow enhancements. Priorities are proposed for review, not approved stakeholder commitments.

## Success and release criteria

The analytical prototype is acceptable when source control totals reconcile, all delivered SQL runs, and tests confirm weighted arithmetic and domain boundaries. A production release additionally requires confirmed provenance, approved KPI semantics, implemented access tests, successful business UAT, refresh monitoring, and a signed decision from the appropriate approvers. A passing analytical test alone does not constitute business acceptance.

## Open discovery items

Request order_id, fee schedule, returns, item costs, seller SLAs, and ledger control totals before extending this case into commercial profitability.

For unresolved questions, record the owner, required evidence, and deadline in the RAID log. Do not convert assumptions into facts to close a requirement.
