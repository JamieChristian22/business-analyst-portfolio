# Functional and data specification

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Data contract

One restaurant-month sales record. Restaurant ID plus month is the candidate business key and is tested for uniqueness.

`source_row` is an integer lineage identifier assigned to the data record after the CSV header. It is never presented as a customer, order, or opportunity business key. Required blank fields or nonfinite numbers cause ingestion to fail with a row/field error. Schema changes require an explicit mapping update and revalidation.

| Source field | Canonical field | Type | Unit | Null policy | Interpretation |
| --- | --- | --- | --- | --- | --- |
| Restaurant ID | restaurant_id | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| City | city | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Zone | zone | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Month | month | YYYY-MM period | Identifier / category | Required | Reporting month; filter numerator and denominator consistently. |
| Sales | sales | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |

## Business rules and metric arithmetic

| Metric | Formula | Interpretation / boundary |
| --- | --- | --- |
| Total sales | Sum sales | Currency is assumed USD for this portfolio; confirm production currency. |
| Zone sales share | Zone sales / portfolio sales | Use matching selected months. |
| Monthly change | (Current sales - prior-month sales) / prior-month sales | First month and nonconsecutive comparisons return null. |
| Restaurant rank | Sales descending; restaurant_id ascending for ties | Use selected-period totals, not an arbitrary last row. |
| Reporting coverage | Distinct months per restaurant | Coverage gaps remain visible; do not fill absent rows with zero. |

Counts and monetary values are summed before division. Rates are stored as fractions and formatted as percentages at presentation. Reconciliation tolerance is $0.01 for monetary totals and zero for record counts. Source rates may be rounded; they are retained for comparison rather than averaged.

## Detailed requirements

### REG-REQ-01: Validate restaurant-month grain

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Validate unique restaurant_id/month and stable city/zone mapping.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** No duplicate candidate keys or conflicting mappings are silently accepted.
- **Exception and boundary behavior:** Duplicate restaurant-month keys and conflicting city/zone mappings are reported rather than silently summed.
- **Traceability:** REG-US-01; REG-UAT-01-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### REG-REQ-02: Aggregate city and zone sales

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Summarize total sales by city and by zone over the supplied months.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Each grouping independently reconciles to portfolio sales within $0.01.
- **Exception and boundary behavior:** A restaurant has one stable zone in the supplied data; a changed mapping requires an effective-dated production design.
- **Traceability:** REG-US-02; REG-UAT-02-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### REG-REQ-03: Show monthly change

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Calculate month-over-month sales change only for adjacent reporting months.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** July has no prior comparison; a missing August makes September comparison null.
- **Exception and boundary behavior:** September following July without August has null adjacent-month change.
- **Traceability:** REG-US-03; REG-UAT-03-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### REG-REQ-04: Rank restaurants fairly

- **Priority / owner:** Should / Sales Operations Manager.
- **Behavior:** Rank restaurants by selected-period sales with stable tie handling.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q04.csv and SQL/Q04.sql.
- **Acceptance criteria:** Ranks use the full selected period and ties resolve deterministically.
- **Exception and boundary behavior:** Tied sales use restaurant_id ordering; compare the same reporting population.
- **Traceability:** REG-US-04; REG-UAT-04-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### REG-REQ-05: Expose coverage gaps

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Show the number of reported months by restaurant.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q04.csv and SQL/Q04.sql.
- **Acceptance criteria:** Restaurants with fewer than the extract month count are listed for investigation.
- **Exception and boundary behavior:** Absent restaurant-months are gaps, not zeros; obtain closure/operating-calendar context.
- **Traceability:** REG-US-05; REG-UAT-05-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### REG-REQ-06: Separate sales from targets

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Exclude target-attainment and profit claims until target and cost datasets exist.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** All current metrics refer to sales; no YoY or profitability claim is presented.
- **Exception and boundary behavior:** No targets, costs, reps, or prior-year data exist; exclude unsupported measures.
- **Traceability:** REG-US-06; REG-UAT-06-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### REG-REQ-07: Define manager review workflow

- **Priority / owner:** Should / Sales Operations Manager.
- **Behavior:** Allow a manager to record context and disposition for a flagged change.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** Design includes owner, reason, next action, due date, and review evidence.
- **Exception and boundary behavior:** A manager can reject a suspected cause and record a context request; retain the evidence and decision.
- **Traceability:** REG-US-07; REG-UAT-07-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.

### REG-REQ-08: Define access by region

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Specify region/zone access and an auditable export policy.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** Future role tests limit managers to assigned zones; current local CSV has no RLS.
- **Exception and boundary behavior:** A manager outside the assigned zone must be denied in a future role test.
- **Traceability:** REG-US-08; REG-UAT-08-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.


## Shared error behavior

A missing required input is an ingestion exception. A ratio with zero denominator is null, displayed as 'Undefined'; it is not a zero performance rate. Empty selections show 'No records' with counts, rather than a successful-looking blank dashboard. Unknown categories and invalid month strings are quarantined in the proposed production contract. The local prototype raises errors for missing required input and records domain exceptions in its profile.

The SQL prototype uses SQLite 3.25+ window functions. It runs against a complete supplied extract in memory. Proposed interactive filters are specified in the BI design and must be tested when implemented; the static result exports are not a filterable production application.
