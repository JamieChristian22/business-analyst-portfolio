# Restaurant Sales Reporting by City and Zone: business requirements

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


**Case status:** Independent portfolio simulation using supplied repository data. Jamie Christian is the portfolio author. Stakeholder roles, proposed meetings, estimates, and approvals below are illustrative. This is not a claim of employment, client engagement, or production deployment.

## Business context and decision

A restaurant operations team needs monthly sales comparisons across cities and zones, stable restaurant rankings, and a defensible review of changes over the six-month extract.

The decision to support is: **Which restaurants and zones require a manager review, and are observed monthly changes supported by comparable records?** The report is a decision aid. It does not automatically change business policy or execute a commercial action.

## Baseline and measurable objectives

The supplied source contains **1,320 records** over 2025-07, 2025-08, 2025-09, 2025-10, 2025-11, 2025-12. The extract is the analytical baseline. There is no verified historical baseline for reporting labor, adoption, financial uplift, or forecasting accuracy.

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

- Authoritative source: `Data/regional_sales_tableau_aligned.csv` from repository commit `7e619b132a3d63304aec64a3e726829ae5c97863`.
- Grain: One restaurant-month sales record. Restaurant ID plus month is the candidate business key and is tested for uniqueness.
- Original input bytes are retained. Canonical types and names are mapped at ingestion; source-derived percentages are not used as aggregate rates.
- Limitations: There are no revenue targets, sales reps, product categories, operating costs, or prior-year records. This case cannot establish target attainment, profitability, rep performance, or year-over-year change.

## Stakeholders and approval responsibilities

| Role | Position | Decision rights |
| --- | --- | --- |
| Sponsor | Regional Operations Director | Approve scope, funding assumptions, and business release |
| Business owner | Sales Operations Manager | Approve metric semantics and UAT disposition |
| Primary user | Regional Analyst | Validate report interpretation and review workflow |
| Data owner | Source System Administrator | Confirm keys, source semantics, completeness, and export authorization |
| Engineering | Data / BI Engineer | Implement transformations, access controls, logging, and refresh |
| Control reviewer | Finance / Security Reviewer | Approve reconciliation, sensitive-data handling, and access model |

The sponsor approves scope and release; the business owner approves metric semantics and UAT; the source owner validates contracts; engineering implements controls. These duties must be confirmed in a real engagement.

## Prioritized requirement inventory

| ID | Requirement | Priority | Acceptance criteria |
| --- | --- | --- | --- |
| REG-REQ-01 | Validate restaurant-month grain | Must | No duplicate candidate keys or conflicting mappings are silently accepted. |
| REG-REQ-02 | Aggregate city and zone sales | Must | Each grouping independently reconciles to portfolio sales within $0.01. |
| REG-REQ-03 | Show monthly change | Must | July has no prior comparison; a missing August makes September comparison null. |
| REG-REQ-04 | Rank restaurants fairly | Should | Ranks use the full selected period and ties resolve deterministically. |
| REG-REQ-05 | Expose coverage gaps | Must | Restaurants with fewer than the extract month count are listed for investigation. |
| REG-REQ-06 | Separate sales from targets | Must | All current metrics refer to sales; no YoY or profitability claim is presented. |
| REG-REQ-07 | Define manager review workflow | Should | Design includes owner, reason, next action, due date, and review evidence. |
| REG-REQ-08 | Define access by region | Must | Future role tests limit managers to assigned zones; current local CSV has no RLS. |

Must requirements protect correct interpretation, lineage, or access. Should requirements add useful drilldowns or workflow enhancements. Priorities are proposed for review, not approved stakeholder commitments.

## Success and release criteria

The analytical prototype is acceptable when source control totals reconcile, all delivered SQL runs, and tests confirm weighted arithmetic and domain boundaries. A production release additionally requires confirmed provenance, approved KPI semantics, implemented access tests, successful business UAT, refresh monitoring, and a signed decision from the appropriate approvers. A passing analytical test alone does not constitute business acceptance.

## Open discovery items

Obtain monthly targets, store operating calendar, closures, currency, comparable-store flags, costs, and prior-year sales before extending performance conclusions.

For unresolved questions, record the owner, required evidence, and deadline in the RAID log. Do not convert assumptions into facts to close a requirement.
