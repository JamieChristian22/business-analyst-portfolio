# Reproducible analysis results

Results are computed from supplied repository CSVs. Amounts are portfolio-assumed USD. Empty tables indicate no rows returned; they are not proof of production approval.

## Q01: Restaurant controls
[SQL](../SQL/Q01.sql) | [Full CSV output](Q01.csv)

| records | restaurants | months | sales |
| --- | --- | --- | --- |
| 1320 | 220 | 6 | 74146771.54 |

## Q02: Zone and city sales
[SQL](../SQL/Q02.sql) | [Full CSV output](Q02.csv)

| zone | city | sales | restaurants | sales_share |
| --- | --- | --- | --- | --- |
| 3 | Durham | 3437178.21 | 10 | 0.04635641092135405 |
| 4 | Fayetteville | 2929919.45 | 8 | 0.03951513180070686 |
| 4 | Wilmington | 2751329.42 | 8 | 0.03710653023531495 |
| 2 | Wilmington | 2745960.94 | 8 | 0.03703412681317668 |
| 5 | Greenville | 2644662.42 | 7 | 0.03566793759284964 |
| 3 | Winston-Salem | 2462281.08 | 7 | 0.03320820352470332 |
| 1 | Charlotte | 2424281.51 | 7 | 0.032695712296686726 |
| 2 | Raleigh | 2397453.41 | 7 | 0.032333888046718856 |
| 5 | Asheville | 2381584.41 | 7 | 0.032119866590755136 |
| 3 | Asheville | 2289283.27 | 7 | 0.030875022909999512 |
| 4 | Durham | 2199536.6 | 5 | 0.029664630762964706 |
| 2 | Charlotte | 2185673.73 | 6 | 0.029477665508617502 |
| 3 | Charlotte | 2150428.18 | 7 | 0.029002317098053385 |
| 2 | Greenville | 2054363.88 | 6 | 0.027706720566946477 |
| 1 | Asheville | 2037646.9100000001 | 5 | 0.027481262739818005 |
| 1 | Durham | 2006356.29 | 6 | 0.027059253536313846 |
| 5 | Wilmington | 1947886.75 | 6 | 0.026270688656338494 |
| 5 | Raleigh | 1812747.84 | 6 | 0.0244481020865767 |
| 4 | Raleigh | 1749553.42 | 6 | 0.023595813865694305 |
| 4 | Greenville | 1736409.8599999999 | 6 | 0.023418549775471448 |
First 20 of 44 result rows shown. Full output is in the linked CSV.

## Q03: Adjacent-month sales change
[SQL](../SQL/Q03.sql) | [Full CSV output](Q03.csv)

| month | sales | prior_month | prior_sales | mom_sales_change |
| --- | --- | --- | --- | --- |
| 2025-07 | 11650527.87 |  |  |  |
| 2025-08 | 11826132.28 | 2025-07 | 11650527.87 | 0.01507265696107898 |
| 2025-09 | 11941894.77 | 2025-08 | 11826132.28 | 0.009788702448033182 |
| 2025-10 | 12474314.59 | 2025-09 | 11941894.77 | 0.044584199597665713 |
| 2025-11 | 12868706.66 | 2025-10 | 12474314.59 | 0.03161633187575401 |
| 2025-12 | 13385195.37 | 2025-11 | 12868706.66 | 0.04013524619419672 |

## Q04: Restaurant rank and coverage
[SQL](../SQL/Q04.sql) | [Full CSV output](Q04.csv)

| restaurant_id | city | zone | sales | months_reported | sales_rank |
| --- | --- | --- | --- | --- | --- |
| R-0187 | Greensboro | 1 | 615248.51 | 6 | 1 |
| R-0186 | Fayetteville | 4 | 600041.52 | 6 | 2 |
| R-0164 | Wilmington | 2 | 554062.4400000001 | 6 | 3 |
| R-0154 | Asheville | 1 | 546988.9500000001 | 6 | 4 |
| R-0053 | Greenville | 3 | 546584.9199999999 | 6 | 5 |
| R-0172 | Durham | 1 | 520278.43 | 6 | 6 |
| R-0002 | Winston-Salem | 3 | 511454.14 | 6 | 7 |
| R-0001 | Raleigh | 5 | 500005.11 | 6 | 8 |
| R-0170 | Fayetteville | 4 | 498888.25 | 6 | 9 |
| R-0217 | Durham | 4 | 491063.11 | 6 | 10 |
| R-0071 | Wilmington | 5 | 490268.22000000003 | 6 | 11 |
| R-0133 | Durham | 4 | 488193.19999999995 | 6 | 12 |
| R-0197 | Charlotte | 2 | 481131.13 | 6 | 13 |
| R-0202 | Raleigh | 2 | 475261.26 | 6 | 14 |
| R-0129 | Wilmington | 2 | 464031.46 | 6 | 15 |
| R-0051 | Winston-Salem | 3 | 454847.49 | 6 | 16 |
| R-0192 | Asheville | 3 | 454412.9 | 6 | 17 |
| R-0042 | Winston-Salem | 4 | 452006.45 | 6 | 18 |
| R-0018 | Charlotte | 2 | 449209.9 | 6 | 19 |
| R-0119 | Greensboro | 4 | 445360.86 | 6 | 20 |
First 20 of 220 result rows shown. Full output is in the linked CSV.

## Q05: Duplicate key exceptions
[SQL](../SQL/Q05.sql) | [Full CSV output](Q05.csv)

No result rows. Review the query purpose and source profile.
