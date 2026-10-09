# Functional and data specification

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Data contract

Source row describing an order-level marketplace record. No order identifier is supplied; source row number is an ingestion key, not proof of business uniqueness.

`source_row` is an integer lineage identifier assigned to the data record after the CSV header. It is never presented as a customer, order, or opportunity business key. Required blank fields or nonfinite numbers cause ingestion to fail with a row/field error. Schema changes require an explicit mapping update and revalidation.

| Source field | Canonical field | Type | Unit | Null policy | Interpretation |
| --- | --- | --- | --- | --- | --- |
| OrderDate | order_date | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Year | year | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| YearMonth | month | YYYY-MM period | Identifier / category | Required | Reporting month; filter numerator and denominator consistently. |
| Category | category | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Seller | seller | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| ProductID | product_id | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Orders | orders | Decimal | Count | Required | Additive fact amount/count. |
| Units Sold | units | Decimal | Count | Required | Additive fact amount/count. |
| GMV | gmv | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |
| Marketplace Revenue | platform_revenue | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |
| Take Rate % | source_take_rate | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| AOV | source_aov | Decimal | USD (portfolio assumption) | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |

## Business rules and metric arithmetic

| Metric | Formula | Interpretation / boundary |
| --- | --- | --- |
| GMV | Sum gmv | Gross merchandise value is distinct from platform revenue; do not add both as total company revenue. |
| Platform revenue | Sum platform_revenue | Use the supplied platform revenue amounts; do not recalculate from rounded row rates. |
| Weighted take rate | Sum platform_revenue / Sum gmv | Return null for zero GMV; do not average source_take_rate. |
| Average order value | Sum gmv / Sum orders | Use counted orders; units are not the denominator. |
| Product concentration | Product GMV / total GMV | Rank products on the selected period; ties use product_id for stable ordering. |

Counts and monetary values are summed before division. Rates are stored as fractions and formatted as percentages at presentation. Reconciliation tolerance is $0.01 for monetary totals and zero for record counts. Source rates may be rounded; they are retained for comparison rather than averaged.

## Detailed requirements

### MKT-REQ-01: Ingest marketplace records

- **Priority / owner:** Must / Marketplace Operations Manager.
- **Behavior:** Load the 12 supplied source fields into the canonical schema and retain row lineage.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** Every source record has one source_row and the aggregate GMV reconciles within $0.01.
- **Exception and boundary behavior:** Missing source columns stop ingestion; source rows are retained when no order business key exists.
- **Traceability:** MKT-US-01; MKT-UAT-01-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### MKT-REQ-02: Separate GMV from platform revenue

- **Priority / owner:** Must / Marketplace Operations Manager.
- **Behavior:** Present GMV and platform revenue as separately labeled measures.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** Portfolio totals match Q01 and neither measure is described as profit.
- **Exception and boundary behavior:** GMV and platform revenue must remain separate even when both are positive.
- **Traceability:** MKT-US-02; MKT-UAT-02-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### MKT-REQ-03: Calculate weighted take rate

- **Priority / owner:** Must / Marketplace Operations Manager.
- **Behavior:** Calculate aggregate take rate from summed platform revenue divided by summed GMV.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** A two-row fixture with unequal GMV produces the ratio of sums; zero GMV returns null.
- **Exception and boundary behavior:** Unequal GMV weights must not become an average of row take rates; zero GMV returns null.
- **Traceability:** MKT-US-03; MKT-UAT-03-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### MKT-REQ-04: Review seller concentration

- **Priority / owner:** Must / Marketplace Operations Manager.
- **Behavior:** Rank sellers by GMV and show GMV share, orders, and weighted take rate.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** Seller GMV sums to the portfolio GMV; all shares sum to 1 within tolerance.
- **Exception and boundary behavior:** A seller with zero GMV has undefined share/rate where its denominator is zero.
- **Traceability:** MKT-US-04; MKT-UAT-04-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### MKT-REQ-05: Identify product contribution

- **Priority / owner:** Should / Marketplace Operations Manager.
- **Behavior:** Rank products and expose cumulative contribution for concentration review.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q04.csv and SQL/Q04.sql.
- **Acceptance criteria:** Cumulative share is nondecreasing and the final row reaches 1.
- **Exception and boundary behavior:** Ties sort by product_id; the final cumulative share reaches 1 when total GMV is positive.
- **Traceability:** MKT-US-05; MKT-UAT-05-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### MKT-REQ-06: Show monthly changes

- **Priority / owner:** Should / Marketplace Operations Manager.
- **Behavior:** Show monthly GMV and previous-month change within the supplied period.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** First month has no prior comparison; months sort chronologically.
- **Exception and boundary behavior:** First month has no change; production comparisons require adjacent months and complete coverage.
- **Traceability:** MKT-US-06; MKT-UAT-06-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### MKT-REQ-07: Govern extracts and access

- **Priority / owner:** Must / Marketplace Operations Manager.
- **Behavior:** Restrict seller-level exports to approved operations roles and record the refresh version.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** A future role test denies viewer export and records an audit event; current CSV prototype is local only.
- **Exception and boundary behavior:** Reject unauthorized seller export; request reauthentication and audit the denial in the proposed application.
- **Traceability:** MKT-US-07; MKT-UAT-07-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.

### MKT-REQ-08: Explain review actions

- **Priority / owner:** Should / Marketplace Operations Manager.
- **Behavior:** Provide a review queue that separates observed concentration from untested commercial hypotheses.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** Every recommendation identifies an owner, supporting result, uncertainty, and next validation step.
- **Exception and boundary behavior:** High contribution alone does not prove poor seller performance or justify a fee change.
- **Traceability:** MKT-US-08; MKT-UAT-08-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.


## Shared error behavior

A missing required input is an ingestion exception. A ratio with zero denominator is null, displayed as 'Undefined'; it is not a zero performance rate. Empty selections show 'No records' with counts, rather than a successful-looking blank dashboard. Unknown categories and invalid month strings are quarantined in the proposed production contract. The local prototype raises errors for missing required input and records domain exceptions in its profile.

The SQL prototype uses SQLite 3.25+ window functions. It runs against a complete supplied extract in memory. Proposed interactive filters are specified in the BI design and must be tested when implemented; the static result exports are not a filterable production application.
