# Case study: CRM Pipeline Definitions and Forecast Readiness

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Engagement framing

A sales operations team needs a transparent pipeline view that separates open opportunities, closed outcomes, and probability-weighted amounts before using the CRM extract in a forecast discussion. This independent portfolio exercise demonstrates requirements definition, source investigation, analytical validation, process design, and implementation handoff. It does not claim a paid engagement or deployed business outcome.

## My role and method

The portfolio author acts as the BA: frame the reporting decision, inspect the actual source, define grain and KPIs, record gaps, prioritize requirements, specify controls, and connect findings to acceptance tests. Local SQL analyses and independent fixtures are executed. Stakeholder conversations, application features, production access controls, and business UAT are proposed rather than represented as completed work.

1. Profile 10 records and preserve original input bytes.
2. Map source fields to a typed canonical schema with source_row lineage.
3. Define ratio-of-sums metrics and source control totals.
4. Execute five analyses and export reproducible CSV evidence.
5. Identify limits before recommending a business action.
6. Link requirements to stories, acceptance criteria, tests, and release responsibilities.

## Findings supported by the supplied data

| Finding | Observed result | Evidence | Interpretation limit | Recommended action |
| --- | --- | --- | --- | --- |
| Open pipeline | Open opportunity amount is $119,000.00; weighted open amount is $53,550.00. | [SQL/Q02.sql](../SQL/Q02.sql) / [Analysis/Q02.csv](../Analysis/Q02.csv) | Weighted amounts are probability-based scenario values, not booked or dated forecast revenue. | Use open-only amounts in forecast-readiness discussions. |
| Closed outcomes | Closed won $30,000.00; closed lost $15,000.00. | [SQL/Q02.sql](../SQL/Q02.sql) / [Analysis/Q02.csv](../Analysis/Q02.csv) | Closed outcomes belong outside open pipeline; this snapshot does not support historical win rate. | Reconcile open plus closed to all-record amount. |
| Snapshot size | 10 opportunity records; all-record amount $164,000.00. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | No snapshot date, close date, cohort, or stage history is supplied. | Request timing and history fields before velocity or forecast accuracy reporting. |
| Opportunity review | Opportunity D (Negotiate) has the highest weighted open amount: $13,500.00. | [SQL/Q04.sql](../SQL/Q04.sql) / [Analysis/Q04.csv](../Analysis/Q04.csv) | No activity history explains probability or deal quality. | Ask the owner to validate stage and probability with account context. |

## Data quality and unresolved questions

- Full-record repetitions: **0**. These are profiled, not automatically removed. A full-row match is not proof of duplication when event keys are absent.
- Domain exceptions found by the loader: **0**. Other source limitations remain relevant even if domain checks pass.
- Input SHA-256: `bbdd4b36ce5cbbe112022dc98642a881256a2f27fa2ce444d5eb912c685f2616`.
- There are no close dates, owners, customer identifiers, stage history, snapshot dates, or activities. This is a small current-state snapshot and cannot establish conversion rates, sales velocity, forecast accuracy, or a historical win rate.
- Add snapshot_date, owner_id, created_date, expected_close_date, stage_history, loss_reason, account_id, and approved probability policy before time-bounded forecasting.

## Alternatives and recommendation

Continue manual reporting with generic KPI labels: low implementation effort, but risks inconsistent interpretation and unsupported claims. Publish an automated report immediately: faster distribution, but source contracts and access controls remain unapproved. Recommended approach: approve definitions and reconciliations first, implement the minimum governed reporting solution, then measure adoption and process time in a limited pilot.

Each recommendation is a next validation or review action. Financial uplift, labor savings, causal explanations, and improved forecast accuracy remain unmeasured. A real sponsor must decide whether the evidence is sufficient and which additional data is worth collecting.

## What I would discuss in an interview

I would demonstrate one requirement through its source field, SQL result, acceptance criterion, and test fixture. I would explain why weighted metrics differ from averages of percentages, what this extract cannot prove, and how I would resolve a stakeholder disagreement before release. I would distinguish executed analysis from proposed implementation, and describe the additional fields required for a production handoff.
