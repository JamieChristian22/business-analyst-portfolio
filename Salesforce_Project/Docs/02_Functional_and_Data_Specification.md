# Functional and data specification

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Data contract

One current opportunity snapshot identified by Opportunity. There are ten records; no snapshot date or stage history is supplied.

`source_row` is an integer lineage identifier assigned to the data record after the CSV header. It is never presented as a customer, order, or opportunity business key. Required blank fields or nonfinite numbers cause ingestion to fail with a row/field error. Schema changes require an explicit mapping update and revalidation.

| Source field | Canonical field | Type | Unit | Null policy | Interpretation |
| --- | --- | --- | --- | --- | --- |
| Opportunity | opportunity_id | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Stage | stage | Text | Identifier / category | Required | Source classification; retain original spelling and exact identifiers. |
| Amount | amount | Decimal | USD (portfolio assumption) | Required | Additive fact amount/count. |
| Probability | probability | Decimal | Fraction 0-1 | Required | Additive fact amount/count. |

## Business rules and metric arithmetic

| Metric | Formula | Interpretation / boundary |
| --- | --- | --- |
| Open pipeline | Sum amount excluding Closed Won and Closed Lost | Closed outcomes appear separately. |
| Weighted open pipeline | Sum amount * probability for open stages | This is a probability-weighted scenario amount, not booked revenue. |
| Closed won amount | Sum amount where Closed Won | Do not add it to open pipeline when describing future opportunity value. |
| Closed lost amount | Sum amount where Closed Lost | Explain known outcomes without inferring loss causes. |
| Probability | Decimal from 0 to 1 | Closed Won requires 1; Closed Lost requires 0; invalid records are rejected in production design. |

Counts and monetary values are summed before division. Rates are stored as fractions and formatted as percentages at presentation. Reconciliation tolerance is $0.01 for monetary totals and zero for record counts. Source rates may be rounded; they are retained for comparison rather than averaged.

## Detailed requirements

### CRM-REQ-01: Validate opportunity records

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Require unique opportunity_id, allowed stages, numeric amount, and bounded probability.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** Duplicate IDs and probability outside 0-1 are detected; supplied records are profiled.
- **Exception and boundary behavior:** Duplicate opportunity IDs, unknown stages, and invalid probabilities require correction.
- **Traceability:** CRM-US-01; CRM-UAT-01-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### CRM-REQ-02: Separate open and closed values

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Calculate open pipeline, closed won, and closed lost as distinct categories.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Open + won + lost equals all-record amount within $0.01.
- **Exception and boundary behavior:** Closed won and closed lost are excluded from open totals even if amounts are positive.
- **Traceability:** CRM-US-02; CRM-UAT-02-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### CRM-REQ-03: Calculate weighted open pipeline

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Multiply each open opportunity amount by its own probability before summing.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q02.csv and SQL/Q02.sql.
- **Acceptance criteria:** Fixed unequal-amount fixture matches sum of products; closed values are excluded.
- **Exception and boundary behavior:** Use sum(amount * probability), not total amount multiplied by average probability.
- **Traceability:** CRM-US-03; CRM-UAT-03-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### CRM-REQ-04: Review stage concentration

- **Priority / owner:** Should / Sales Operations Manager.
- **Behavior:** Show opportunity count, amount, and weighted amount for each stage.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q03.csv and SQL/Q03.sql.
- **Acceptance criteria:** Stage amounts reconcile; counts total the source record count.
- **Exception and boundary behavior:** Counts and amounts have separate labels; small stage samples do not imply stable rates.
- **Traceability:** CRM-US-04; CRM-UAT-04-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### CRM-REQ-05: Create opportunity review queue

- **Priority / owner:** Should / Sales Operations Manager.
- **Behavior:** Rank open opportunities by weighted amount with stable ID tie handling.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q04.csv and SQL/Q04.sql.
- **Acceptance criteria:** Only open stages appear and each value is traceable to one source record.
- **Exception and boundary behavior:** Tied weighted amounts sort by opportunity_id; closed opportunities never enter open review queue.
- **Traceability:** CRM-US-05; CRM-UAT-05-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### CRM-REQ-06: Expose forecast limitations

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Display missing timing and history fields in the forecast-readiness checklist.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** Analysis/Q01.csv and SQL/Q01.sql.
- **Acceptance criteria:** No sales velocity, historical win rate, or time-bounded forecast is claimed.
- **Exception and boundary behavior:** An undated snapshot cannot support velocity or a time-bounded revenue forecast.
- **Traceability:** CRM-US-06; CRM-UAT-06-A/B/C.
- **Implementation status:** Executed SQL evidence exists; full application behavior is not implemented.

### CRM-REQ-07: Specify stage controls

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Design validation rules for stage/probability and record mandatory close reason/date fields.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** Closed Won with probability below 1 and Closed Lost above 0 are blocked in fixture/design tests.
- **Exception and boundary behavior:** Closed Won requires probability 1; Closed Lost requires 0. Mandatory close fields are future implementation requirements.
- **Traceability:** CRM-US-07; CRM-UAT-07-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.

### CRM-REQ-08: Define CRM role controls

- **Priority / owner:** Must / Sales Operations Manager.
- **Behavior:** Document owner/manager/admin permissions and audit changes to probability.
- **Trigger:** A new approved extract, filter selection, review action, or attempted export relevant to this requirement.
- **Inputs:** The canonical schema below; use the same source version and reporting population on both sides of a comparison.
- **Output / evidence:** System design and planned future application control test.
- **Acceptance criteria:** Future role tests prevent unauthorized forecast edits; local CSV prototype does not enforce CRM roles.
- **Exception and boundary behavior:** Only authorized roles may edit probability or stage in a future CRM configuration; audit all changes.
- **Traceability:** CRM-US-08; CRM-UAT-08-A/B/C.
- **Implementation status:** Design only. No live system or access enforcement is claimed.


## Shared error behavior

A missing required input is an ingestion exception. A ratio with zero denominator is null, displayed as 'Undefined'; it is not a zero performance rate. Empty selections show 'No records' with counts, rather than a successful-looking blank dashboard. Unknown categories and invalid month strings are quarantined in the proposed production contract. The local prototype raises errors for missing required input and records domain exceptions in its profile.

The SQL prototype uses SQLite 3.25+ window functions. It runs against a complete supplied extract in memory. Proposed interactive filters are specified in the BI design and must be tested when implemented; the static result exports are not a filterable production application.
