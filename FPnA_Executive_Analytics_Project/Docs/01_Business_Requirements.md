# Finance Reporting Reconciliation and Variance Control: business requirements

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Case status:** Independent portfolio simulation using supplied repository data. Jamie Christian is the portfolio author. Stakeholder roles, proposed meetings, estimates, and approvals below are illustrative. This is not a claim of employment, client engagement, or production deployment.

## Business context and decision

Finance has two supplied extracts: a dashboard summary and an account fact table. Leadership needs reconciled actual/budget reporting and an explicit treatment of any differences before a close pack can be approved.

The decision to support is: **Can the account fact table support a reliable variance pack, and can its totals be reconciled to the separate dashboard extract?** The report is a decision aid. It does not automatically change business policy or execute a commercial action.

## Baseline and measurable objectives

The supplied source contains **420 records** over 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12. The extract is the analytical baseline. There is no verified historical baseline for reporting labor, adoption, financial uplift, or forecasting accuracy.

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

- Authoritative source: `Data/fpna_finance_fact.csv` from repository commit `7e619b132a3d63304aec64a3e726829ae5c97863`.
- Grain: One month / fiscal year / department / region / account / account category / scenario record. Account categories are Revenue, COGS, and OpEx; scenarios are Actual and Budget.
- Original input bytes are retained. Canonical types and names are mapped at ingestion; source-derived percentages are not used as aggregate rates.
- Limitations: The two supplied extracts are not assumed to share totals or definitions. The account fact table is the analysis basis; reconciliation differences remain visible and block production close approval. There are no balance sheet or cash-flow records.

## Stakeholders and approval responsibilities

| Role | Position | Decision rights |
| --- | --- | --- |
| Sponsor | Chief Financial Officer | Approve scope, funding assumptions, and business release |
| Business owner | FP&A Manager | Approve metric semantics and UAT disposition |
| Primary user | Finance Analyst | Validate report interpretation and review workflow |
| Data owner | Source System Administrator | Confirm keys, source semantics, completeness, and export authorization |
| Engineering | Data / BI Engineer | Implement transformations, access controls, logging, and refresh |
| Control reviewer | Finance / Security Reviewer | Approve reconciliation, sensitive-data handling, and access model |

The sponsor approves scope and release; the business owner approves metric semantics and UAT; the source owner validates contracts; engineering implements controls. These duties must be confirmed in a real engagement.

## Prioritized requirement inventory

| ID | Requirement | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| FIN-REQ-01 | Validate finance dimensions | Must | All accepted rows have allowed scenario/category values and traceable source_row. |
| FIN-REQ-02 | Create actual/budget revenue bridge | Must | Actual and budget reconcile separately; zero budget returns null rate. |
| FIN-REQ-03 | Calculate operating income | Must | A fixed fixture produces the expected operating income and weighted gross margin. |
| FIN-REQ-04 | Explain department contribution | Must | Department variances sum to the overall variance; no percentage averages are used. |
| FIN-REQ-05 | Reconcile the dashboard extract | Must | Every difference above $0.01 is listed; unresolved differences block close approval. |
| FIN-REQ-06 | Preserve a close version | Must | A rebuilt run produces identical totals for identical input hashes. |
| FIN-REQ-07 | Design approval workflow | Must | A rejected reconciliation remains unresolved and cannot be marked approved by the preparer alone. |
| FIN-REQ-08 | Document forecast limits | Should | No forecast accuracy uplift is claimed without actual/forecast history and a defined error measure. |

Must requirements protect correct interpretation, lineage, or access. Should requirements add useful drilldowns or workflow enhancements. Priorities are proposed for review, not approved stakeholder commitments.

## Success and release criteria

The analytical prototype is acceptable when source control totals reconcile, all delivered SQL runs, and tests confirm weighted arithmetic and domain boundaries. A production release additionally requires confirmed provenance, approved KPI semantics, implemented access tests, successful business UAT, refresh monitoring, and a signed decision from the appropriate approvers. A passing analytical test alone does not constitute business acceptance.

## Open discovery items

Obtain ledger control totals, chart-of-accounts mapping, approved budget version, FX policy, fiscal calendar, and controller signoff before production finance use.

For unresolved questions, record the owner, required evidence, and deadline in the RAID log. Do not convert assumptions into facts to close a requirement.
