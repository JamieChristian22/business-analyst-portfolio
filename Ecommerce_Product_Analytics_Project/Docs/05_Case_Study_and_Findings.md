# Case study: Ecommerce Funnel Measurement and Experiment Discovery

**Local-system implementation update:** The shared workbench now implements filtered analysis, source drilldown, persistent UAT, analyst/reviewer workflow separation, gap closure, transactional source refresh, version conflicts, and audit history. Use [the system guide](../../Local_System/README.md) and [detailed gap analysis](10_Detailed_Gap_Analysis.md). Native BI/CRM configuration, enterprise RLS/SSO, external business UAT, and production release remain separate. References below to a future application describe those deployment/platform requirements; the shared local workbench is delivered.


## Engagement framing

An ecommerce team needs a reliable funnel baseline and device comparison to choose a checkout investigation without attributing drop-off to causes that were never measured. This independent portfolio exercise demonstrates requirements definition, source investigation, analytical validation, process design, and implementation handoff. It does not claim a paid engagement or deployed business outcome.

## My role and method

The portfolio author acts as the BA: frame the reporting decision, inspect the actual source, define grain and KPIs, record gaps, prioritize requirements, specify controls, and connect findings to acceptance tests. Local SQL analyses and independent fixtures are executed. Stakeholder conversations, application features, production access controls, and business UAT are proposed rather than represented as completed work.

1. Profile 14,000 records and preserve original input bytes.
2. Map source fields to a typed canonical schema with source_row lineage.
3. Define ratio-of-sums metrics and source control totals.
4. Execute five analyses and export reproducible CSV evidence.
5. Identify limits before recommending a business action.
6. Link requirements to stories, acceptance criteria, tests, and release responsibilities.

## Findings supported by the supplied data

| Finding | Observed result | Evidence | Interpretation limit | Recommended action |
| --- | --- | --- | --- | --- |
| Funnel baseline | 14,000 view observations, 2,406 cart observations, 1,608 checkout observations, and 1,200 purchase observations. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | No customer/session key proves unique people. | Use observation labels until an event/customer contract is approved. |
| Largest proportional transition loss | View to cart loses 82.81% of prior-stage observations (11,594 observations). | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | Loss identifies where to investigate, not why abandonment occurs. | Inspect errors, device context, and shipping/payment events before selecting a change. |
| Device comparison | desktop has the highest observed purchase/view rate at 10.58% across 4,425 view observations. | [SQL/Q02.sql](../SQL/Q02.sql) / [Analysis/Q02.csv](../Analysis/Q02.csv) | Device mix and channel differences are uncontrolled. | Use this comparison to prioritize investigation, not claim device causality. |
| Revenue and source profit | Revenue is $94,277.20; supplied profit is $23,418.34. | [SQL/Q01.sql](../SQL/Q01.sql) / [Analysis/Q01.csv](../Analysis/Q01.csv) | Source profit is not independently reconciled to costs. | Confirm the profit definition and obtain cost/return records before extending the economics. |

## Data quality and unresolved questions

- Full-record repetitions: **138**. These are profiled, not automatically removed. A full-row match is not proof of duplication when event keys are absent.
- Domain exceptions found by the loader: **0**. Other source limitations remain relevant even if domain checks pass.
- Input SHA-256: `12da40d34fac38874fb3387720bbf9d5f77835d4d60d5cbd3fe682a49f68bf64`.
- Repeated complete rows may be valid anonymous observations. Retain them until event keys establish duplication. There are no shipping fees, error events, experiment arms, or customer IDs; causal checkout explanations and unique-customer claims are unsupported.
- Add event_id, session_id, exposure_id, experiment_variant, timestamps, shipping quote events, payment outcomes, and consent flags before causal experimentation.

## Alternatives and recommendation

Continue manual reporting with generic KPI labels: low implementation effort, but risks inconsistent interpretation and unsupported claims. Publish an automated report immediately: faster distribution, but source contracts and access controls remain unapproved. Recommended approach: approve definitions and reconciliations first, implement the minimum governed reporting solution, then measure adoption and process time in a limited pilot.

Each recommendation is a next validation or review action. Financial uplift, labor savings, causal explanations, and improved forecast accuracy remain unmeasured. A real sponsor must decide whether the evidence is sufficient and which additional data is worth collecting.

## What I would discuss in an interview

I would demonstrate one requirement through its source field, SQL result, acceptance criterion, and test fixture. I would explain why weighted metrics differ from averages of percentages, what this extract cannot prove, and how I would resolve a stakeholder disagreement before release. I would distinguish executed analysis from proposed implementation, and describe the additional fields required for a production handoff.
