# Functional and data specification

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Data contract

One month / fiscal year / department / region / account / account category / scenario record. Account categories are Revenue, COGS, and OpEx; scenarios are Actual and Budget.

`source_row` is an integer lineage identifier assigned to the data record after the CSV header. It is never presented as a customer, order, or opportunity business key. Required blank fields or nonfinite numbers cause ingestion to fail with a row/field error. Schema changes require an explicit mapping update and revalidation.

| Source field | Canonical field | Type | Unit | Null policy | Interpretation |
| --- | --- | --- | --- | --- | --- |
| MonthYear | month | YYYY-MM period | Identifier / category | Required | Reporting month; filter numerator and denominator consistently. |
| FiscalYear | fiscal_year | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Department | department | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Region | region | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Account | account | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| AccountCategory | account_category | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Scenario | scenario | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Amount | amount | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |

## Business rules and metric arithmetic

| Metric | Formula | Interpretation / boundary |
| --- | --- | --- |
| Revenue actual | Sum amount where Revenue and Actual | Use the account fact table; do not combine dashboard summary revenue. |
| Revenue budget | Sum amount where Revenue and Budget | Use matching months/departments; missing budget is not zero. |
| Revenue variance | Revenue actual minus budget | Positive means revenue above budget; use ratio to budget only when budget is nonzero. |
| Operating income | Actual revenue minus actual COGS minus actual OpEx | Costs are positive amounts in this source; validate sign conventions. |
| Gross margin | (Actual revenue minus actual COGS) / actual revenue | Return null for zero revenue; do not average department margin percentages. |

Counts and monetary values are summed before division. Rates are stored as fractions and formatted as percentages at presentation. Reconciliation tolerance is $0.01 for monetary totals and zero for record counts. Source rates may be rounded; they are retained for comparison rather than averaged.

## Detailed requirements

### FIN-REQ-01: Validate finance dimensions

- **Priority / owner:** Must / FP&A Manager.
- **Behavior:** Load the fact table and validate month, scenario, category, and numeric amount.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** All accepted rows have allowed scenario/category values and traceable source_row.
- **Exception and boundary behavior:** Unknown account categories or scenarios require mapping review; no fallback to Revenue.
- **Traceability:** FIN-US-01; FIN-UAT-01-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### FIN-REQ-02: Create actual/budget revenue bridge

- **Priority / owner:** Must / FP&A Manager.
- **Behavior:** Show actual, budget, dollar variance, and variance rate for each month.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Actual and budget reconcile separately; zero budget returns null rate.
- **Exception and boundary behavior:** Zero budget produces undefined percentage variance; absent budget is an exception rather than a zero budget.
- **Traceability:** FIN-US-02; FIN-UAT-02-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### FIN-REQ-03: Calculate operating income

- **Priority / owner:** Must / FP&A Manager.
- **Behavior:** Subtract COGS and OpEx from revenue using actual scenario only.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** A fixed fixture produces the expected operating income and weighted gross margin.
- **Exception and boundary behavior:** Subtract positive costs; do not mix summary-derived operating income with fact-derived totals.
- **Traceability:** FIN-US-03; FIN-UAT-03-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### FIN-REQ-04: Explain department contribution

- **Priority / owner:** Must / FP&A Manager.
- **Behavior:** Rank departments by signed revenue variance and show corresponding budgets.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** Department variances sum to the overall variance; no percentage averages are used.
- **Exception and boundary behavior:** Department variance totals reconcile while department variance percentages are not additive.
- **Traceability:** FIN-US-04; FIN-UAT-04-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### FIN-REQ-05: Reconcile the dashboard extract

- **Priority / owner:** Must / FP&A Manager.
- **Behavior:** Compare account-fact revenue to the supplied dashboard summary by month and department.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q04.csv and SQL/Q04.sql.
- **Acceptance criteria:** Every difference above $0.01 is listed; unresolved differences block close approval.
- **Exception and boundary behavior:** Missing source and nonzero discrepancies remain unresolved; do not average or overwrite either extract.
- **Traceability:** FIN-US-05; FIN-UAT-05-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### FIN-REQ-06: Preserve a close version

- **Priority / owner:** Must / FP&A Manager.
- **Behavior:** Record file hashes, run timestamp, control totals, and the sign convention.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** A rebuilt run produces identical totals for identical input hashes.
- **Exception and boundary behavior:** Identical input hashes produce equal control totals; new files require a new close version.
- **Traceability:** FIN-US-06; FIN-UAT-06-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### FIN-REQ-07: Design approval workflow

- **Priority / owner:** Must / FP&A Manager.
- **Behavior:** Require preparer, reviewer, and CFO decisions before distributing a close pack.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** A rejected reconciliation remains unresolved and cannot be marked approved by the preparer alone.
- **Exception and boundary behavior:** The preparer cannot approve their own material exception; approval remains pending without reviewer evidence.
- **Traceability:** FIN-US-07; FIN-UAT-07-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.

### FIN-REQ-08: Document forecast limits

- **Priority / owner:** Should / FP&A Manager.
- **Behavior:** Separate measured variance from prospective cost or revenue scenarios.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** No forecast accuracy uplift is claimed without actual/forecast history and a defined error measure.
- **Exception and boundary behavior:** A forecast without forecast history cannot claim improved forecasting accuracy.
- **Traceability:** FIN-US-08; FIN-UAT-08-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.


## Shared error behavior

A missing required input is an ingestion exception. A ratio with zero denominator is null, displayed as 'Undefined'; it is not a zero performance rate. Empty selections show 'No records' with counts, rather than a successful-looking blank dashboard. Unknown categories and invalid month strings are quarantined in the proposed production contract. The local prototype raises errors for missing required input and records domain exceptions in its profile.

The SQL prototype uses SQLite 3.25+ window functions. It runs against a complete supplied extract in memory. Proposed interactive filters are specified in the BI design and must be tested when implemented; the static result exports are not a filterable production application.
