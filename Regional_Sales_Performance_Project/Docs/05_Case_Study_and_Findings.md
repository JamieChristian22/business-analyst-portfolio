# Case study: Restaurant Sales Reporting by City and Zone

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Engagement framing

A restaurant operations team needs monthly sales comparisons across cities and zones, stable restaurant rankings, and a defensible review of changes over the six-month extract. This independent portfolio exercise demonstrates requirements definition, source investigation, analytical validation, process design, and implementation handoff. It does not claim a paid engagement or deployed business outcome.

## My role and method

The portfolio author acts as the BA: frame the reporting decision, inspect the actual source, define grain and KPIs, record gaps, prioritize requirements, specify controls, and connect findings to acceptance tests. Local SQL analyses and independent fixtures are executed. Stakeholder conversations, application features, production access controls, and business UAT are proposed rather than represented as completed work.

1. Profile 1,320 records and preserve original input bytes.
2. Map source fields to a typed canonical schema with source_row lineage.
3. Define ratio-of-sums metrics and source control totals.
4. Execute five analyses and export reproducible CSV evidence.
5. Identify limits before recommending a business action.
6. Link requirements to stories, acceptance criteria, tests, and release responsibilities.

## Findings supported by the supplied data

| Finding | Observed result | Evidence | Interpretation limit | Recommended action |
| --- | --- | --- | --- | --- |
| Restaurant sales baseline | 220 restaurants across 6 months generate $74,146,771.54 sales. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | The extract contains restaurants, not sales reps or product margins. | Use restaurant/city/zone reporting labels. |
| Restaurant review | R-0187 in Greensboro has the highest six-month sales: $615,248.51. | [SQL/Q04.sql](../SQL/Q04.sql) / [Analysis/Q04.csv](../Analysis/Q04.csv) | Sales rank is not profitability or target attainment. | Ask the manager for operating calendar, size, and local context. |
| Latest monthly movement | 2025-12 sales are $13,385,195.37; adjacent-month change is 4.01%. | [SQL/Q03.sql](../SQL/Q03.sql) / [Analysis/Q03.csv](../Analysis/Q03.csv) | Six months cannot establish YoY changes or stable seasonality. | Discuss a comparable-month review and request prior-year records. |
| Coverage control | All 220 restaurants report all six supplied months. | [SQL/Q04.sql](../SQL/Q04.sql) / [Analysis/Q04.csv](../Analysis/Q04.csv) | Complete source coverage does not prove comparable operating days. | Obtain closures and comparable-store flags before performance judgments. |

## Data quality and unresolved questions

- Full-record repetitions: **0**. These are profiled, not automatically removed. A full-row match is not proof of duplication when event keys are absent.
- Domain exceptions found by the loader: **0**. Other source limitations remain relevant even if domain checks pass.
- Input SHA-256: `df348e86f66cca6a5e9c14a2fd638fe4d037e18f3fe0e2401475ea36250b12ef`.
- There are no revenue targets, sales reps, product categories, operating costs, or prior-year records. This case cannot establish target attainment, profitability, rep performance, or year-over-year change.
- Obtain monthly targets, store operating calendar, closures, currency, comparable-store flags, costs, and prior-year sales before extending performance conclusions.

## Alternatives and recommendation

Continue manual reporting with generic KPI labels: low implementation effort, but risks inconsistent interpretation and unsupported claims. Publish an automated report immediately: faster distribution, but source contracts and access controls remain unapproved. Recommended approach: approve definitions and reconciliations first, implement the minimum governed reporting solution, then measure adoption and process time in a limited pilot.

Each recommendation is a next validation or review action. Financial uplift, labor savings, causal explanations, and improved forecast accuracy remain unmeasured. A real sponsor must decide whether the evidence is sufficient and which additional data is worth collecting.

## What I would discuss in an interview

I would demonstrate one requirement through its source field, SQL result, acceptance criterion, and test fixture. I would explain why weighted metrics differ from averages of percentages, what this extract cannot prove, and how I would resolve a stakeholder disagreement before release. I would distinguish executed analysis from proposed implementation, and describe the additional fields required for a production handoff.
