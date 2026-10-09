# Delivery, UAT, and change control

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Delivery status

The local analysis and database-backed workbench are delivered; calculation tests and HTTP integration tests are recorded under Quality. All business UAT cases are **Not executed**. All external approvals are **Pending**. Security, refresh, usability, and accessibility controls are design requirements until implemented in an appropriate environment.

## Backlog and implementation sequence

The backlog contains 8 stories, one per requirement, and 24 planned UAT cases. Story estimates are illustrative relative points, not a promised schedule or actual team velocity. Jira-import CSV fields are provided; map columns in your own Jira instance before import. No live Jira board is created.

| Sequence | Scope | Exit evidence | Dependencies |
| --- | --- | --- | --- |
| 1: Discovery | Confirm source provenance, grain, KPI owner, and scope | Approved definitions and open-question owners | Sponsor and source-owner availability |
| 2: Analysis | Implement canonical mappings, source controls, and calculations | Query exports, fixture tests, exception profile | Confirmed source contract |
| 3: Governed prototype | Build BI views and access policy in a sandbox | Role tests, filters, label review, refresh metadata | Identity model and approved platform |
| 4: Business UAT | Execute planned acceptance and exception cases | Actual results, defects, retest, owner disposition | Representative users and stable candidate build |
| 5: Limited release | Pilot approved reporting and review workflow | Release approval, monitoring, rollback record | All open Must controls resolved |

## Definition of Ready

A story has an agreed business need, owner, priority, source fields, measurable acceptance criteria, exception behavior, dependencies, and test approach. Ambiguous grain or missing required production keys keeps the story in clarification rather than implementation.

## Definition of Done

Code/specification is reviewed; source controls reconcile; positive and negative tests pass; labels match the KPI dictionary; lineage and refresh metadata are present; relevant access and export tests pass; defects have an approved disposition; users execute business UAT; and the accountable owner signs the release record. Completed SQL does not satisfy the entire production Definition of Done.

## UAT procedure

1. Freeze the candidate input hashes, query/build version, environment, and expected controls.
2. Prepare test data separately from the original extract. Never edit source CSVs to make a result pass.
3. Execute each Acceptance, Boundary / exception, and Business review case.
4. Enter actual result, evidence location, tester, and execution date in the UAT register.
5. Log defects with steps, observed versus expected behavior, severity, owner, and linked requirement.
6. Retest the affected behavior and a reconciliation control after correction.
7. Business owner records approval/rejection; unresolved Must controls remain visible in the release review.

## Defect severity

Critical: unauthorized disclosure, corrupt source, or release of materially incorrect totals. High: wrong business population, failed monetary reconciliation, incorrect weighted KPI, or unsupported causal claim. Medium: a drilldown, filter, or workflow issue that does not corrupt controls. Low: cosmetic issues with no interpretive effect. Severity is based on business effect, not how easy the fix appears.

## Current RAID and exception context

| ID | Type | Issue / risk | Owner | Response |
| --- | --- | --- | --- | --- |
| REG-R-01 | Risk | Restaurant data described as rep data | Sales Operations Manager | Rewrite scope and dictionary using actual fields. |
| REG-R-02 | Risk | Missing month appears as a sales decline | Sales Operations Manager | Coverage check and adjacency condition. |
| REG-R-03 | Risk | Ranking interpreted as profitability | Sales Operations Manager | Sales-only labels and request cost data. |
| REG-A-01 | Assumption | Currency is USD and supplied extracts are permitted portfolio data; original external provenance is not independently established. | BA | Confirm provenance, currency, and publication permission before commercial reuse. |
| REG-D-01 | Dependency | Obtain monthly targets, store operating calendar, closures, currency, comparable-store flags, costs, and prior-year sales before extending performance conclusions. | Source System Administrator | Obtain source contracts and required additional fields. |
| REG-I-01 | Issue | There are no revenue targets, sales reps, product categories, operating costs, or prior-year records. This case cannot establish target attainment, profitability, rep performance, or year-over-year change. | BA | Keep limitations next to measures and distinguish design from executed evidence. |

## Change-control worked example

REG-CR-01 addresses the observed mismatch between historical claims and supplied source evidence. The BA records the trigger, affected requirements, data consequences, test impact, and proposed disposition. Source bytes stay unchanged. Current narrative and query specifications replace generic claims. The portfolio correction is delivered; no external sponsor approval is invented.

For a subsequent request such as adding a profitability KPI, inspect whether costs and a reconciled cost definition exist. If not, update scope, dependencies, mapping, acceptance criteria, tests, and delivery estimates. The sponsor may approve collecting new data or defer the feature. The BA must not label a revenue proxy as profit to satisfy the change informally.

## Approval gates

| Gate | Accountable role | Required evidence | Current state |
| --- | --- | --- | --- |
| Source / metric approval | Business owner and source owner | Grain, provenance, definitions, control totals | Pending simulated review |
| Technical verification | Engineer | Query runs and meaningful fixtures | See executed Quality report |
| Business acceptance | Business owner | Executed UAT and defect dispositions | Not executed |
| Access approval | Control reviewer | Positive/negative role and export tests | Design only |
| Release | Sponsor | All gates, monitoring, rollback plan | Not deployed |
