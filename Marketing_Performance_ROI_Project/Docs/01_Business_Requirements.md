# Advertising Efficiency and Budget Review: business requirements

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Case status:** Independent portfolio simulation using supplied repository data. Jamie Christian is the portfolio author. Stakeholder roles, proposed meetings, estimates, and approvals below are illustrative. This is not a claim of employment, client engagement, or production deployment.

## Business context and decision

A growth team needs a consistent way to compare ad groups and device mix while finance needs clarity on whether revenue/spend ratios represent ROAS, contribution, or full business ROI.

The decision to support is: **Which ad groups should be reviewed for a controlled budget test, and what cost/attribution gaps prevent a full ROI claim?** The report is a decision aid. It does not automatically change business policy or execute a commercial action.

## Baseline and measurable objectives

The supplied source contains **1,104 records** over 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12. The extract is the analytical baseline. There is no verified historical baseline for reporting labor, adoption, financial uplift, or forecasting accuracy.

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

- Authoritative source: `Data/marketing_ads_roi_dashboard_aligned.csv` from repository commit `7e619b132a3d63304aec64a3e726829ae5c97863`.
- Grain: Source advertising observation by month, ad group, and device. There is no campaign or event ID; repeated dimension combinations are valid additive records.
- Original input bytes are retained. Canonical types and names are mapped at ingestion; source-derived percentages are not used as aggregate rates.
- Limitations: Attributed revenue does not prove incremental revenue. Revenue minus advertising cost excludes COGS, agency fees, returns, and other costs; it is an ad-only contribution measure, not full net profit or causal ROI.

## Stakeholders and approval responsibilities

| Role | Position | Decision rights |
| --- | --- | --- |
| Sponsor | VP Growth | Approve scope, funding assumptions, and business release |
| Business owner | Marketing Operations Manager | Approve metric semantics and UAT disposition |
| Primary user | Campaign Analyst | Validate report interpretation and review workflow |
| Data owner | Source System Administrator | Confirm keys, source semantics, completeness, and export authorization |
| Engineering | Data / BI Engineer | Implement transformations, access controls, logging, and refresh |
| Control reviewer | Finance / Security Reviewer | Approve reconciliation, sensitive-data handling, and access model |

The sponsor approves scope and release; the business owner approves metric semantics and UAT; the source owner validates contracts; engineering implements controls. These duties must be confirmed in a real engagement.

## Prioritized requirement inventory

| ID | Requirement | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| ADS-REQ-01 | Load additive ad records | Must | Revenue and cost control totals reconcile independently to the CSV. |
| ADS-REQ-02 | Calculate weighted efficiency | Must | Weighted fixtures match independent arithmetic; all zero denominators return null. |
| ADS-REQ-03 | Compare ad groups | Must | Group totals reconcile to the portfolio totals and contribution is correctly labeled. |
| ADS-REQ-04 | Inspect device differences | Should | Device totals reconcile and no causal explanation is generated automatically. |
| ADS-REQ-05 | Track monthly efficiency | Should | Month order is chronological and first-month change is null. |
| ADS-REQ-06 | Set budget-test guardrails | Must | The proposed plan includes approval, holdout strategy, minimum evidence, and a stop rule. |
| ADS-REQ-07 | Validate P&L labeling | Must | Every record with a difference above $0.01 is reported and full-profit language is excluded. |
| ADS-REQ-08 | Govern campaign exports | Must | A future access test prevents viewer budget edits; prototype CSV has no role enforcement. |

Must requirements protect correct interpretation, lineage, or access. Should requirements add useful drilldowns or workflow enhancements. Priorities are proposed for review, not approved stakeholder commitments.

## Success and release criteria

The analytical prototype is acceptable when source control totals reconcile, all delivered SQL runs, and tests confirm weighted arithmetic and domain boundaries. A production release additionally requires confirmed provenance, approved KPI semantics, implemented access tests, successful business UAT, refresh monitoring, and a signed decision from the appropriate approvers. A passing analytical test alone does not constitute business acceptance.

## Open discovery items

Obtain campaign IDs, attribution windows, order-level revenue, returns, COGS, agency fees, and experiment assignments before full ROI or incrementality reporting.

For unresolved questions, record the owner, required evidence, and deadline in the RAID log. Do not convert assumptions into facts to close a requirement.
