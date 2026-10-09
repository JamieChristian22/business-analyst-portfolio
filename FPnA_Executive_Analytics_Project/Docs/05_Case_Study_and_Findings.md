# Case study: Finance Reporting Reconciliation and Variance Control

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Engagement framing

Finance has two supplied extracts: a dashboard summary and an account fact table. Leadership needs reconciled actual/budget reporting and an explicit treatment of any differences before a close pack can be approved. This independent portfolio exercise demonstrates requirements definition, source investigation, analytical validation, process design, and implementation handoff. It does not claim a paid engagement or deployed business outcome.

## My role and method

The portfolio author acts as the BA: frame the reporting decision, inspect the actual source, define grain and KPIs, record gaps, prioritize requirements, specify controls, and connect findings to acceptance tests. Local SQL analyses and independent fixtures are executed. Stakeholder conversations, application features, production access controls, and business UAT are proposed rather than represented as completed work.

1. Profile 420 records and preserve original input bytes.
2. Map source fields to a typed canonical schema with source_row lineage.
3. Define ratio-of-sums metrics and source control totals.
4. Execute five analyses and export reproducible CSV evidence.
5. Identify limits before recommending a business action.
6. Link requirements to stories, acceptance criteria, tests, and release responsibilities.

## Findings supported by the supplied data

| Finding | Observed result | Evidence | Interpretation limit | Recommended action |
| --- | --- | --- | --- | --- |
| Account-fact baseline | Actual revenue $13,328,601.00 versus budget $13,330,369.00; variance $-1,768.00 (-0.01%). | [SQL/Q02.sql](../SQL/Q02.sql) / [Analysis/Q02.csv](../Analysis/Q02.csv) | These totals come from the fact table only. | Review the signed variance by department and keep the dashboard source separate. |
| Operating income | Fact-derived actual operating income is $1,447,948.00. | [SQL/Q02.sql](../SQL/Q02.sql) / [Analysis/Q02.csv](../Analysis/Q02.csv) | Positive COGS and OpEx are subtracted; no balance sheet or cash flow is present. | Confirm sign and account mapping with Accounting. |
| Revenue source reconciliation | 30 of 30 month/department revenue comparisons match within $0.01; 0 remain unresolved. | [SQL/Q04.sql](../SQL/Q04.sql) / [Analysis/Q04.csv](../Analysis/Q04.csv) | Revenue matching does not validate every summary field, an approved ledger, or business acceptance. | Retain the reconciliation at every refresh; any future difference blocks a production close pack until the reviewer approves its resolution. |
| Variance ownership | Customer Success has the lowest signed revenue variance: $-19,990.00. | [SQL/Q03.sql](../SQL/Q03.sql) / [Analysis/Q03.csv](../Analysis/Q03.csv) | Variance magnitude does not establish cause or personal performance. | Request a department narrative supported by operational drivers. |

## Data quality and unresolved questions

- Full-record repetitions: **0**. These are profiled, not automatically removed. A full-row match is not proof of duplication when event keys are absent.
- Domain exceptions found by the loader: **0**. Other source limitations remain relevant even if domain checks pass.
- Input SHA-256: `da43a29ac9694d4dccf43ffd065e311773e6b5bdb771fe2da8a56778159d8225`.
- The two supplied extracts are not assumed to share totals or definitions. The account fact table is the analysis basis; reconciliation differences remain visible and block production close approval. There are no balance sheet or cash-flow records.
- Obtain ledger control totals, chart-of-accounts mapping, approved budget version, FX policy, fiscal calendar, and controller signoff before production finance use.

## Alternatives and recommendation

Continue manual reporting with generic KPI labels: low implementation effort, but risks inconsistent interpretation and unsupported claims. Publish an automated report immediately: faster distribution, but source contracts and access controls remain unapproved. Recommended approach: approve definitions and reconciliations first, implement the minimum governed reporting solution, then measure adoption and process time in a limited pilot.

Each recommendation is a next validation or review action. Financial uplift, labor savings, causal explanations, and improved forecast accuracy remain unmeasured. A real sponsor must decide whether the evidence is sufficient and which additional data is worth collecting.

## What I would discuss in an interview

I would demonstrate one requirement through its source field, SQL result, acceptance criterion, and test fixture. I would explain why weighted metrics differ from averages of percentages, what this extract cannot prove, and how I would resolve a stakeholder disagreement before release. I would distinguish executed analysis from proposed implementation, and describe the additional fields required for a production handoff.
