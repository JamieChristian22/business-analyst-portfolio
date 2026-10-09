# Case study: Marketplace Revenue and Seller Reporting

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Engagement framing

A marketplace operations team needs one agreed view of gross merchandise value, platform revenue, seller concentration, and take rate before it reviews seller performance. This independent portfolio exercise demonstrates requirements definition, source investigation, analytical validation, process design, and implementation handoff. It does not claim a paid engagement or deployed business outcome.

## My role and method

The portfolio author acts as the BA: frame the reporting decision, inspect the actual source, define grain and KPIs, record gaps, prioritize requirements, specify controls, and connect findings to acceptance tests. Local SQL analyses and independent fixtures are executed. Stakeholder conversations, application features, production access controls, and business UAT are proposed rather than represented as completed work.

1. Profile 5,500 records and preserve original input bytes.
2. Map source fields to a typed canonical schema with source_row lineage.
3. Define ratio-of-sums metrics and source control totals.
4. Execute five analyses and export reproducible CSV evidence.
5. Identify limits before recommending a business action.
6. Link requirements to stories, acceptance criteria, tests, and release responsibilities.

## Findings supported by the supplied data

| Finding | Observed result | Evidence | Interpretation limit | Recommended action |
| --- | --- | --- | --- | --- |
| Portfolio volume | GMV $239,161.36; platform revenue $33,393.15; orders 5,500. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | GMV and platform revenue have different business meanings. | Use separate measures in monthly reporting. |
| Seller contribution | Apex Outdoor contributes 25.30% of GMV. | [SQL/Q03.sql](../SQL/Q03.sql) / [Analysis/Q03.csv](../Analysis/Q03.csv) | Concentration is observed; seller quality or margin is not measured. | Ask operations to review seller context before any commercial action. |
| Product concentration | Top 16 of 80 products contribute 24.44% of GMV. | [SQL/Q04.sql](../SQL/Q04.sql) / [Analysis/Q04.csv](../Analysis/Q04.csv) | This directly tests the historical generic Pareto claim. | Use the computed contribution rather than assume an 80/20 relationship. |
| Weighted monetization | Portfolio take rate is 13.96%; AOV is $43.48. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | The rates use the ratio of sums, not an average of row percentages. | Ask Finance to approve definitions and reconcile platform revenue to its ledger. |

## Data quality and unresolved questions

- Full-record repetitions: **0**. These are profiled, not automatically removed. A full-row match is not proof of duplication when event keys are absent.
- Domain exceptions found by the loader: **0**. Other source limitations remain relevant even if domain checks pass.
- Input SHA-256: `64d55b11b0676a1eef06846de2786e94a02e0b656860ac28a0c69b4e417daeba`.
- The dataset has no item cost, returns, seller fees beyond platform revenue, inventory, or experiment assignment. It cannot establish profit margins, pricing causality, or actual Amazon business performance.
- Request order_id, fee schedule, returns, item costs, seller SLAs, and ledger control totals before extending this case into commercial profitability.

## Alternatives and recommendation

Continue manual reporting with generic KPI labels: low implementation effort, but risks inconsistent interpretation and unsupported claims. Publish an automated report immediately: faster distribution, but source contracts and access controls remain unapproved. Recommended approach: approve definitions and reconciliations first, implement the minimum governed reporting solution, then measure adoption and process time in a limited pilot.

Each recommendation is a next validation or review action. Financial uplift, labor savings, causal explanations, and improved forecast accuracy remain unmeasured. A real sponsor must decide whether the evidence is sufficient and which additional data is worth collecting.

## What I would discuss in an interview

I would demonstrate one requirement through its source field, SQL result, acceptance criterion, and test fixture. I would explain why weighted metrics differ from averages of percentages, what this extract cannot prove, and how I would resolve a stakeholder disagreement before release. I would distinguish executed analysis from proposed implementation, and describe the additional fields required for a production handoff.
