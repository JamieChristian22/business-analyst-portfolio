# Functional and data specification

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Data contract

Source advertising observation by month, ad group, and device. There is no campaign or event ID; repeated dimension combinations are valid additive records.

`source_row` is an integer lineage identifier assigned to the data record after the CSV header. It is never presented as a customer, order, or opportunity business key. Required blank fields or nonfinite numbers cause ingestion to fail with a row/field error. Schema changes require an explicit mapping update and revalidation.

| Source field | Canonical field | Type | Unit | Null policy | Interpretation |
| --- | --- | --- | --- | --- | --- |
| Month | month | YYYY-MM period | Identifier / category | Required | Reporting month; filter numerator and denominator consistently. |
| Ad Group | ad_group | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Device | device | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Impressions | impressions | Decimal | Count | Required | Additive fact amount/count. |
| Clicks | clicks | Decimal | Count | Required | Additive fact amount/count. |
| CTR | source_ctr | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| CPC | source_cpc | Decimal | USD (portfolio assumption) | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Conv Rate | source_conversion_rate | Decimal | Fraction 0-1 | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| Conversions | conversions | Decimal | Count | Required | Additive fact amount/count. |
| Cost | cost | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |
| Revenue | revenue | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |
| Sale Amount | source_sale_amount | Decimal | USD (portfolio assumption) | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |
| P&L | source_pnl | Decimal | USD (portfolio assumption) | Required | Original source value retained for comparison; aggregate KPIs are recomputed from additive amounts/counts. |

## Business rules and metric arithmetic

| Metric | Formula | Interpretation / boundary |
| --- | --- | --- |
| ROAS | Sum revenue / Sum cost | Return null for zero cost; ratio of sums, not average row ROAS. |
| Ad-only contribution | Sum revenue minus Sum cost | Do not label it company profit; other costs are absent. |
| CTR | Sum clicks / Sum impressions | Use the same period and device selection. |
| CPC | Sum cost / Sum clicks | No-click observations yield null at zero denominator. |
| Conversion rate | Sum conversions / Sum clicks | Observed attributed conversions, not experiment lift. |

Counts and monetary values are summed before division. Rates are stored as fractions and formatted as percentages at presentation. Reconciliation tolerance is $0.01 for monetary totals and zero for record counts. Source rates may be rounded; they are retained for comparison rather than averaged.

## Detailed requirements

### ADS-REQ-01: Load additive ad records

- **Priority / owner:** Must / Marketing Operations Manager.
- **Behavior:** Retain all advertising observations and preserve source row references.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** Revenue and cost control totals reconcile independently to the CSV.
- **Exception and boundary behavior:** Dimension combinations may repeat legitimately; retain source rows rather than grouping during ingestion.
- **Traceability:** ADS-US-01; ADS-UAT-01-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ADS-REQ-02: Calculate weighted efficiency

- **Priority / owner:** Must / Marketing Operations Manager.
- **Behavior:** Calculate ROAS, CTR, CPC, and conversion rate from summed counts/amounts.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Weighted fixtures match independent arithmetic; all zero denominators return null.
- **Exception and boundary behavior:** No spend, no impressions, or no clicks yields undefined corresponding ratios.
- **Traceability:** ADS-US-02; ADS-UAT-02-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ADS-REQ-03: Compare ad groups

- **Priority / owner:** Must / Marketing Operations Manager.
- **Behavior:** Show revenue, cost, ROAS, conversions, and ad-only contribution by group.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Group totals reconcile to the portfolio totals and contribution is correctly labeled.
- **Exception and boundary behavior:** Contribution excludes other business costs; low spend remains visible beside high ROAS.
- **Traceability:** ADS-US-03; ADS-UAT-03-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ADS-REQ-04: Inspect device differences

- **Priority / owner:** Should / Marketing Operations Manager.
- **Behavior:** Compare devices with spend and denominator counts shown.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** Device totals reconcile and no causal explanation is generated automatically.
- **Exception and boundary behavior:** Device mix is observational and cannot establish causal effectiveness.
- **Traceability:** ADS-US-04; ADS-UAT-04-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ADS-REQ-05: Track monthly efficiency

- **Priority / owner:** Should / Marketing Operations Manager.
- **Behavior:** Show monthly spend, revenue, ROAS, and prior-month spend change.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q04.csv and SQL/Q04.sql.
- **Acceptance criteria:** Month order is chronological and first-month change is null.
- **Exception and boundary behavior:** The first month has no prior spend comparison; production changes require complete adjacent months.
- **Traceability:** ADS-US-05; ADS-UAT-05-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ADS-REQ-06: Set budget-test guardrails

- **Priority / owner:** Must / Marketing Operations Manager.
- **Behavior:** Require a controlled pilot with spend caps and an attribution review before reallocation.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** The proposed plan includes approval, holdout strategy, minimum evidence, and a stop rule.
- **Exception and boundary behavior:** A pilot stops at its agreed cap or adverse guardrail; an observational high ROAS is not automatic approval.
- **Traceability:** ADS-US-06; ADS-UAT-06-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.

### ADS-REQ-07: Validate P&L labeling

- **Priority / owner:** Must / Marketing Operations Manager.
- **Behavior:** Explain and reconcile source_pnl to revenue minus cost.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** Every record with a difference above $0.01 is reported and full-profit language is excluded.
- **Exception and boundary behavior:** A source P&L difference above $0.01 is an exception; display both values until resolved.
- **Traceability:** ADS-US-07; ADS-UAT-07-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### ADS-REQ-08: Govern campaign exports

- **Priority / owner:** Must / Marketing Operations Manager.
- **Behavior:** Define analyst/manager access, approved exports, and review ownership.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** A future access test prevents viewer budget edits; prototype CSV has no role enforcement.
- **Exception and boundary behavior:** Unauthorized budget changes are blocked in a future configured system; local CSV has no such control.
- **Traceability:** ADS-US-08; ADS-UAT-08-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.


## Shared error behavior

A missing required input is an ingestion exception. A ratio with zero denominator is null, displayed as 'Undefined'; it is not a zero performance rate. Empty selections show 'No records' with counts, rather than a successful-looking blank dashboard. Unknown categories and invalid month strings are quarantined in the proposed production contract. The local prototype raises errors for missing required input and records domain exceptions in its profile.

The SQL prototype uses SQLite 3.25+ window functions. It runs against a complete supplied extract in memory. Proposed interactive filters are specified in the BI design and must be tested when implemented; the static result exports are not a filterable production application.
