# Case study: Advertising Efficiency and Budget Review

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Engagement framing

A growth team needs a consistent way to compare ad groups and device mix while finance needs clarity on whether revenue/spend ratios represent ROAS, contribution, or full business ROI. This independent portfolio exercise demonstrates requirements definition, source investigation, analytical validation, process design, and implementation handoff. It does not claim a paid engagement or deployed business outcome.

## My role and method

The portfolio author acts as the BA: frame the reporting decision, inspect the actual source, define grain and KPIs, record gaps, prioritize requirements, specify controls, and connect findings to acceptance tests. Local SQL analyses and independent fixtures are executed. Stakeholder conversations, application features, production access controls, and business UAT are proposed rather than represented as completed work.

1. Profile 1,104 records and preserve original input bytes.
2. Map source fields to a typed canonical schema with source_row lineage.
3. Define ratio-of-sums metrics and source control totals.
4. Execute five analyses and export reproducible CSV evidence.
5. Identify limits before recommending a business action.
6. Link requirements to stories, acceptance criteria, tests, and release responsibilities.

## Findings supported by the supplied data

| Finding | Observed result | Evidence | Interpretation limit | Recommended action |
| --- | --- | --- | --- | --- |
| Advertising baseline | Attributed revenue $1,675,567.96; spend $1,254,002.01; weighted ROAS 1.34x. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | Attribution is not incrementality and the attribution window is unknown. | Confirm attribution definitions before comparing across platforms. |
| Ad-group review candidate | Affiliates has the highest observed ROAS at 2.20x on $82,332.05 spend. | [SQL/Q02.sql](../SQL/Q02.sql) / [Analysis/Q02.csv](../Analysis/Q02.csv) | High average efficiency does not prove marginal response to more spend. | Propose a capped test with a holdout and Finance review. |
| Ad-only contribution | Revenue minus ad cost is $421,565.95. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | This omits COGS, agency fees, overhead, returns, and other business costs. | Label this ad-only contribution; request costs before full ROI or net profit reporting. |
| Response counts | 997,083 clicks and 20,129 attributed conversions. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | Conversion events do not prove incremental sales. | Display denominators and clarify the conversion window. |

## Data quality and unresolved questions

- Full-record repetitions: **0**. These are profiled, not automatically removed. A full-row match is not proof of duplication when event keys are absent.
- Domain exceptions found by the loader: **0**. Other source limitations remain relevant even if domain checks pass.
- Input SHA-256: `318e33a200b946d18701c20cfa715d0980c865b8353affcaaca86116d5ed4d83`.
- Attributed revenue does not prove incremental revenue. Revenue minus advertising cost excludes COGS, agency fees, returns, and other costs; it is an ad-only contribution measure, not full net profit or causal ROI.
- Obtain campaign IDs, attribution windows, order-level revenue, returns, COGS, agency fees, and experiment assignments before full ROI or incrementality reporting.

## Alternatives and recommendation

Continue manual reporting with generic KPI labels: low implementation effort, but risks inconsistent interpretation and unsupported claims. Publish an automated report immediately: faster distribution, but source contracts and access controls remain unapproved. Recommended approach: approve definitions and reconciliations first, implement the minimum governed reporting solution, then measure adoption and process time in a limited pilot.

Each recommendation is a next validation or review action. Financial uplift, labor savings, causal explanations, and improved forecast accuracy remain unmeasured. A real sponsor must decide whether the evidence is sufficient and which additional data is worth collecting.

## What I would discuss in an interview

I would demonstrate one requirement through its source field, SQL result, acceptance criterion, and test fixture. I would explain why weighted metrics differ from averages of percentages, what this extract cannot prove, and how I would resolve a stakeholder disagreement before release. I would distinguish executed analysis from proposed implementation, and describe the additional fields required for a production handoff.
