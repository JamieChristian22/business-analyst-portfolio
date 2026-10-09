# Reproducible analysis results

Results are computed from supplied repository CSVs. Amounts are portfolio-assumed USD. Empty tables indicate no rows returned; they are not proof of production approval.

## Q01: Finance controls
[SQL](../SQL/Q01.sql) | [Full CSV output](Q01.csv)

| scenario | account_category | records | amount |
| --- | --- | --- | --- |
| Actual | COGS | 60 | 5399711.0 |
| Actual | OpEx | 90 | 6480942.0 |
| Actual | Revenue | 60 | 13328601.0 |
| Budget | COGS | 60 | 5382121.0 |
| Budget | OpEx | 90 | 6513882.0 |
| Budget | Revenue | 60 | 13330369.0 |

## Q02: Monthly actual budget bridge
[SQL](../SQL/Q02.sql) | [Full CSV output](Q02.csv)

| month | revenue_actual | revenue_budget | cogs_actual | opex_actual | revenue_variance | revenue_variance_rate | operating_income | gross_margin |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-07 | 2197675.0 | 2187801.0 | 885630.0 | 998261.0 | 9874.0 | 0.004513207554069132 | 313784.0 | 0.5970150272447018 |
| 2025-08 | 2121690.0 | 2121022.0 | 664418.0 | 1179216.0 | 668.0 | 0.00031494251356185837 | 278056.0 | 0.6868449207942725 |
| 2025-09 | 2174210.0 | 2155376.0 | 938596.0 | 1028612.0 | 18834.0 | 0.008738150559345561 | 207002.0 | 0.5683048095630137 |
| 2025-10 | 1976318.0 | 1976360.0 | 961430.0 | 1159106.0 | -42.0 | -2.1251189054625674e-05 | -144218.0 | 0.5135246453252968 |
| 2025-11 | 2524320.0 | 2538970.0 | 893945.0 | 985074.0 | -14650.0 | -0.005770056361437906 | 645301.0 | 0.6458670057678899 |
| 2025-12 | 2334388.0 | 2350840.0 | 1055692.0 | 1130673.0 | -16452.0 | -0.006998349526126831 | 148023.0 | 0.5477649816568625 |

## Q03: Department revenue variance
[SQL](../SQL/Q03.sql) | [Full CSV output](Q03.csv)

| department | revenue_actual | revenue_budget | revenue_variance | revenue_variance_rate |
| --- | --- | --- | --- | --- |
| Customer Success | 2480778.0 | 2500768.0 | -19990.0 | -0.007993544383165492 |
| G&A | 2548647.0 | 2555564.0 | -6917.0 | -0.0027066432302223697 |
| Sales | 2757144.0 | 2763237.0 | -6093.0 | -0.0022050225876390625 |
| Marketing | 2729841.0 | 2722188.0 | 7653.0 | 0.002811341465027397 |
| Product | 2812191.0 | 2788612.0 | 23579.0 | 0.00845546099636665 |

## Q04: Fact versus dashboard reconciliation
[SQL](../SQL/Q04.sql) | [Full CSV output](Q04.csv)

| month | department | fact_revenue | dashboard_revenue | difference | disposition |
| --- | --- | --- | --- | --- | --- |
| 2025-07 | Customer Success | 368128.0 | 368128.0 | 0.0 | MATCH |
| 2025-07 | G&A | 375318.0 | 375318.0 | 0.0 | MATCH |
| 2025-07 | Marketing | 360350.0 | 360350.0 | 0.0 | MATCH |
| 2025-07 | Product | 545938.0 | 545938.0 | 0.0 | MATCH |
| 2025-07 | Sales | 547941.0 | 547941.0 | 0.0 | MATCH |
| 2025-08 | Customer Success | 453624.0 | 453624.0 | 0.0 | MATCH |
| 2025-08 | G&A | 315498.0 | 315498.0 | 0.0 | MATCH |
| 2025-08 | Marketing | 563998.0 | 563998.0 | 0.0 | MATCH |
| 2025-08 | Product | 367367.0 | 367367.0 | 0.0 | MATCH |
| 2025-08 | Sales | 421203.0 | 421203.0 | 0.0 | MATCH |
| 2025-09 | Customer Success | 403447.0 | 403447.0 | 0.0 | MATCH |
| 2025-09 | G&A | 409922.0 | 409922.0 | 0.0 | MATCH |
| 2025-09 | Marketing | 539321.0 | 539321.0 | 0.0 | MATCH |
| 2025-09 | Product | 442166.0 | 442166.0 | 0.0 | MATCH |
| 2025-09 | Sales | 379354.0 | 379354.0 | 0.0 | MATCH |
| 2025-10 | Customer Success | 396335.0 | 396335.0 | 0.0 | MATCH |
| 2025-10 | G&A | 398136.0 | 398136.0 | 0.0 | MATCH |
| 2025-10 | Marketing | 405994.0 | 405994.0 | 0.0 | MATCH |
| 2025-10 | Product | 353517.0 | 353517.0 | 0.0 | MATCH |
| 2025-10 | Sales | 422336.0 | 422336.0 | 0.0 | MATCH |
First 20 of 30 result rows shown. Full output is in the linked CSV.

## Q05: Budget completeness
[SQL](../SQL/Q05.sql) | [Full CSV output](Q05.csv)

No result rows. Review the query purpose and source profile.
