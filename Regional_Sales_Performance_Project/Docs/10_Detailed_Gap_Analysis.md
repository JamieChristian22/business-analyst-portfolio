# Detailed gap analysis: Restaurant Sales Reporting by City and Zone

## Decision and assessment basis

Which restaurants and zones require a manager review, and are observed monthly changes supported by comparable records?

This analysis compares the delivered local system and supplied data with the controls needed for a production or expanded capability. Source/schema limits and implemented code are observed. Organizational reporting problems, staffing constraints, approval authority, and benefit baselines require discovery; they are not represented as facts from interviews.

## Current-state capabilities

The local application has a persistent SQLite database, four authenticated roles, filtered analytical queries, source-row drilldowns, CSV export, editable UAT, analyst submission, reviewer approval/rejection, gap closure review, optimistic version checks, and audit records. Refresh validates all sources before replacing persistent facts. Business approvals and UAT executions remain unseeded so you can practice honestly.

## Current-to-target matrix

| Gap ID / category | Current state | Target state | Business impact | Priority / owner |
| --- | --- | --- | --- | --- |
| REG-GAP-01 / Data | Sales records have no monthly targets, costs, reps, or prior-year data. | Obtain approved targets and prior-year inputs before adding attainment/YoY metrics. | Unsupported target and YoY judgments would misrepresent the source. | P1 - release control / Sales Operations Manager |
| REG-GAP-02 / Data / metrics | All 220 restaurants report six months; operating days and closures are unknown. | Add operating calendar and comparable-store flags. | Complete rows do not establish comparable store performance. | P2 - capability improvement / Sales Operations Manager |
| REG-GAP-03 / Business process | Current restaurant-to-city/zone mapping is stable in this snapshot. | Define effective-dated mappings for future zone transfers. | A future transfer may double-count sales or restrict the wrong users. | P2 - capability improvement / Sales Operations Manager |
| REG-GAP-04 / Technology | The local dashboard recalculates filters and exposes lineage. Historical PBIX/TWB files are unverified. | Rebuild the native semantic model and verify filters, measures, accessibility, and exports. | A historical native dashboard may differ from canonical SQL. | P2 - capability improvement / BI Engineer |
| REG-GAP-05 / Security / controls | Local accounts and backend role checks are implemented. Enterprise SSO and business-scope RLS are absent. | Configure approved identity, least-privilege business scope, export policy, and revoked-access behavior. | Local account controls do not establish enterprise deployment readiness. | P1 - release control / Security / Control Reviewer |
| REG-GAP-06 / People / acceptance | 144 planned UAT cases are seeded Not executed. The app records executions, evidence, and independent reviews. | Execute representative tasks with actual business reviewers and resolve defects. | A technical pass does not establish user acceptance. | P1 - release control / Sales Operations Manager |
| REG-GAP-07 / Operations | Admin can refresh sources transactionally; hashes and refresh runs persist. Unattended scheduling is external. | Agree refresh frequency, monitoring owner, retention, backup, and rollback expectations. | A failed upstream export may leave stale reporting without agreed escalation. | P2 - capability improvement / Operations Owner |
| REG-GAP-08 / Benefits | No measured production reporting time, task success, or adoption baseline exists. | Collect comparable baseline and pilot measurements before claiming benefits. | No realized time saving, uplift, or forecast improvement can be asserted. | P2 - capability improvement / Sales Operations Manager |

## Prioritization and dependency logic

P1 gaps protect release correctness, authorized access, or business acceptance. Resolve them before claiming a production release. P2 gaps extend capability or permit benefits measurement. No fabricated implementation cost, duration, or ROI is assigned. Estimate work after source access, platform choices, owner availability, and test environment are agreed.

Sequence: confirm source contracts and definitions; certify native reporting if needed; configure production identity/scope; execute business UAT; agree operational handoff; measure pilot benefits. A future profitability, causal, or forecasting extension must obtain the additional fields identified above before its metric is advertised.

## Requirement and closure evidence

| Gap | Requirement | Dependency | Closure criteria |
| --- | --- | --- | --- |
| REG-GAP-01 | REG-REQ-06 | Obtain monthly targets, store operating calendar, closures, currency, comparable-store flags, costs, and prior-year sales before extending performance conclusions. | New sources reconcile; target and comparable-period formulas pass boundary cases. |
| REG-GAP-02 | REG-REQ-05 | Obtain monthly targets, store operating calendar, closures, currency, comparable-store flags, costs, and prior-year sales before extending performance conclusions. | Managers approve comparability flags and missing/closed-store test cases. |
| REG-GAP-03 | REG-REQ-01 | Obtain monthly targets, store operating calendar, closures, currency, comparable-store flags, costs, and prior-year sales before extending performance conclusions. | Mapping tests preserve total sales and assigned scope across transfer dates. |
| REG-GAP-04 | REG-REQ-02 | Approved platform, accountable owner, and representative environment | Native measure totals reconcile to Q01-Q05 and interactive/access test evidence is retained. |
| REG-GAP-05 | REG-REQ-08 | Approved platform, accountable owner, and representative environment | Positive/negative scope tests, revocation, and export checks pass in the chosen environment. |
| REG-GAP-06 | REG-REQ-04 | Approved platform, accountable owner, and representative environment | Actual UAT evidence, reviewer identity, defect dispositions, and sponsor decision are recorded. |
| REG-GAP-07 | REG-REQ-01 | Approved platform, accountable owner, and representative environment | Scheduled run and failure alert are exercised; restore a backup and reconcile controls. |
| REG-GAP-08 | REG-REQ-05 | Approved platform, accountable owner, and representative environment | Baseline and pilot measures include comparable populations, sample sizes, and uncertainty. |

Each linked requirement also has three UAT cases in the delivery register. Gap closure is a separate decision: an approved local requirement does not automatically close every related production gap. In the application, the analyst proposes closure with evidence and the reviewer records Closed or Open with rationale. The audit log retains both actions.

## Options and recommendation

Option 1: keep the local workbench as a portfolio simulation. It provides executable analytical/workflow evidence without a paid platform. Option 2: certify one native BI/CRM sandbox as the next project, keeping the canonical definitions and tests. Option 3: pursue full enterprise deployment with approved identity, source contracts, operations, and stakeholders. Recommend Option 1 now, then one focused sandbox pilot rather than imply production maturity from documentation.

## Measurement plan

Track unresolved P1 gaps, requirements awaiting independent review, UAT outcomes with evidence, refresh failures, and unresolved source differences. Measure user task completion and preparation/review time over comparable baseline and pilot cycles before assigning economic value. Record the reporting population, period, and denominator for every metric.

[Gap register](../Delivery/gap_register.csv) · [Functional specification](02_Functional_and_Data_Specification.md) · [Local system guide](../../Local_System/README.md)
