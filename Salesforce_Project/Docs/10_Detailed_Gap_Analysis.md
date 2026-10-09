# Detailed gap analysis: CRM Pipeline Definitions and Forecast Readiness

## Decision and assessment basis

What is the current open pipeline and weighted open pipeline, and what additional CRM fields are needed before forecasting timing or conversion?

This analysis compares the delivered local system and supplied data with the controls needed for a production or expanded capability. Source/schema limits and implemented code are observed. Organizational reporting problems, staffing constraints, approval authority, and benefit baselines require discovery; they are not represented as facts from interviews.

## Current-state capabilities

The local application has a persistent SQLite database, four authenticated roles, filtered analytical queries, source-row drilldowns, CSV export, editable UAT, analyst submission, reviewer approval/rejection, gap closure review, optimistic version checks, and audit records. Refresh validates all sources before replacing persistent facts. Business approvals and UAT executions remain unseeded so you can practice honestly.

## Current-to-target matrix

| Gap ID / category | Current state | Target state | Business impact | Priority / owner |
| --- | --- | --- | --- | --- |
| CRM-GAP-01 / Data | Ten opportunity records have no close/snapshot dates or stage history. | Add dated snapshots, expected close dates, and history before forecasting timing. | Velocity, time-bounded forecast, and historical win rate cannot be established. | P1 - release control / Sales Operations Manager |
| CRM-GAP-02 / Data / metrics | Stage probabilities are supplied, not calibrated to historical outcomes. | Review stage policy and calibrate on approved history. | Weighted open value is a scenario rather than a validated forecast. | P2 - capability improvement / Sales Operations Manager |
| CRM-GAP-03 / Business process | Local fixtures validate stage/probability; Salesforce is not configured. | Implement mandatory close fields and validation in a Salesforce sandbox. | The live CRM could still accept invalid stage/probability combinations. | P2 - capability improvement / Sales Operations Manager |
| CRM-GAP-04 / Technology | The local dashboard recalculates filters and exposes lineage. Historical PBIX/TWB files are unverified. | Rebuild the native semantic model and verify filters, measures, accessibility, and exports. | A historical native dashboard may differ from canonical SQL. | P2 - capability improvement / BI Engineer |
| CRM-GAP-05 / Security / controls | Local accounts and backend role checks are implemented. Enterprise SSO and business-scope RLS are absent. | Configure approved identity, least-privilege business scope, export policy, and revoked-access behavior. | Local account controls do not establish enterprise deployment readiness. | P1 - release control / Security / Control Reviewer |
| CRM-GAP-06 / People / acceptance | 144 planned UAT cases are seeded Not executed. The app records executions, evidence, and independent reviews. | Execute representative tasks with actual business reviewers and resolve defects. | A technical pass does not establish user acceptance. | P1 - release control / Sales Operations Manager |
| CRM-GAP-07 / Operations | Admin can refresh sources transactionally; hashes and refresh runs persist. Unattended scheduling is external. | Agree refresh frequency, monitoring owner, retention, backup, and rollback expectations. | A failed upstream export may leave stale reporting without agreed escalation. | P2 - capability improvement / Operations Owner |
| CRM-GAP-08 / Benefits | No measured production reporting time, task success, or adoption baseline exists. | Collect comparable baseline and pilot measurements before claiming benefits. | No realized time saving, uplift, or forecast improvement can be asserted. | P2 - capability improvement / Sales Operations Manager |

## Prioritization and dependency logic

P1 gaps protect release correctness, authorized access, or business acceptance. Resolve them before claiming a production release. P2 gaps extend capability or permit benefits measurement. No fabricated implementation cost, duration, or ROI is assigned. Estimate work after source access, platform choices, owner availability, and test environment are agreed.

Sequence: confirm source contracts and definitions; certify native reporting if needed; configure production identity/scope; execute business UAT; agree operational handoff; measure pilot benefits. A future profitability, causal, or forecasting extension must obtain the additional fields identified above before its metric is advertised.

## Requirement and closure evidence

| Gap | Requirement | Dependency | Closure criteria |
| --- | --- | --- | --- |
| CRM-GAP-01 | CRM-REQ-06 | Add snapshot_date, owner_id, created_date, expected_close_date, stage_history, loss_reason, account_id, and approved probability policy before time-bounded forecasting. | Date/history fields are validated and the forecast cohort is documented. |
| CRM-GAP-02 | CRM-REQ-03 | Add snapshot_date, owner_id, created_date, expected_close_date, stage_history, loss_reason, account_id, and approved probability policy before time-bounded forecasting. | Sales Ops approves policy; hold-out evaluation and closed-stage rules pass. |
| CRM-GAP-03 | CRM-REQ-07 | Add snapshot_date, owner_id, created_date, expected_close_date, stage_history, loss_reason, account_id, and approved probability policy before time-bounded forecasting. | Sandbox tests block Closed Won below 1 and Closed Lost above 0; retain screenshots/logs. |
| CRM-GAP-04 | CRM-REQ-02 | Approved platform, accountable owner, and representative environment | Native measure totals reconcile to Q01-Q05 and interactive/access test evidence is retained. |
| CRM-GAP-05 | CRM-REQ-08 | Approved platform, accountable owner, and representative environment | Positive/negative scope tests, revocation, and export checks pass in the chosen environment. |
| CRM-GAP-06 | CRM-REQ-04 | Approved platform, accountable owner, and representative environment | Actual UAT evidence, reviewer identity, defect dispositions, and sponsor decision are recorded. |
| CRM-GAP-07 | CRM-REQ-01 | Approved platform, accountable owner, and representative environment | Scheduled run and failure alert are exercised; restore a backup and reconcile controls. |
| CRM-GAP-08 | CRM-REQ-05 | Approved platform, accountable owner, and representative environment | Baseline and pilot measures include comparable populations, sample sizes, and uncertainty. |

Each linked requirement also has three UAT cases in the delivery register. Gap closure is a separate decision: an approved local requirement does not automatically close every related production gap. In the application, the analyst proposes closure with evidence and the reviewer records Closed or Open with rationale. The audit log retains both actions.

## Options and recommendation

Option 1: keep the local workbench as a portfolio simulation. It provides executable analytical/workflow evidence without a paid platform. Option 2: certify one native BI/CRM sandbox as the next project, keeping the canonical definitions and tests. Option 3: pursue full enterprise deployment with approved identity, source contracts, operations, and stakeholders. Recommend Option 1 now, then one focused sandbox pilot rather than imply production maturity from documentation.

## Measurement plan

Track unresolved P1 gaps, requirements awaiting independent review, UAT outcomes with evidence, refresh failures, and unresolved source differences. Measure user task completion and preparation/review time over comparable baseline and pilot cycles before assigning economic value. Record the reporting population, period, and denominator for every metric.

[Gap register](../Delivery/gap_register.csv) · [Functional specification](02_Functional_and_Data_Specification.md) · [Local system guide](../../Local_System/README.md)
