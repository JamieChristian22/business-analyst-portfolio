# Reproducible analysis results

Results are computed from supplied repository CSVs. Amounts are portfolio-assumed USD. Empty tables indicate no rows returned; they are not proof of production approval.

## Q01: Funnel control totals
[SQL](../SQL/Q01.sql) | [Full CSV output](Q01.csv)

| records | views | carts | checkouts | purchases | orders | revenue | profit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 14000 | 14000.0 | 2406.0 | 1608.0 | 1200.0 | 1200.0 | 94277.2 | 23418.34 |

## Q02: Device funnel
[SQL](../SQL/Q02.sql) | [Full CSV output](Q02.csv)

| device | views | carts | checkouts | purchases | view_cart_rate | cart_checkout_rate | checkout_purchase_rate | view_purchase_rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mobile | 9003.0 | 1439.0 | 907.0 | 672.0 | 0.15983561035210486 | 0.6302988186240445 | 0.74090407938258 | 0.07464178607130956 |
| desktop | 4425.0 | 867.0 | 627.0 | 468.0 | 0.1959322033898305 | 0.7231833910034602 | 0.7464114832535885 | 0.10576271186440678 |
| tablet | 572.0 | 100.0 | 74.0 | 60.0 | 0.17482517482517482 | 0.74 | 0.8108108108108109 | 0.1048951048951049 |

## Q03: Channel economics
[SQL](../SQL/Q03.sql) | [Full CSV output](Q03.csv)

| channel | views | purchases | orders | revenue | profit | profit_margin | aov |
| --- | --- | --- | --- | --- | --- | --- | --- |
| organic | 5392.0 | 471.0 | 471.0 | 37144.42 | 9189.99 | 0.24741239733989656 | 78.86288747346072 |
| paid_search | 2946.0 | 260.0 | 260.0 | 20771.3 | 5164.76 | 0.24864885683611523 | 79.88961538461538 |
| paid_social | 2601.0 | 201.0 | 201.0 | 15748.23 | 3913.98 | 0.24853459722140203 | 78.34940298507462 |
| email | 2054.0 | 187.0 | 187.0 | 14242.56 | 3540.1 | 0.24855784353374674 | 76.16342245989304 |
| referral | 1007.0 | 81.0 | 81.0 | 6370.69 | 1609.51 | 0.25264296332108455 | 78.65049382716049 |

## Q04: Monthly ecommerce metrics
[SQL](../SQL/Q04.sql) | [Full CSV output](Q04.csv)

| month | views | purchases | revenue | prior_revenue | view_purchase_rate | mom_revenue_change |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-07 | 2334.0 | 197.0 | 15718.710000000001 |  | 0.0844044558697515 |  |
| 2025-08 | 2328.0 | 199.0 | 15641.85 | 15718.710000000001 | 0.08548109965635739 | -0.0048897142322748225 |
| 2025-09 | 2289.0 | 177.0 | 13689.16 | 15641.85 | 0.07732634338138926 | -0.12483753520203815 |
| 2025-10 | 2450.0 | 223.0 | 17395.7 | 13689.16 | 0.0910204081632653 | 0.2707646049867195 |
| 2025-11 | 2241.0 | 189.0 | 14771.39 | 17395.7 | 0.08433734939759036 | -0.15085969521203524 |
| 2025-12 | 2358.0 | 215.0 | 17060.39 | 14771.39 | 0.09117896522476675 | 0.1549617199193847 |

## Q05: Funnel validity exceptions
[SQL](../SQL/Q05.sql) | [Full CSV output](Q05.csv)

No result rows. Review the query purpose and source profile.
