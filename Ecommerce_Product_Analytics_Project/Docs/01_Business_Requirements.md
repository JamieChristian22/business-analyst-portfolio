# Ecommerce Funnel Measurement and Experiment Discovery: business requirements

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Case status:** Independent portfolio simulation using supplied repository data. Jamie Christian is the portfolio author. Stakeholder roles, proposed meetings, estimates, and approvals below are illustrative. This is not a claim of employment, client engagement, or production deployment.

## Business context and decision

An ecommerce team needs a reliable funnel baseline and device comparison to choose a checkout investigation without attributing drop-off to causes that were never measured.

The decision to support is: **Which funnel transition and device should be investigated first, and what new instrumentation is needed to test a proposed checkout change?** The report is a decision aid. It does not automatically change business policy or execute a commercial action.

## Baseline and measurable objectives

The supplied source contains **14,000 records** over 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12. The extract is the analytical baseline. There is no verified historical baseline for reporting labor, adoption, financial uplift, or forecasting accuracy.

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

- Authoritative source: `Data/ecommerce_product_analytics_aligned.csv` from repository commit `7e619b132a3d63304aec64a3e726829ae5c97863`.
- Grain: Anonymous source observation with binary funnel counts. There is no customer/session identifier; totals count observations and cannot establish distinct customers across periods.
- Original input bytes are retained. Canonical types and names are mapped at ingestion; source-derived percentages are not used as aggregate rates.
- Limitations: Repeated complete rows may be valid anonymous observations. Retain them until event keys establish duplication. There are no shipping fees, error events, experiment arms, or customer IDs; causal checkout explanations and unique-customer claims are unsupported.

## Stakeholders and approval responsibilities

| Role | Position | Decision rights |
| --- | --- | --- |
| Sponsor | Head of Ecommerce | Approve scope, funding assumptions, and business release |
| Business owner | Checkout Product Manager | Approve metric semantics and UAT disposition |
| Primary user | Product Analyst | Validate report interpretation and review workflow |
| Data owner | Source System Administrator | Confirm keys, source semantics, completeness, and export authorization |
| Engineering | Data / BI Engineer | Implement transformations, access controls, logging, and refresh |
| Control reviewer | Finance / Security Reviewer | Approve reconciliation, sensitive-data handling, and access model |

The sponsor approves scope and release; the business owner approves metric semantics and UAT; the source owner validates contracts; engineering implements controls. These duties must be confirmed in a real engagement.

## Prioritized requirement inventory

| ID | Requirement | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| ECOM-REQ-01 | Preserve anonymous observations | Must | Row count equals the source count; repeated-row count is profiled and disclosed. |
| ECOM-REQ-02 | Define a monotonic funnel | Must | Every violating observation is reported; the supplied file passes or is explicitly flagged. |
| ECOM-REQ-03 | Calculate funnel rates | Must | Zero denominators return null; a weighted fixture matches independently calculated results. |
| ECOM-REQ-04 | Compare devices | Must | Device stage counts reconcile to portfolio totals and comparisons use identical periods. |
| ECOM-REQ-05 | Inspect acquisition mix | Should | Channel revenue sums to total; low sample counts are visible. |
| ECOM-REQ-06 | Track monthly conversion | Should | The first month has null prior-month change and no missing month is silently treated as zero. |
| ECOM-REQ-07 | Specify an experiment | Should | No claim of experiment success is made without assignment/exposure events; launch remains pending. |
| ECOM-REQ-08 | Protect customer data | Must | Future design excludes raw contact data from analyst exports and requires a privacy review. |

Must requirements protect correct interpretation, lineage, or access. Should requirements add useful drilldowns or workflow enhancements. Priorities are proposed for review, not approved stakeholder commitments.

## Success and release criteria

The analytical prototype is acceptable when source control totals reconcile, all delivered SQL runs, and tests confirm weighted arithmetic and domain boundaries. A production release additionally requires confirmed provenance, approved KPI semantics, implemented access tests, successful business UAT, refresh monitoring, and a signed decision from the appropriate approvers. A passing analytical test alone does not constitute business acceptance.

## Open discovery items

Add event_id, session_id, exposure_id, experiment_variant, timestamps, shipping quote events, payment outcomes, and consent flags before causal experimentation.

For unresolved questions, record the owner, required evidence, and deadline in the RAID log. Do not convert assumptions into facts to close a requirement.
