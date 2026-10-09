# Functional and data specification

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Data contract

Anonymous source observation with binary funnel counts. There is no customer/session identifier; totals count observations and cannot establish distinct customers across periods.

`source_row` is an integer lineage identifier assigned to the data record after the CSV header. It is never presented as a customer, order, or opportunity business key. Required blank fields or nonfinite numbers cause ingestion to fail with a row/field error. Schema changes require an explicit mapping update and revalidation.

| Source field | Canonical field | Type | Unit | Null policy | Interpretation |
| --- | --- | --- | --- | --- | --- |
| YearMonth | month | YYYY-MM period | Identifier / category | Required | Reporting month; filter numerator and denominator consistently. |
| device_type | device | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| acquisition_channel | channel | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| country | country | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| category | category | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| product_id | product_id | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Viewed Customers | views | Decimal | Count | Required | Additive fact amount/count. |
| Cart Customers | carts | Decimal | Count | Required | Additive fact amount/count. |
| Checkout Customers | checkouts | Decimal | Count | Required | Additive fact amount/count. |
| Purchased Customers | purchases | Decimal | Count | Required | Additive fact amount/count. |
| Total Revenue | revenue | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |
| Profit | profit | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |
| Total Orders | orders | Decimal | Count | Required | Additive fact amount/count. |
| Profit Margin | source_margin | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| View → Cart % | source_view_cart | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Cart → Checkout % | source_cart_checkout | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Checkout → Purchase % | source_checkout_purchase | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Drop-off (Views→Cart) | source_drop_view_cart | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Drop-off (Cart→Checkout) | source_drop_cart_checkout | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Drop-off (Checkout→Purchase) | source_drop_checkout_purchase | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Funnel Metric | funnel_metric | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Stage | stage_label | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| AOV | source_aov | Decimal | USD (portfolio assumption) | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |

## Business rules and metric arithmetic

| Metric | Formula | Interpretation / boundary |
| --- | --- | --- |
| View-to-cart rate | Sum carts / Sum views | Counts represent observations; do not average row rates. |
| Cart-to-checkout rate | Sum checkouts / Sum carts | Return null if there are no cart observations. |
| Checkout-to-purchase rate | Sum purchases / Sum checkouts | Use the same device/period filter on numerator and denominator. |
| Profit margin | Sum profit / Sum revenue | Profit uses the source definition; no independent cost reconciliation is available. |
| Average order value | Sum revenue / Sum orders | Zero orders returns null; a blank amount is an ingestion exception. |

Counts and monetary values are summed before division. Rates are stored as fractions and formatted as percentages at presentation. Reconciliation tolerance is $0.01 for monetary totals and zero for record counts. Source rates may be rounded; they are retained for comparison rather than averaged.

## Detailed requirements

### ECOM-REQ-01: Preserve anonymous observations

- **Priority / owner:** Must / Checkout Product Manager.
- **Behavior:** Load every observation with source lineage without deleting repeated rows.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** Row count equals the source count; repeated-row count is profiled and disclosed.
- **Exception and boundary behavior:** Repeated anonymous rows are retained because no event key proves duplication.
- **Traceability:** ECOM-US-01; ECOM-UAT-01-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ECOM-REQ-02: Define a monotonic funnel

- **Priority / owner:** Must / Checkout Product Manager.
- **Behavior:** Validate views >= carts >= checkouts >= purchases >= 0 per observation.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** Every violating observation is reported; the supplied file passes or is explicitly flagged.
- **Exception and boundary behavior:** A later stage greater than an earlier stage is a data exception, not a valid funnel.
- **Traceability:** ECOM-US-02; ECOM-UAT-02-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ECOM-REQ-03: Calculate funnel rates

- **Priority / owner:** Must / Checkout Product Manager.
- **Behavior:** Calculate each transition as a ratio of summed stage counts.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Zero denominators return null; a weighted fixture matches independently calculated results.
- **Exception and boundary behavior:** Zero prior-stage count produces undefined transition rate, never zero conversion by default.
- **Traceability:** ECOM-US-03; ECOM-UAT-03-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ECOM-REQ-04: Compare devices

- **Priority / owner:** Must / Checkout Product Manager.
- **Behavior:** Show device-level stage counts and rates with denominators visible.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Device stage counts reconcile to portfolio totals and comparisons use identical periods.
- **Exception and boundary behavior:** A small device denominator remains visible; a device with no observations is labeled No records.
- **Traceability:** ECOM-US-04; ECOM-UAT-04-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ECOM-REQ-05: Inspect acquisition mix

- **Priority / owner:** Should / Checkout Product Manager.
- **Behavior:** Compare channels using revenue, orders, funnel counts, and margin.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** Channel revenue sums to total; low sample counts are visible.
- **Exception and boundary behavior:** Profit uses the supplied definition; do not assume shipping, returns, or overhead are reconciled.
- **Traceability:** ECOM-US-05; ECOM-UAT-05-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ECOM-REQ-06: Track monthly conversion

- **Priority / owner:** Should / Checkout Product Manager.
- **Behavior:** Show purchase/view conversion and prior-month revenue change.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q04.csv and SQL/Q04.sql.
- **Acceptance criteria:** The first month has null prior-month change and no missing month is silently treated as zero.
- **Exception and boundary behavior:** Missing months must be shown in the proposed calendar; no fabricated zeros or prior-year comparisons.
- **Traceability:** ECOM-US-06; ECOM-UAT-06-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ECOM-REQ-07: Specify an experiment

- **Priority / owner:** Should / Checkout Product Manager.
- **Behavior:** Document one investigation hypothesis, randomization unit, success metric, guardrails, and instrumentation gaps.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** No claim of experiment success is made without assignment/exposure events; launch remains pending.
- **Exception and boundary behavior:** Exposure and assignment must exist before any A/B effect can be estimated.
- **Traceability:** ECOM-US-07; ECOM-UAT-07-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.

### ECOM-REQ-08: Protect customer data

- **Priority / owner:** Must / Checkout Product Manager.
- **Behavior:** Define minimal identifiers and approved retention for proposed event tracking.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** Future design excludes raw contact data from analyst exports and requires a privacy review.
- **Exception and boundary behavior:** Future analyst exports must exclude direct identifiers and respect approved retention.
- **Traceability:** ECOM-US-08; ECOM-UAT-08-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.


## Shared error behavior

A missing required input is an ingestion exception. A ratio with zero denominator is null, displayed as 'Undefined'; it is not a zero performance rate. Empty selections show 'No records' with counts, rather than a successful-looking blank dashboard. Unknown categories and invalid month strings are quarantined in the proposed production contract. The local prototype raises errors for missing required input and records domain exceptions in its profile.

The SQL prototype uses SQLite 3.25+ window functions. It runs against a complete supplied extract in memory. Proposed interactive filters are specified in the BI design and must be tested when implemented; the static result exports are not a filterable production application.
