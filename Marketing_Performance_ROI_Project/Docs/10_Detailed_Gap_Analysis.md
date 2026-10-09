# Detailed gap analysis: Advertising Efficiency and Budget Review

## Decision and assessment basis

Which ad groups should be reviewed for a controlled budget test, and what cost/attribution gaps prevent a full ROI claim?

This analysis compares the delivered local system and supplied data with the controls needed for a production or expanded capability. Source/schema limits and implemented code are observed. Organizational reporting problems, staffing constraints, approval authority, and benefit baselines require discovery; they are not represented as facts from interviews.

## Current-state capabilities

The local application has a persistent SQLite database, four authenticated roles, filtered analytical queries, source-row drilldowns, CSV export, editable UAT, analyst submission, reviewer approval/rejection, gap closure review, optimistic version checks, and audit records. Refresh validates all sources before replacing persistent facts. Business approvals and UAT executions remain unseeded so you can practice honestly.

## Current-to-target matrix

| Gap ID / category | Current state | Target state | Business impact | Priority / owner |
| --- | --- | --- | --- | --- |
| ADS-GAP-01 / Data | Attributed revenue is present; attribution window and event keys are unknown. | Agree conversion window, campaign identifiers, and revenue reconciliation. | Cross-channel ROAS comparisons may use incompatible populations. | P1 - release control / Marketing Operations Manager |
| ADS-GAP-02 / Data / metrics | Revenue minus spend excludes COGS, returns, fees, and overhead. | Add approved cost inputs before reporting full business ROI. | Ad-only contribution may be mistaken for net profit. | P2 - capability improvement / Marketing Operations Manager |
| ADS-GAP-03 / Business process | High observed ROAS has no randomized/holdout evidence. | Run a capped budget pilot with a holdout, stop rules, and saturation review. | Observed efficiency does not prove marginal return on extra spend. | P2 - capability improvement / Marketing Operations Manager |
| ADS-GAP-04 / Technology | The local dashboard recalculates filters and exposes lineage. Historical PBIX/TWB files are unverified. | Rebuild the native semantic model and verify filters, measures, accessibility, and exports. | A historical native dashboard may differ from canonical SQL. | P2 - capability improvement / BI Engineer |
| ADS-GAP-05 / Security / controls | Local accounts and backend role checks are implemented. Enterprise SSO and business-scope RLS are absent. | Configure approved identity, least-privilege business scope, export policy, and revoked-access behavior. | Local account controls do not establish enterprise deployment readiness. | P1 - release control / Security / Control Reviewer |
| ADS-GAP-06 / People / acceptance | 144 planned UAT cases are seeded Not executed. The app records executions, evidence, and independent reviews. | Execute representative tasks with actual business reviewers and resolve defects. | A technical pass does not establish user acceptance. | P1 - release control / Marketing Operations Manager |
| ADS-GAP-07 / Operations | Admin can refresh sources transactionally; hashes and refresh runs persist. Unattended scheduling is external. | Agree refresh frequency, monitoring owner, retention, backup, and rollback expectations. | A failed upstream export may leave stale reporting without agreed escalation. | P2 - capability improvement / Operations Owner |
| ADS-GAP-08 / Benefits | No measured production reporting time, task success, or adoption baseline exists. | Collect comparable baseline and pilot measurements before claiming benefits. | No realized time saving, uplift, or forecast improvement can be asserted. | P2 - capability improvement / Marketing Operations Manager |

## Prioritization and dependency logic

P1 gaps protect release correctness, authorized access, or business acceptance. Resolve them before claiming a production release. P2 gaps extend capability or permit benefits measurement. No fabricated implementation cost, duration, or ROI is assigned. Estimate work after source access, platform choices, owner availability, and test environment are agreed.

Sequence: confirm source contracts and definitions; certify native reporting if needed; configure production identity/scope; execute business UAT; agree operational handoff; measure pilot benefits. A future profitability, causal, or forecasting extension must obtain the additional fields identified above before its metric is advertised.

## Requirement and closure evidence

| Gap | Requirement | Dependency | Closure criteria |
| --- | --- | --- | --- |
| ADS-GAP-01 | ADS-REQ-01 | Obtain campaign IDs, attribution windows, order-level revenue, returns, COGS, agency fees, and experiment assignments before full ROI or incrementality reporting. | Marketing and Finance approve the attribution contract and reconciliation. |
| ADS-GAP-02 | ADS-REQ-07 | Obtain campaign IDs, attribution windows, order-level revenue, returns, COGS, agency fees, and experiment assignments before full ROI or incrementality reporting. | A reconciled cost bridge supports the new metric; existing labels remain accurate. |
| ADS-GAP-03 | ADS-REQ-06 | Obtain campaign IDs, attribution windows, order-level revenue, returns, COGS, agency fees, and experiment assignments before full ROI or incrementality reporting. | Pilot assignment, actual spend, guardrails, and approved interpretation are recorded. |
| ADS-GAP-04 | ADS-REQ-02 | Approved platform, accountable owner, and representative environment | Native measure totals reconcile to Q01-Q05 and interactive/access test evidence is retained. |
| ADS-GAP-05 | ADS-REQ-08 | Approved platform, accountable owner, and representative environment | Positive/negative scope tests, revocation, and export checks pass in the chosen environment. |
| ADS-GAP-06 | ADS-REQ-04 | Approved platform, accountable owner, and representative environment | Actual UAT evidence, reviewer identity, defect dispositions, and sponsor decision are recorded. |
| ADS-GAP-07 | ADS-REQ-01 | Approved platform, accountable owner, and representative environment | Scheduled run and failure alert are exercised; restore a backup and reconcile controls. |
| ADS-GAP-08 | ADS-REQ-05 | Approved platform, accountable owner, and representative environment | Baseline and pilot measures include comparable populations, sample sizes, and uncertainty. |

Each linked requirement also has three UAT cases in the delivery register. Gap closure is a separate decision: an approved local requirement does not automatically close every related production gap. In the application, the analyst proposes closure with evidence and the reviewer records Closed or Open with rationale. The audit log retains both actions.

## Options and recommendation

Option 1: keep the local workbench as a portfolio simulation. It provides executable analytical/workflow evidence without a paid platform. Option 2: certify one native BI/CRM sandbox as the next project, keeping the canonical definitions and tests. Option 3: pursue full enterprise deployment with approved identity, source contracts, operations, and stakeholders. Recommend Option 1 now, then one focused sandbox pilot rather than imply production maturity from documentation.

## Measurement plan

Track unresolved P1 gaps, requirements awaiting independent review, UAT outcomes with evidence, refresh failures, and unresolved source differences. Measure user task completion and preparation/review time over comparable baseline and pilot cycles before assigning economic value. Record the reporting population, period, and denominator for every metric.

[Gap register](../Delivery/gap_register.csv) · [Functional specification](02_Functional_and_Data_Specification.md) · [Local system guide](../../Local_System/README.md)
