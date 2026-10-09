# Reproducible analysis results

Results are computed from supplied repository CSVs. Amounts are portfolio-assumed USD. Empty tables indicate no rows returned; they are not proof of production approval.

## Q01: Opportunity controls
[SQL](../SQL/Q01.sql) | [Full CSV output](Q01.csv)

| records | unique_opportunities | all_record_amount | all_record_weighted_amount |
| --- | --- | --- | --- |
| 10 | 10 | 164000.0 | 83550.0 |

## Q02: Open and closed bridge
[SQL](../SQL/Q02.sql) | [Full CSV output](Q02.csv)

| open_pipeline | weighted_open_pipeline | closed_won | closed_lost |
| --- | --- | --- | --- |
| 119000.0 | 53550.0 | 30000.0 | 15000.0 |

## Q03: Stage concentration
[SQL](../SQL/Q03.sql) | [Full CSV output](Q03.csv)

| stage | opportunities | amount | weighted_amount |
| --- | --- | --- | --- |
| Proposal | 3 | 67000.0 | 33500.0 |
| Closed Won | 1 | 30000.0 | 30000.0 |
| Meet | 2 | 21000.0 | 5250.0 |
| Negotiate | 1 | 18000.0 | 13500.0 |
| Closed Lost | 1 | 15000.0 | 0.0 |
| Qualify | 2 | 13000.0 | 1300.0 |

## Q04: Open opportunity review queue
[SQL](../SQL/Q04.sql) | [Full CSV output](Q04.csv)

| opportunity_id | stage | amount | probability | weighted_amount | review_rank |
| --- | --- | --- | --- | --- | --- |
| D | Negotiate | 18000.0 | 0.75 | 13500.0 | 1 |
| C | Proposal | 25000.0 | 0.5 | 12500.0 | 2 |
| H | Proposal | 22000.0 | 0.5 | 11000.0 | 3 |
| J | Proposal | 20000.0 | 0.5 | 10000.0 | 4 |
| B | Meet | 12000.0 | 0.25 | 3000.0 | 5 |
| I | Meet | 9000.0 | 0.25 | 2250.0 | 6 |
| G | Qualify | 8000.0 | 0.1 | 800.0 | 7 |
| A | Qualify | 5000.0 | 0.1 | 500.0 | 8 |

## Q05: Stage probability exceptions
[SQL](../SQL/Q05.sql) | [Full CSV output](Q05.csv)

No result rows. Review the query purpose and source profile.
